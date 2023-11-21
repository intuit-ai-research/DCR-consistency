import json
from unittest.mock import Mock

import pytest

from dcr.components.dce_amc import DCE_AMC
from dcr.evaluator import evaluate


class Test_Evaluate:
    def test_evalaute(self):
        dce_mock_data = {
            "reason": [{"sentence": "test", "reason": "test reason"}],
            "is_consistent": True,
        }
        amc_mock_data = {
            "reason": [
                "The first paragraph is negative as it mentions the attempt answer is wrong. Thus mark -1",
                "The second paragraph is negative as it adds something that is not in true answer. Thus mark -1",
                "The third paragraph is positive. Thus mark +1",
            ],
            "answer": [-1, -1, 1],
        }

        mock_llm = Mock()
        mock_llm.get_chat_response.side_effect = [
            json.dumps(dce_mock_data),
            json.dumps(amc_mock_data),
        ]

        data = [{"id": 1, "reference": "this is good", "candidate": "this is bad"}]

        result = evaluate(mock_llm, {}, data)
        assert list(result["score"])[0] > 0.3
        assert list(result["decision"])[0] == True

        # test unhappy path
        data2 = [{"reference": "this is good", "candidate": "this is bad"}]
        data3 = [{"id": 1, "candidate": "this is bad"}]
        with pytest.raises(ValueError):
            evaluate(mock_llm, {}, data2)

        with pytest.raises(ValueError):
            evaluate(mock_llm, {}, data3)

        mock_llm.get_chat_response.side_effect = Exception("test")
        result = evaluate(mock_llm, {}, data)
        assert list(result["score"])[0] == DCE_AMC.ERROR_SCORE
