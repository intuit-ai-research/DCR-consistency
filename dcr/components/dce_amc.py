import datetime
import json
import logging
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

import pandas as pd

from dcr.components.llm import LLM
from dcr.inputs.input import Input
from dcr.utils import divide_input, get_final_prompt


class DCE_AMC:
    ERROR_SCORE = -1000000

    def __init__(self, llm: LLM, model_config: Dict):
        self.llm = llm
        self.model_config = model_config

        # setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def evaluate(
        self,
        dce_prompt: str,
        amc_prompt: str,
        orin_data_list: List[Input],
        worker_count: int = 1,
    ) -> pd.DataFrame:
        self.logger.info("=========Evaluation started=========")
        self.logger.info(f"divider prompt is: {dce_prompt}")
        self.logger.info(f"conquer prompt is: {amc_prompt}")
        self.logger.info(
            f"data length: {len(orin_data_list)}, worker count: {worker_count}"
        )

        # divide the input data so each divider worker can take a portion of load
        input_divided = divide_input(orin_data_list, worker_count)
        self.logger.info(f"divided input into {len(input_divided)} parts")
        return self._multi_thread_evaluate(
            dce_prompt, amc_prompt, input_divided, worker_count
        )

    def _multi_thread_evaluate(
        self,
        dce_prompt: str,
        amc_prompt: str,
        input_divided: List[Dict],
        worker_count: int,
    ) -> pd.DataFrame:
        # stop_flag is the singal that AMC threads listens to. If it is true, AMC threads will stop
        stop_flag = {"stop": False}
        # shared queue is accesed by both DCE threads and AMC threads.
        # DCE thread put items into this shared queue
        # AMC thread takes items from the shared queue
        shared_queue = queue.Queue()
        results_queue = queue.Queue()

        # party begins
        dce_pool = ThreadPoolExecutor(max_workers=worker_count)
        amc_pool = ThreadPoolExecutor(max_workers=worker_count)

        start = datetime.datetime.now()
        self.logger.info(f"DCE started at {start}")

        dce_futures = [
            dce_pool.submit(
                self.divider_conquer_evaluator, dce_prompt, divided, shared_queue
            )
            for divided in input_divided
        ]
        amc_futures = [
            amc_pool.submit(
                self.auto_metric_converter,
                amc_prompt,
                shared_queue,
                results_queue,
                stop_flag,
            )
            for _ in range(worker_count)
        ]

        # wait for the DCE pool to finish
        for future in dce_futures:
            future.result()

        # notify AMC pool that DCE has finished
        stop_flag["stop"] = True
        mid = datetime.datetime.now()
        dce_pool.shutdown()

        # wait for AMC pool to finish
        for future in amc_futures:
            future.result()
        amc_pool.shutdown()
        end = datetime.datetime.now()

        self.logger.info(f"all time taken: {end - start}")
        self.logger.info(f"DCE time taken: {mid - start}")
        self.logger.info(f"lingering AMC time taken: {end - mid}")

        # because of multi-trhead, the order of items in result queue does not match the order in the
        # input, thus sort the result queue by index
        res = list(results_queue.queue)
        res = sorted(res, key=lambda x: x[0])

        final_df = pd.DataFrame(
            res,
            columns=[
                "id",
                "score",
                "dce_reasons",
                "amc_reasons",
                "dce_raw",
                "amc_raw",
                "decision",
            ],
        )

        return final_df

    def divider_conquer_evaluator(
        self, dce_prompt: str, data_list: List[Input], shared_queue: queue.Queue
    ):
        for data in data_list:
            data = data.get_data()
            id = data.get("id")

            try:
                final_prompt = get_final_prompt(dce_prompt, **data)
                message_prompt = [{"role": "user", "content": final_prompt}]
                self.logger.debug(f"DCE: for {id}, final prompt is {message_prompt}")

                res_raw_dce = self.llm.get_chat_response(
                    message_prompt, **self.model_config
                )
                self.logger.debug(f"DCE: for {id}, llm response: {res_raw_dce}")

                # parsing result
                res_dce = json.loads(res_raw_dce)
                if res_dce["reason"]:
                    data = res_dce["reason"]
                    reasons = [d.get("reason", "") for d in data]
                    decision = res_dce["is_consistent"]
                    self.logger.info(f"DCE: for {id}, adding to queue")
                    shared_queue.put((id, reasons, res_raw_dce, decision))
            except Exception as e:
                self.logger.error(f"DCE: for {id}, divider error {e}")
                shared_queue.put((id, "", "", ""))

        self.logger.info(f"DCE completed successfully")

    def auto_metric_converter(
        self,
        amc_prompt: str,
        shared_queue: queue.Queue,
        results_queue: queue.Queue,
        stop_flag: bool,
    ):
        while not stop_flag["stop"] or not shared_queue.empty():
            self.logger.debug(
                f"AMC: stop flag: {stop_flag} ; queue size {shared_queue.qsize()}"
            )
            score = self.ERROR_SCORE

            if not shared_queue.empty():
                ind, dce_reasons, res_raw, decision = shared_queue.get()
                answer = ""
                amc_reason = ""
                res_raw_amc = ""
                res_amc = ""
                if len(dce_reasons) > 0:
                    reason_str = ""
                    for reason in dce_reasons:
                        reason_str += f"* {reason} \n"
                    data = {"attempt_answer": reason_str}
                    try:
                        final_prompt_dc = get_final_prompt(amc_prompt, **data)

                        message_prompt = [{"role": "user", "content": final_prompt_dc}]
                        self.logger.debug(
                            f"AMC: for {ind} final prompt is {message_prompt}"
                        )

                        res_raw_amc = self.llm.get_chat_response(
                            message_prompt, **self.model_config
                        )
                        res_raw_amc = res_raw_amc.replace("+1", "1")
                        self.logger.debug(
                            f"AMC: for {ind}, llm response: {res_raw_amc}"
                        )

                        ## final metric calculation.
                        res_amc = json.loads(res_raw_amc)
                        answer = res_amc.get("answer")
                        score = sum(answer) / len(answer)
                        score = (score + 1) / 2
                        amc_reason = res_amc.get("reason")

                    except Exception as e:
                        self.logger.error(f"AMC: for {ind}, exception caught: {e}")

                self.logger.debug(f"AMC: adding score for {ind} , {score}")
                results_queue.put(
                    (ind, score, dce_reasons, amc_reason, res_raw, res_amc, decision)
                )
            else:
                time.sleep(1)
