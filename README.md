# Job Description Chat Application

This repository contains a Streamlit application for job description analysis using GROQ API.

## Prerequisites

- Docker installed on your system
- GROQ API key

## Docker Setup

1. Clone the repository:
```bash
git clone https://github.com/akhilaraop/job-description-chat.git
cd job-description-chat
```

2. Create a `.env` file in the root directory with your GROQ API key:
```
GROQ_API_KEY=your_api_key_here
```

3. Build the Docker image:
```bash
docker build -t job-description-chat .
```

4. Run the container:
```bash
docker run -p 8501:8501 --env-file .env job-description-chat
```

The application will be available at `http://localhost:8501`

## Running Tests in Docker

To run tests in the Docker container:

```bash
# Build the test image
docker build -t job-description-chat-tests .

# Run all tests
docker run job-description-chat-tests python -m pytest

# Run specific tests
docker run job-description-chat-tests python -m pytest tests/test_main.py
```

## Project Structure

```
job-description-chat/
├── Dockerfile
├── .dockerignore
├── .env
├── main.py
├── requirements.txt
├── rag_app/
│   └── ...
├── tests/
│   └── ...
├── job_descriptions/
│   └── ...
└── documents/
    └── ...
```

## Notes
- Keep your `.env` file secure and never commit it to version control
- For production deployment, consider using Docker secrets or environment variables passed at runtime instead of copying the .env file

# Job Description ChatBot

Chat with your documents using the power of **Llama3-8B** and **Groq**! 
This Streamlit app lets you upload PDFs, converts them into embeddings with HuggingFace, and retrieves smart, contextual answers at lightning speed.

## Features

- PDF document processing and embedding
- Context-aware question answering
- Similarity search results display
- Streamlit-based user interface
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
