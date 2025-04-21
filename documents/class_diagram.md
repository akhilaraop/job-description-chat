```mermaid 
classDiagram
    class RAGApp {
        -api_key: str
        -processor: DocumentProcessor
        -model: RAGModel
        -vectorstore: FAISS
        +__init__()
        +load_styles()
        +setup_sidebar()
        +prepare_vectorstore()
        +query_documents()
        +display_similarity_results()
        +display_main_ui()
        +handle_user_input()
        +run()
    }

    class DocumentProcessor {
        -path: str
        -loader: PyPDFDirectoryLoader
        -embeddings: HuggingFaceEmbeddings
        -chunk_size: int = 1000
        -chunk_overlap: int = 200
        +__init__(path: str)
        +load_and_embed() FAISS
        +split_documents(documents) List[Document]
    }

    class RAGModel {
        -llm: ChatGroq
        -model_name: str = "llama3-8b-8192"
        -prompt: ChatPromptTemplate
        -temperature: float = 0.7
        +__init__(groq_api_key: str)
        +get_response(retriever, user_input: str) dict
        +format_response(response: str, sources: List[str]) str
    }

    class TestRAGApp {
        +test_initialization_sets_up_dependencies()
        +test_query_documents_with_context()
        +test_query_documents_no_vectorstore()
        +test_query_documents_retriever_failure()
        +test_query_documents_model_failure()
        +test_query_documents_exception_handling()
        +test_display_similarity_results()
        +test_handle_user_input()
        +test_prepare_vectorstore()
    }

    RAGApp --> DocumentProcessor : uses
    RAGApp --> RAGModel : uses
    DocumentProcessor --> FAISS : creates
    RAGModel --> ChatGroq : uses
    TestRAGApp ..> RAGApp : tests
