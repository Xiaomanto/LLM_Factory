from typing import Literal
from langchain.schema.document import Document
from langchain.schema.vectorstore import VectorStoreRetriever
from langchain_community.document_loaders import PyPDFLoader,CSVLoader,TextLoader,Docx2txtLoader,UnstructuredExcelLoader
from langchain_ollama import OllamaLLM
from langchain.text_splitter import TokenTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from chatModelService.BaseService import BaseService
import os

class OllamaService(BaseService):
    def __init__(self, model:str, api_key:str, embedding_model:str|None=None,**kwargs):
        """
            ## 其他參數：
             - base_url: str
        """
        self.llm = OllamaLLM(model=model, **kwargs)
        if embedding_model:
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    def Chat(self, prompt: str,**kwargs) -> str:
        template = """
        請根據提問的語言來回應問題。若沒有context，你可以用你既有的資料來回應問題。
            Question: {question}

            context: {context}
        """
        context = kwargs.get("context","No context")
        query = ChatPromptTemplate.from_template(template)
        llm = query | self.llm
        return llm.invoke({'question': prompt,"context":context})
    
    def RAG(self, query: str, context:str)-> str:
        return self.Chat(query, context)

    
    def Summarize_text(self, text:str, **kwargs)-> VectorStoreRetriever:
        """
        ### 可用參數
            
            search_kwargs={"k": number}
            可設定最大檢索數量

            chunk_size= number
            可設定切塊大小

            chunk_overlap= number
            可設定每個塊的重疊大小
        """
        spliter = TokenTextSplitter(**kwargs)
        doc = spliter.split_text(text=text)
        vecstore = FAISS.from_texts(texts=doc,embedding=self.embeddings)
        return vecstore.as_retriever(kwargs)

    
    def Summarize_document(self, document: list[Document], **kwargs) -> VectorStoreRetriever:
        """
        ### 可用參數
            
            search_kwargs={"k": number}
            可設定最大檢索數量

            chunk_size= number
            可設定切塊大小

            chunk_overlap= number
            可設定每個塊的重疊大小
        """
        spliter = TokenTextSplitter(**kwargs)
        doc = spliter.split_documents(document)
        vecstore = FAISS.from_documents(doc, self.embeddings)
        return vecstore.as_retriever(**kwargs)

    
    def FileLoader(self, fileOrDirName:str, mode:Literal['Dir','file']='file',**kwargs) -> dict[str,list[Document]]:
        """
            用於讀取[pdf,docx,txt,csv,excel]類型的文件，並回傳一個字典，key預設為文件名稱

            fileOrDirName: 為文件路徑或資料夾路徑，文件須包含副檔名

            mode: 讀取模式，'Dir'表示讀取資料夾，'file'表示讀取單個文件
        """
        self.encoding = kwargs.get('encoding', 'utf-8')
        if mode == 'file':
            if ".txt" in fileOrDirName:
                return {fileOrDirName:TextLoader(fileOrDirName,encoding=self.encoding).load()}
            if ".pdf" in fileOrDirName:
                return {fileOrDirName:PyPDFLoader(fileOrDirName).load()}
            if ".docx" in fileOrDirName:
                return {fileOrDirName:Docx2txtLoader(fileOrDirName).load()}
            if ".csv" in fileOrDirName:
                return {fileOrDirName:CSVLoader(fileOrDirName,encoding=self.encoding).load()}
            if ".xlsx" in fileOrDirName:
                return {fileOrDirName:UnstructuredExcelLoader(fileOrDirName).load()}
            raise ValueError("Unsupported file type")
        else:
            result = {}
            for file in os.listdir(fileOrDirName):
                if ".txt" in fileOrDirName:
                    result[file] = TextLoader(fileOrDirName,encoding=self.encoding).load()
                if ".pdf" in fileOrDirName:
                    result[file] = PyPDFLoader(fileOrDirName).load()
                if ".docx" in fileOrDirName:
                    result[file] = Docx2txtLoader(fileOrDirName).load()
                if ".csv" in fileOrDirName:
                    result[file] = CSVLoader(fileOrDirName,encoding=self.encoding).load()
                if ".xlsx" in fileOrDirName:
                    result[file] = UnstructuredExcelLoader(fileOrDirName).load()
            if not result:
                raise ValueError("No supported file types found in the directory.")
            return result

