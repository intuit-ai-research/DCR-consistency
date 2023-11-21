from typing import Dict

from dcr.inputs.input import Input


class RAISummaryInput(Input):
    def __init__(self, raw_input: Dict):
        super().__init__(raw_input)

        article = raw_input.get("article")
        sentences = raw_input.get("sentences")

        if not (article and sentences):
            raise ValueError("Invalid input: {article} and {sentences} are required")

        self.data = self.data | {
            "article": article,
            "sentences": sentences,
        }
