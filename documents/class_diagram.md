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
        +__init__(path: str)
        +load_and_embed() FAISS
    }

    class RAGModel {
        -llm: ChatGroq
        -prompt: ChatPromptTemplate
        +__init__(groq_api_key: str)
        +get_response(retriever, user_input: str) dict
    }

    class TestRAGApp {
        +test_initialization_sets_up_dependencies()
        +test_query_documents_with_context()
        +test_query_documents_no_vectorstore()
        +test_query_documents_retriever_failure()
        +test_query_documents_model_failure()
        +test_query_documents_exception_handling()
    }

    RAGApp --> DocumentProcessor : uses
    RAGApp --> RAGModel : uses
    DocumentProcessor --> FAISS : creates
    RAGModel --> ChatGroq : uses
    TestRAGApp ..> RAGApp : tests
