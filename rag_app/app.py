import streamlit as st
import os
import warnings
from dotenv import load_dotenv
from rag_app.document_processor import DocumentProcessor
from rag_app.rag_model import RAGModel
import time
from PIL import Image

'''
RAGApp: A Streamlit application for querying job description documents using a RAG model.
This application allows users to load job description documents, create embeddings, and ask questions related to the documents.
It uses the Groq API for model inference and FAISS for vector storage.'''
# Load environment variables
load_dotenv()
# Load environment variables from .env file
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", message=".*torch.classes.*_path.*")

class RAGApp:
    def __init__(self):
        '''
        Initialize the RAGApp with the Groq API key and other configurations.
        '''
        self.processor = DocumentProcessor()
        self.model = RAGModel(groq_api_key)
        self.vectorstore = None

    def load_styles(self):
        '''
        Load custom CSS styles for the Streamlit app.'''
        css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def setup_sidebar(self, logo_path):
        '''
        Setup the sidebar with instructions and logo.
        '''
        st.sidebar.title("Job Description ChatBot")
        st.sidebar.image(Image.open(logo_path), width=200)
        st.sidebar.markdown("## Instructions")
        st.sidebar.markdown("1. Click on 'Document Embeddings' to prepare the data.")
        st.sidebar.markdown("2. Ask questions related to your documents.")
        st.sidebar.markdown("## About")
        st.sidebar.markdown("This app uses Llama3 8B model to answer questions based on your Job Description documents.")

    def handle_embedding(self):
        '''
        Handle the embedding process and store the vectorstore in session state.
        '''
        if "vectorstore" in st.session_state:
            st.warning("Vector Store DB is already prepared. Please ask your questions.")
            return
            
        st.info("Preparing Document Embeddings. Please wait...")
        with st.spinner("Loading and embedding documents..."):
            # Load and embed documents
            self.vectorstore = self.processor.load_and_embed()
            st.success("Documents loaded and embedded successfully!")
            

        st.session_state["vectorstore"] = self.vectorstore
       
    def handle_query(self, prompt):
        '''
        Handle the query process and display the response.
        '''
        if "vectorstore" not in st.session_state:
            st.warning("Please click 'Document Embeddings' first to prepare the data.")
            return
        
        
        retriever = st.session_state["vectorstore"].as_retriever()

        start = time.process_time()
        # Get the response from the model
        st.info("Processing your query. Please wait...")

        response = self.model.get_response(retriever, prompt)
        st.success("Query processed successfully!")
        # Display the response
        st.write("### Response:")
        # Display the response time
        st.write(f"Response time: {time.process_time() - start:.2f} seconds")
        st.write(response['answer'])
        # Display the document similarity search results
        st.write("### Document Similarity Search Results:")
        # Display the context from the response
        if response['context']:
            
            # Display each document's content
            
            with st.expander("Document similarity search"):
                for doc in response['context']:
                    st.write(doc.page_content)
                    st.write("--------------------------------")
        else:
            st.write("No relevant documents found.")
           


    def run(self):
        '''
        Run the Streamlit app.
        '''
        self.load_styles()

        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "jd_chat_bot.png")
        
        self.setup_sidebar(logo_path)

        st.subheader("Chat with your Job Description documents using Llama3 8B")
        prompt = st.text_input("Enter your question from Documents!!")

        if st.button("Document Embeddings"):
            self.handle_embedding()

        if prompt:
            self.handle_query(prompt)
