from typing import Literal
from langchain.schema.document import Document
from langchain.schema.vectorstore import VectorStoreRetriever
from abc import ABC, abstractmethod

class BaseService(ABC):

    @abstractmethod
    def __init__(self, model:str, api_key:str, types:Literal['ollama','openai']='ollama', embedding_model:str|None=None,**kwargs):
        pass

    @abstractmethod
    def Chat(self, prompt: str,**kwargs) -> str:
        pass

    @abstractmethod
    def RAG(self, query: str, context:str)-> str:
        pass
    @abstractmethod
    def Summarize_text(self, text:str, **kwargs)-> VectorStoreRetriever:
        pass

    @abstractmethod
    def Summarize_document(self, document: list[Document], **kwargs) -> VectorStoreRetriever:
        pass

    @abstractmethod
    def FileLoader(self, fileOrDirName:str, mode:Literal['Dir','file']='file',**kwargs) -> dict[str,list[Document]]:
        pass