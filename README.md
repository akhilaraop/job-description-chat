# Job Description Chat Application

Chat with your documents using the power of **Llama3-8B** and **Groq**! 
This Streamlit app lets you upload PDFs, converts them into embeddings with HuggingFace, and retrieves smart, contextual answers at lightning speed.

## Features

- PDF document processing and embedding
- Context-aware question answering
- Similarity search results display
- Streamlit-based user interface
- Performance metrics display

## Prerequisites

- Docker installed on your system
- GROQ API key (see instructions below)

### Getting a GROQ API Key

1. Go to [GROQ Console](https://console.groq.com/)
2. Sign up for an account if you don't have one
3. Once logged in, navigate to the API Keys section
4. Click "Create API Key"
5. Copy the generated API key
6. Create a `.env` file in the project root and add:
```bash
   # Method 1: Using touch and then edit
   touch .env
   
   ```
7. Add the API key to the `.env` file:

```bash
   GROQ_API_KEY=your-api-key-here
   ```

## Docker Setup

1. Clone the repository:
```bash
git clone https://github.com/akhilaraop/job-description-chat.git
cd job-description-chat
```

2. Build the Docker image:
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

