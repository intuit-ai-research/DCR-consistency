from typing import Dict


class Input:
    def __init__(self, raw_input: Dict):
        id = raw_input.get("id")
        if id is None:
            raise ValueError("Invalid input: {id} is required")

        self.data = {
            "id": id,
        }

    def get_data(self):
        return self.data
