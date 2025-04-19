# job-description-chat-bot

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
   streamlit run main.py
   ```
4. Open the app in your browser (usually at http://localhost:8501)

## Testing

The project includes unit tests to ensure functionality. To run the tests:

1. Make sure you're in the virtual environment:
   ```bash
   source venv310/bin/activate
   ```

2. Run all tests:
   ```bash
   python -m pytest tests/
   ```

3. For verbose output:
   ```bash
   python -m pytest tests/ -v
   ```

4. To run a specific test file:
   ```bash
   python -m pytest tests/test_app.py
   ```

The test suite includes:
- App initialization tests
- Document processing tests
- Query handling tests
- Context retrieval tests

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
     │ Load PDFs from "./job_descriptions" folder │
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
```

## Architecture

### Class Diagram
See [class_diagram.md](assets/class_diagram.md) for the detailed class diagram of the application.

### Information Flow

1. **Application Initialization**:
   - `main.py` creates an instance of `RAGApp`
   - `RAGApp` initializes `DocumentProcessor` and `RAGModel`
   - Environment variables are loaded and validated

2. **Document Processing Flow**:
   ```
   User clicks "Document Embeddings" 
   → RAGApp.prepare_vectorstore() 
   → DocumentProcessor.load_and_embed() 
   → Documents are loaded, split, and embedded 
   → FAISS vector store is created and cached
   ```

3. **Query Processing Flow**:
   ```
   User enters question 
   → RAGApp.handle_user_input() 
   → RAGApp.query_documents() 
   → RAGModel.get_response() 
   → Retrieval chain processes query 
   → Response is displayed with context
   ```

## Components

### RAGApp
The main application class that handles the Streamlit UI and coordinates between document processing and query handling.

### DocumentProcessor
Responsible for:
- Loading PDF documents from the specified directory
- Splitting documents into chunks
- Creating embeddings using HuggingFace's all-MiniLM-L6-v2 model
- Building and returning a FAISS vector store

### RAGModel
Handles the interaction with the Llama3 8B model through Groq's API:
- Initializes the language model with the Groq API key
- Creates a prompt template for context-aware responses
- Processes queries using a retrieval chain

## Dependencies

- Python 3.10+
- Streamlit
- LangChain
- FAISS
- HuggingFace Transformers
- Groq API

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   ```bash
   export GROQ_API_KEY="your-api-key"
   ```
4. Place your PDF documents in the `job_descriptions` directory
5. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Click the "Document Embeddings" button to process your documents
2. Enter your question in the text input field
3. View the response and relevant document context

## Features

- PDF document processing and embedding
- Context-aware question answering
- Similarity search results display
- Streamlit-based user interface
- Performance metrics display
