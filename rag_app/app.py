import streamlit as st
import os
import warnings
from dotenv import load_dotenv
from rag_app.document_processor import DocumentProcessor
from rag_app.rag_model import RAGModel
import time
from PIL import Image

class RAGApp:
    def __init__(self):
        '''
        Initialize the RAGApp with the Groq API key and other configurations.
        '''
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        warnings.filterwarnings("ignore", message=".*torch.classes.*_path.*")
        
        self.processor = DocumentProcessor()
        self.model = RAGModel(self.api_key)
        self.vectorstore = None

    def load_styles(self):
        '''
        Load custom CSS styles for the Streamlit app.
        '''
        css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def setup_sidebar(self, logo_path):
        '''
        Setup the sidebar with instructions and branding.
        '''
        st.sidebar.title("Job Description ChatBot")
        if os.path.exists(logo_path):
            st.sidebar.image(Image.open(logo_path), width=200)
        st.sidebar.markdown("## Instructions")
        st.sidebar.markdown("1. Click on 'Document Embeddings' to prepare the data.")
        st.sidebar.markdown("2. Ask questions related to your documents.")
        st.sidebar.markdown("## About")
        st.sidebar.markdown("This app uses Llama3 8B model to answer questions based on your Job Description documents.")

    def prepare_vectorstore(self):
        '''
        Embed and cache documents.
        '''
        if "vectorstore" in st.session_state:
            st.warning("Vector Store DB is already prepared. Please ask your questions.")
        else:
            st.info("Preparing Document Embeddings. Please wait...")
            with st.spinner("Loading and embedding documents..."):
                self.vectorstore = self.processor.load_and_embed()
                st.session_state["vectorstore"] = self.vectorstore
                st.success("Documents loaded and embedded successfully!")

    def query_documents(self, prompt):
        '''
        Run query against the vector store.
        '''
        if "vectorstore" not in st.session_state:
            st.warning("Please click 'Document Embeddings' first to prepare the data.")
            return

        retriever = st.session_state["vectorstore"].as_retriever()

        st.info("Processing your query. Please wait...")
        start = time.process_time()

        response = self.model.get_response(retriever, prompt)

        st.success("Query processed successfully!")
        st.write("### Response:")
        st.write(f"Response time: {time.process_time() - start:.2f} seconds")
        st.write(response['answer'])

        self.display_similarity_results(response['context'])

    def display_similarity_results(self, context_docs):
        '''
        Display document context from similarity search.
        '''
        st.write("### Document Similarity Search Results:")
        if context_docs:
            with st.expander("Document similarity search"):
                for doc in context_docs:
                    st.write(doc.page_content)
                    st.write("--------------------------------")
        else:
            st.write("No relevant documents found.")

    def display_main_ui(self):
        '''
        Display main header and prompt box.
        '''
        st.subheader("Chat with your Job Description documents using Llama3 8B")
        return st.text_input("Enter your question from Documents!!")

    def handle_user_input(self, prompt):
        '''
        Handle the document embedding and query interaction.
        '''
        if st.button("Document Embeddings"):
            self.prepare_vectorstore()

        if prompt:
            self.query_documents(prompt)

    def run(self):
        '''
        Run the Streamlit application.
        '''
        self.load_styles()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "jd_chat_bot.png")
        self.setup_sidebar(logo_path)

        prompt = self.display_main_ui()
        self.handle_user_input(prompt)
