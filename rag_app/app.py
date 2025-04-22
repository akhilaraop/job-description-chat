"""Streamlit application for the RAG system.

This module implements the main Streamlit application for the RAG (Retrieval-Augmented Generation)
system. It provides a user interface for interacting with job description documents
using the Llama3 8B model through Groq's API.
"""
import os
import time
import warnings
import torch
import logging
from typing import Optional, List, Dict, Any

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from rag_app.document_processor import DocumentProcessor
from rag_app.rag_model import RAGModel
from rag_app.config.loader import load_config, setup_logging

# Load configuration and setup logging
config = load_config()
setup_logging(config)
logger = logging.getLogger(__name__)


class RAGApp:
    """Main application class for the RAG system.
    
    This class handles the Streamlit UI, document processing, and interaction
    with the RAG model. It manages the application state and user interactions.
    """

    def __init__(self) -> None:
        """Initialize the RAGApp with the Groq API key and other configurations.
        
        Raises:
            ValueError: If GROQ_API_KEY is not set in environment variables.
        """
        logger.info("Initializing RAGApp")
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY is not set in environment variables")
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        
        # Fix PyTorch classes warning
        logger.info("Configuring PyTorch settings")
        torch.classes.__path__ = []
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        warnings.filterwarnings("ignore", message=".*torch.classes.*_path.*")

        logger.info("Initializing DocumentProcessor")
        self.processor = DocumentProcessor()
        logger.info("Initializing RAGModel")
        self.model = RAGModel(self.api_key)
        self.vectorstore = None
        logger.info("RAGApp initialization complete")

    def load_styles(self) -> None:
        """Load custom CSS styles for the Streamlit app.
        
        Loads and applies custom CSS styles from the assets directory.
        The styles are applied to the entire Streamlit application.
        """
        logger.info("Loading custom CSS styles")
        css_path = os.path.join(os.path.dirname(__file__), "..", config['app']['css_path'])
        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            logger.info("Custom CSS styles loaded successfully")
        else:
            logger.warning(f"CSS file not found at {css_path}")

    def setup_sidebar(self) -> None:
        """Setup the sidebar with instructions and branding."""
        logger.info("Setting up sidebar")
        app_config = config['app']
        
        st.sidebar.title(app_config['title'])
        logo_path = os.path.join(os.path.dirname(__file__), "..", app_config['logo_path'])
        if os.path.exists(logo_path):
            st.sidebar.image(Image.open(logo_path), width=app_config['ui']['sidebar_width'])
            logger.info("Logo loaded successfully")
        else:
            logger.warning(f"Logo file not found at {logo_path}")
        
        st.sidebar.markdown("## Instructions")
        for instruction in app_config['instructions']:
            st.sidebar.markdown(f"- {instruction}")
        
        st.sidebar.markdown("## About")
        st.sidebar.markdown(app_config['about'])
        logger.info("Sidebar setup complete")

    def prepare_vectorstore(self) -> None:
        """Embed and cache documents.
        
        Loads documents, creates embeddings, and stores them in a vector store.
        The vector store is cached in the Streamlit session state for subsequent queries.
        """
        logger.info("Preparing vector store")
        if "vectorstore" in st.session_state:
            logger.info("Vector store already exists in session state")
            st.warning("Vector Store DB is already prepared. Please ask your questions.")
        else:
            logger.info("Starting document embedding process")
            st.info("Preparing Document Embeddings. Please wait...")
            with st.spinner("Loading and embedding documents..."):
                self.vectorstore = self.processor.load_and_embed()
                st.session_state["vectorstore"] = self.vectorstore
                logger.info("Documents loaded and embedded successfully")
                st.success("Documents loaded and embedded successfully!")

    def query_documents(self, prompt: str) -> None:
        """Run query against the vector store.
        
        Args:
            prompt: The user's question or query string.
            
        Note:
            This method requires the vector store to be prepared first using prepare_vectorstore().
        """
        logger.info(f"Processing query: {prompt}")
        if "vectorstore" not in st.session_state:
            logger.warning("Vector store not prepared")
            st.warning("Please click 'Document Embeddings' first to prepare the data.")
            return

        try:
            logger.info("Creating retriever from vector store")
            retriever = st.session_state["vectorstore"].as_retriever()
            if retriever is None:
                logger.error("Failed to create retriever")
                st.error("Failed to create retriever. Please try preparing the documents again.")
                return

            st.info("Processing your query. Please wait...")
            start = time.process_time()
            logger.info("Getting response from model")

            response = self.model.get_response(retriever, prompt)
            if not response or "answer" not in response:
                logger.error("Failed to get response from model")
                st.error("Failed to get response from the model. Please try again.")
                return

            response_time = time.process_time() - start
            logger.info(f"Query processed successfully in {response_time:.2f} seconds")
            st.success("Query processed successfully!")
            st.write("### Response:")
            st.write(f"Response time: {response_time:.2f} seconds")
            st.write(response["answer"])

            self.display_similarity_results(response.get("context", []))

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            st.error(f"An error occurred while processing your query: {str(e)}")
            st.info("Please try preparing the documents again or check your internet connection.")

    def display_similarity_results(self, context_docs: List[Any]) -> None:
        """Display document context from similarity search.
        
        Args:
            context_docs: List of document chunks that were found to be relevant to the query.
        """
        logger.info(f"Displaying similarity results for {len(context_docs)} documents")
        st.write("### Document Similarity Search Results:")
        if context_docs:
            with st.expander("Document similarity search"):
                for doc in context_docs:
                    st.write(doc.page_content)
                    st.write("--------------------------------")
        else:
            logger.info("No relevant documents found")
            st.write("No relevant documents found.")

    def display_main_ui(self) -> Optional[str]:
        """Display main header and prompt box.
        
        Returns:
            Optional[str]: The user's input text if provided, None otherwise.
        """
        logger.info("Displaying main UI")
        ui_config = config['app']['ui']
        st.subheader(ui_config['main_header'])
        return st.text_input(ui_config['input_label'])

    def handle_user_input(self, prompt: Optional[str]) -> None:
        """Handle the document embedding and query interaction.
        
        Args:
            prompt: The user's input text, if any.
        """
        if st.button(config['app']['ui']['button_text']):
            logger.info("Document Embeddings button clicked")
            self.prepare_vectorstore()

        if prompt:
            logger.info(f"Handling user input: {prompt}")
            self.query_documents(prompt)

    def run(self) -> None:
        """Run the Streamlit application.
        
        This is the main entry point for the application. It sets up the UI
        and handles the main application loop.
        """
        logger.info("Starting RAGApp")
        self.load_styles()
        self.setup_sidebar()

        prompt = self.display_main_ui()
        self.handle_user_input(prompt)
        logger.info("RAGApp running")
