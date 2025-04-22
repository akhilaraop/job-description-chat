# Job Description Chat Application

Chat with your documents using the power of **Llama3-8B** and **Groq**! 
This Streamlit app lets you upload PDFs, converts them into embeddings with HuggingFace, and retrieves smart, contextual answers at lightning speed.

## Features

- PDF document processing and embedding
- Context-aware question answering
- Similarity search results display
- Streamlit-based user interface
- Performance metrics display
- Development mode with hot-reloading and test watching

## Prerequisites

- Docker and Docker Compose installed on your system
- GROQ API key (see instructions below)

### Getting a GROQ API Key

1. Go to [GROQ Console](https://console.groq.com/)
2. Sign up for an account if you don't have one
3. Once logged in, navigate to the API Keys section
4. Click "Create API Key"


## Development Setup

The project includes a development environment with hot-reloading and test watching capabilities.

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/akhilaraop/job-description-chat.git
cd job-description-chat
```
2. From the project directory, create a `.env` file with your GROQ API key created earlier
```bash
GROQ_API_KEY=your-api-key-here > .env
```

2. Start the development environment:
```bash
docker-compose -f docker-compose.dev.yml up
```

This will start two services:
- `streamlit-app`: The main application with hot-reloading enabled
- `test-watcher`: Automatically runs tests when Python files change

The application will be available at `http://localhost:8501`


## Production Setup

For production deployment:

1. Build the production image:
```bash
docker build -t job-description-chat .
```

2. Run the container:
```bash
docker run -p 8501:8501 --env-file .env job-description-chat
```

## Running Tests

### Using Docker Compose (Development)
Tests will automatically run when Python files change:
```bash
docker-compose -f docker-compose.dev.yml up test-watcher
```

### Manual Test Execution
To run tests manually:

```bash
# Run all tests
docker run job-description-chat-tests python -m pytest

# Run specific tests
docker run job-description-chat-tests python -m pytest tests/test_app.py
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

## Architecture

The system architecture is documented in two key diagrams:

1. **Class Diagram**: See [class_diagram.md](documents/class_diagram.md) for the detailed class relationships and interactions.
2. **System Design**: For comprehensive system design information, see [SYSTEM_DESIGN.md](documents/SYSTEM_DESIGN.md).

