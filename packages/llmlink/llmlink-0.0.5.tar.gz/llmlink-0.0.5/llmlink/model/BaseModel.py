class BaseModel:
    """
    Base model to extend when creating custom models for Chainlink

    To ensure interoperability with LLMLink applications, ensure that the `run` method is
    overwritten. The method should accept one single string parameter and return a string
    """

    def run(self):
        raise NotImplemented
