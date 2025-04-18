import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class DocumentProcessor:
    def __init__(self, path: str = "./job_descriptions"):
        '''
        Initialize the DocumentProcessor with the path to the directory containing PDF documents.
        '''
        self.path = path
        self.loader = PyPDFDirectoryLoader(self.path)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def load_and_embed(self):
        '''
        Load documents from the specified directory and create embeddings.
        '''
        # Load documents
        docs = self.loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        return vectorstore
