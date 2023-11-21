import json
from unittest.mock import Mock

import pytest

from dcr.improver import improve


class Test_Improver:
    def test_improver(self):
        rai_mock_data = [
            {
                "sentence": "original sentence",
                "improved_sentence": "improved sentence",
                "reason": "if it is improved, how it is improved. if not, say 'ALREADY CONSISTENT'",
            }
        ]

        mock_llm = Mock()
        mock_llm.get_chat_response.side_effect = [json.dumps(rai_mock_data)]

        data = [{"id": 1, "article": "this is good", "sentences": "this is bad"}]

        res = improve(mock_llm, {}, data)
        assert "improved sentence" in list(res["improved_version"])[0]

        # test_unhappy paths
        data2 = [{"article": "this is good", "sentences": "this is bad"}]
        data3 = [{"id": 1, "sentences": "this is bad"}]
        with pytest.raises(ValueError):
            improve(mock_llm, {}, data2)

        with pytest.raises(ValueError):
            improve(mock_llm, {}, data3)

        mock_llm.get_chat_response.side_effect = Exception("test")
        res = improve(mock_llm, {}, data)
        assert list(res["improved_version"])[0] == "-1"
