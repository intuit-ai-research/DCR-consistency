from abc import abstractmethod


class LLM:
    @abstractmethod
    def get_chat_response(self, prompt, times=0, **model_config) -> str:
        pass
