"""RAG model implementation for the chat system."""
from typing import Any, Dict

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class RAGModel:
    """Handles the interaction with the Llama3-8B model through Groq's API."""

    def __init__(self, groq_api_key: str) -> None:
        """Initialize the RAGModel with the Groq API key.

        Args:
            groq_api_key: API key for the Groq service.
        """
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
        self.prompt = ChatPromptTemplate.from_template(
            """
            Answer the questions based on the provided context only.
            Please provide the most accurate response based on the question.
            <context>
            {context}
            <context>
            Question: {input}
            """
        )

    def get_response(self, retriever: Any, user_input: str) -> Dict[str, Any]:
        """Get the response from the model using the retriever and user input.

        Args:
            retriever: The document retriever to use.
            user_input: The user's question or input.

        Returns:
            Dictionary containing the model's response and context.
        """
        chain = create_retrieval_chain(
            retriever, create_stuff_documents_chain(self.llm, self.prompt)
        )
        return chain.invoke({"input": user_input})
