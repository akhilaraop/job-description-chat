import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import warnings


from dotenv import load_dotenv
load_dotenv()

# Load API keys
groq_api_key = os.getenv('GROQ_API_KEY')
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Streamlit app title
st.title('Job Description ChatBot')
st.subheader('Chat with your Job Description documents using Llama3 8B model')

# Initialize the ChatGroq LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Prompt template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question: {input}
    """
)

# Function to create vector embeddings
def vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state["vectors"] = None
        st.session_state.embeddings = st.session_state.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        st.session_state.loader = PyPDFDirectoryLoader("./job_descriptions")  # Data ingestion
        st.session_state.docs = st.session_state.loader.load()  # Document loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Chunk creation
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)  # Splitting
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)  # Vector store

# Streamlit input
prompt1 = st.text_input("Enter your question from Documents!!")

# Silence PyTorch class registration warnings as its relevant to only custon extensions
warnings.filterwarnings("ignore", message=".*torch.classes.*_path.*")

# Button to start vector embedding
if st.button("Document Embeddings"):
    vector_embeddings()
    st.write("Vector Store DB is Ready!!")

# Document retrieval and response generation
if prompt1:
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        st.warning("Please click 'Document Embeddings' first to prepare the data.")
    else:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = st.session_state.vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        # Measure response time
        import time
        start = time.process_time()
        response = retrieval_chain.invoke({'input': prompt1})
        st.write(f"Response time: {time.process_time() - start:.2f} seconds")
        st.write(response['answer'])

        # Display document similarity search results
        with st.expander("Document similarity search"):
            for i, doc in enumerate(response["context"]):
                st.write(doc.page_content)
                st.write("--------------------------------")
