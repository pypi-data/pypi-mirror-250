from cria_index.core import LLM

class HuggingFaceLLM(LLM):
    @classmethod
    def class_name(cls):
        return "HuggingFaceLLM"