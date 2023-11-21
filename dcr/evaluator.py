from typing import Dict, List

import pandas as pd

from dcr.components.dce_amc import DCE_AMC
from dcr.components.llm import LLM
from dcr.inputs.evaluator_input import EvaluatorInput
from dcr.prompts.amc_prompt import amc_prompt
from dcr.prompts.dce_summary_prompt import dce_summary_prompt


def evaluate(
    llm: LLM,
    model_config: Dict,
    input_data: List[Dict],
    amc_prompt=amc_prompt,
    dce_prompt=dce_summary_prompt,
    worker_count=1,
) -> pd.DataFrame:
    orin_df = pd.DataFrame.from_dict(input_data)

    evaluator_inputs = []
    for item in input_data:
        evaluator_inputs.append(EvaluatorInput(item))

    dce_amc = DCE_AMC(llm, model_config)
    dce_df = dce_amc.evaluate(
        dce_prompt, amc_prompt, evaluator_inputs, worker_count=worker_count
    )

    final_df = pd.merge(orin_df, dce_df, on="id", how="left")
    return final_df
