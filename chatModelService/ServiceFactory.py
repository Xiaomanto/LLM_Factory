from chatModelService.OllamaService import OllamaService
from chatModelService.OpenaiService import OpenaiService
from chatModelService.BaseService import BaseService
from typing import Literal

class ServiceFactory():

    def __init__(self) -> None:
        pass
    
    def getService(self, types:Literal['ollama','openai']='ollama',**kwargs) -> BaseService:
        """
        ## 必填參數：
            model: str,  # your llm model name
            api_key: str, # openai api key if you not use openai type you can enter "none" in here
        ## 可選參數：
            embedding_model: str | None = None # here is enter huggingdace_embedding model path only
            base_url: str = "http://localhost:11434" # if you use ollama type you can enter ollama base url in here
        """
        if not kwargs.get("model"):
            raise ValueError("model is not set")
        if not kwargs.get("api_key"):
            raise ValueError("api_key is not set")
        if types == 'ollama':
            return OllamaService(**kwargs)
        if types == 'openai':
            return OpenaiService(**kwargs)