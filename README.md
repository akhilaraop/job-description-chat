

# 💬 job-description-chat-bot

Chat with your documents using the power of **Llama3-8B** and **Groq**! 
This Streamlit app lets you upload PDFs, converts them into embeddings with HuggingFace, and retrieves smart, contextual answers at lightning speed.

##  Features

- Upload and process PDF job descriptions
- Smart document embedding using HuggingFace
- Fast similarity search with FAISS
- Intelligent answers powered by Llama3-8B and Groq
- User-friendly Streamlit interface

##  Requirements

- Python 3.x
- Streamlit – for the web UI
- Langchain - to chain together the retrieval and LLM calls 
- HuggingFace Embeddings – for document vectorization
- FAISS – for efficient similarity search
- Groq + Llama3-8B – for fast, powerful natural language answers
- PyPDFDirectoryLoader – to load PDFs from a directory

## Getting Started

### Environment Setup
Before running the app, make sure to set up your environment variables:
1. Create a `.env` file in the root directory
2. Add your GROQ_API_KEY:
   ```bash
   GROQ_API_KEY=<your_groq_api_key>
   ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/akhilaraop/job-description-chat.git
   cd job-description-chat-bot
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open the app in your browser (usually at http://localhost:8501)


## 🔍 Functionality

- **Document Ingestion**: Upload your PDF job descriptions to be processed by the system
- **Smart Embedding**: Documents are automatically processed and embedded using state-of-the-art HuggingFace models
- **Efficient Retrieval**: FAISS vector database enables lightning-fast similarity search
- **Intelligent Q&A**: Ask questions about your job descriptions and get contextual answers powered by Llama3-8B
- **Real-time Processing**: Get instant responses with Groq's high-performance infrastructure

## 🔁 How It Works (Data Flow)

```text
        ┌─────────────────────────────┐
        │      Start Streamlit App    │
        └────────────┬────────────────┘
                     │
                     ▼
        ┌─────────────────────────────┐
        │ Display UI Title & Prompt   │
        └────────────┬────────────────┘
                     │
                     ▼
     ┌─────────────────────────────────────┐
     │  [Button Click] "Document Embeddings"│
     └────────────────┬────────────────────┘
                      │
                      ▼
     ┌─────────────────────────────────────┐
     │ Load PDFs from "./us_census" folder │
     ├─────────────────────────────────────┤
     │ Split documents into chunks         │
     ├─────────────────────────────────────┤
     │ Create embeddings using HuggingFace │
     ├─────────────────────────────────────┤
     │ Store in FAISS vector DB            │
     └────────────────┬────────────────────┘
                      │
                      ▼
     ┌─────────────────────────────────────┐
     │ [User Input] Enter a question       │
     └────────────────┬────────────────────┘
                      │
                      ▼
     ┌─────────────────────────────────────┐
     │ Retrieve relevant chunks from FAISS │
     ├─────────────────────────────────────┤
     │ Pass context + question to Llama3   │
     ├─────────────────────────────────────┤
     │ Generate answer via ChatGroq        │
     └────────────────┬────────────────────┘
                      │
                      ▼
     ┌─────────────────────────────────────┐
     │ Display answer + response time      │
     ├─────────────────────────────────────┤
     │ Show documents used (if expanded)   │
     └─────────────────────────────────────┘
