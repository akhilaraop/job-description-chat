# Job Description Chat Application

A Streamlit application for job description analysis using GROQ API and Llama3-8B.

## Quick Start

1. Clone the repo and create `.env` with your GROQ API key:
```bash
git clone https://github.com/akhilaraop/job-description-chat.git
cd job-description-chat
echo "GROQ_API_KEY=your_api_key_here" > .env
```

2. Run with Docker:
```bash
docker build -t job-description-chat .
docker run -p 8501:8501 --env-file .env job-description-chat
```

Access the app at `http://localhost:8501`

## Features

- Pre-loaded job descriptions from "./job_descriptions" folder
- Context-aware question answering using Llama3-8B
- Similarity search with FAISS vector database
- Performance metrics display

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

## Architecture

The application follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Document Processing**:
   - Load PDFs from "./job_descriptions"
   - Split into chunks and create embeddings
   - Store in FAISS vector database

2. **Query Processing**:
   - Retrieve relevant chunks from FAISS
   - Generate answers using Llama3-8B via Groq
   - Display results with response time

For detailed architecture, see:
- [Class Diagram](documents/class_diagram.md)
- [System Design](documents/SYSTEM_DESIGN.md)

## Testing

Run tests in Docker:
```bash
docker build -t job-description-chat-tests .
docker run job-description-chat-tests python -m pytest
```

## Security Note

Never commit `.env` files. For production, use Docker secrets or runtime environment variables.
