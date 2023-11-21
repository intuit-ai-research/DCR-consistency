import ast
import datetime
import json
import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

import pandas as pd

from dcr.components.llm import LLM
from dcr.inputs.input import Input
from dcr.utils import divide_input, get_final_prompt


class RAI:
    def __init__(self, llm: LLM, model_config: Dict):
        self.model_config = model_config
        self.llm = llm

        # setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def improve(
        self, rai_prompt: str, orin_data_list: List[Input], worker_count: int = 1
    ):
        self.logger.info("=========Improving started=========")
        self.logger.info(
            f"data length: {len(orin_data_list)}, worker count: {worker_count}"
        )

        input_divided = divide_input(orin_data_list, worker_count)
        self.logger.info(f"divided input into {len(input_divided)} parts")

        res = self._multi_thread_improve(rai_prompt, input_divided, worker_count)
        self.logger.info(f"improving complete")
        return res

    def _multi_thread_improve(
        self, rai_prompt: str, input_divided: List[Input], worker_count: int
    ) -> pd.DataFrame:
        improve_queue = queue.Queue()
        improver_pool = ThreadPoolExecutor(max_workers=worker_count)

        start = datetime.datetime.now()
        self.logger.info(f"improver started at {start}")

        improver_futures = [
            improver_pool.submit(self.rai, rai_prompt, divided, improve_queue)
            for divided in input_divided
        ]

        for future in improver_futures:
            future.result()

        end = datetime.datetime.now()
        improver_pool.shutdown()

        self.logger.info(f"all time taken: {end - start}")

        # because of multi-trhead, the order of items in result queue does not match the order in the
        # input, thus sort the result queue by index
        res = list(improve_queue.queue)
        res = sorted(res, key=lambda x: x[0])

        final_df = pd.DataFrame(res, columns=["id", "improved_version", "rai_raw"])
        return final_df

    def rai(self, rai_prompt: str, data_list: List[Input], improve_queue: queue.Queue):
        for data in data_list:
            data = data.get_data()
            self.logger.info(f"get data {data}")
            index = data.get("id")

            improved = "-1"
            rai_raw = ""
            try:
                final_prompt = get_final_prompt(rai_prompt, **data)
                message_prompt = [{"role": "user", "content": final_prompt}]
                self.logger.info(
                    f"Improver: for {index}, final prompt is {message_prompt}"
                )
                rai_raw = self.llm.get_chat_response(
                    message_prompt, **self.model_config
                )
                self.logger.info(f"Improver: for {index}, {rai_raw}")

                res = ast.literal_eval(rai_raw)
                improved = ""
                for sentence in res:
                    improved += sentence["improved_sentence"] + " "
            except Exception as e:
                self.logger.error(f"Improver for {index}, exception caught: {e}")

            improve_queue.put((index, improved, rai_raw))
