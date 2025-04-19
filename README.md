# Job Description ChatBot

Chat with your documents using the power of **Llama3-8B** and **Groq**! 
This Streamlit app lets you upload PDFs, converts them into embeddings with HuggingFace, and retrieves smart, contextual answers at lightning speed.

## Features

- PDF document processing and embedding
- Context-aware question answering
- Similarity search results display
- Streamlit-based user interface
- Performance metrics display

## Requirements

- Python 3.x
- Streamlit
- Langchain
- HuggingFace Embeddings
- FAISS
- Groq + Llama3-8B
- PyPDFDirectoryLoader

## Getting Started

### Environment Setup

1. Create and activate a Python virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```

2. Create a `.env` file in the root directory and add your GROQ_API_KEY:
   ```bash
   GROQ_API_KEY=<your_groq_api_key>
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akhilaraop/job-description-chat.git
   cd job-description-chat
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

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# For verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_app.py
```

## How It Works

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

1. **Document Processing**:
   - PDFs are loaded from the "./job_descriptions" folder
   - Documents are split into chunks
   - Embeddings are created using HuggingFace
   - Results are stored in FAISS vector database

2. **Query Processing**:
   - User enters a question
   - Relevant chunks are retrieved from FAISS
   - Context and question are passed to Llama3-8B
   - Response is generated via Groq
   - Answer and response time are displayed

## Architecture

The system architecture is documented in two key diagrams:

1. **Class Diagram**: See [class_diagram.md](documents/class_diagram.md) for the detailed class relationships and interactions.
2. **System Design**: For comprehensive system design information, see [SYSTEM_DESIGN.md](documents/SYSTEM_DESIGN.md).

### Main Components

- **RAGApp**: Main application class handling UI and coordination
- **DocumentProcessor**: Handles PDF loading, chunking, and embedding
- **RAGModel**: Manages interaction with Llama3-8B through Groq's API
