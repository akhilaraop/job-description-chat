```mermaid 
classDiagram
    class RAGApp {
        -api_key: str
        -processor: DocumentProcessor
        -model: RAGModel
        -vectorstore: FAISS
        -config: Dict[str, Any]
        +__init__()
        +load_styles()
        +setup_sidebar(logo_path: str)
        +prepare_vectorstore()
        +query_documents(prompt: str)
        +display_similarity_results(context_docs: List[Any])
        +display_main_ui() Optional[str]
        +handle_user_input(prompt: Optional[str])
        +run()
    }

    class DocumentProcessor {
        -path: str
        -loader: PyPDFDirectoryLoader
        -embeddings: HuggingFaceEmbeddings
        -config: Dict[str, Any]
        +__init__(path: str)
        +load_and_embed() FAISS
        +split_documents(documents) List[Document]
    }

    class RAGModel {
        -llm: ChatGroq
        -model_name: str = "llama3-8b-8192"
        -prompt: ChatPromptTemplate
        -config: Dict[str, Any]
        +__init__(groq_api_key: str)
        +get_response(retriever: Any, user_input: str) Dict[str, Any]
    }

    class ConfigLoader {
        +load_config(config_file: str) Dict[str, Any]
        +setup_logging(config: Dict[str, Any])
    }

    RAGApp --> DocumentProcessor : uses
    RAGApp --> RAGModel : uses
    RAGApp --> ConfigLoader : uses
    DocumentProcessor --> FAISS : creates
    DocumentProcessor --> ConfigLoader : uses
    RAGModel --> ChatGroq : uses
    RAGModel --> ConfigLoader : uses
