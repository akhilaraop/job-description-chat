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

    RAGApp --> DocumentProcessor : uses
    RAGApp --> RAGModel : uses
    DocumentProcessor --> FAISS : creates
    RAGModel --> ChatGroq : uses
