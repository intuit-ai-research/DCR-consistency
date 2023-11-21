from typing import Dict

from dcr.inputs.input import Input


class EvaluatorInput(Input):
    def __init__(self, raw_input: Dict):
        super().__init__(raw_input)

        reference = raw_input.get("reference")
        candidate = raw_input.get("candidate")

        if not (reference and candidate):
            raise ValueError("Invalid input: {reference} and {candidate} are required")

        self.data = self.data | {
            "reference": reference,
            "candidate": candidate,
        }
