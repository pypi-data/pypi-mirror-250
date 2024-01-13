from cria_index.core import LLM

class OpenAI(LLM):
    @classmethod
    def class_name(cls):
        return "OpenAI"