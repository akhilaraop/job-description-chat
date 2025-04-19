"""Document processing module for the RAG system."""
import os
from typing import Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class DocumentProcessor:
    """Handles document loading, splitting, and embedding."""

    def __init__(self, path: str = "./job_descriptions") -> None:
        """Initialize the DocumentProcessor with the path to the directory containing PDF documents.

        Args:
            path: Path to the directory containing PDF documents. Defaults to "./job_descriptions".
        """
        self.path = path
        self.loader = PyPDFDirectoryLoader(self.path)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def load_and_embed(self) -> Any:
        """Load documents from the specified directory and create embeddings.

        Returns:
            FAISS vector store containing the document embeddings.
        """
        # Load documents
        docs = self.loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        return vectorstore
