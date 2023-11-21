import json

import pandas as pd

from dcr.components.llm import LLM
from dcr.evaluator import evaluate
from dcr.improver import improve


class OpenAIConnector(LLM):
    """Example Test class

    Args:
        LLM (_type_): handles api calls to Openai models
    """

    def get_chat_response(self, prompt, tims=0, **model_config) -> str:
        return ""


LLM_CONNECTOR = OpenAIConnector()
MODEL_CONFIG = {
    "model": "gpt-4",
    "temperature": 0,
}

SOURCE_FILE = "./examples/qags_cnndm.json"
OUTPUT_DCE_AMC = "test_gags.csv"
OUTPUT_RAI = "test_gags_improved.csv"


def evalute_example():
    data = get_qags_data()
    res = evaluate(LLM_CONNECTOR, MODEL_CONFIG, data, worker_count=5)
    res.to_csv(OUTPUT_DCE_AMC, index=False)


def improve_example():
    data = transfer_data_from_dce_amc()
    res = improve(LLM_CONNECTOR, MODEL_CONFIG, data, worker_count=5)
    res.to_csv(OUTPUT_RAI, index=False)


def get_qags_data():
    data = []
    with open(SOURCE_FILE) as f:
        raw_data = json.load(f)
        for item in raw_data[:50]:
            doc_id = item["doc_id"]
            article = item["source"]
            summary = item["system_output"]
            consistency_score = item["scores"]["consistency"]
            data.append(
                {
                    "id": doc_id,
                    "reference": article,
                    "candidate": summary,
                    "label": consistency_score,
                }
            )
        return data


def transfer_data_from_dce_amc():
    df = pd.read_csv(OUTPUT_DCE_AMC)
    cleaned_input = []

    def get_data(item):
        id, reference, score, dce_raw = (
            item["id"],
            item["reference"],
            item["score"],
            json.loads(item["dce_raw"]),
        )

        # only look at the ones that is inconsistent
        if score < 1:
            sentences = dce_raw["reason"]
            final_sentences = ""
            for sentence in sentences:
                reason = sentence["reason"]
                final_sentences += f"- sentence: {sentence} \n"
                final_sentences += f"  reason: {reason}\n"
            cleaned_input.append(
                {"id": id, "article": reference, "sentences": final_sentences}
            )

    df.apply(get_data, axis=1)
    return cleaned_input


if __name__ == "__main__":
    evalute_example()
    improve_example()
