from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

class RAGModel:
    def __init__(self, groq_api_key: str):
        '''
        Initialize the RAGModel with the Groq API key.
        '''
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")
        self.prompt = ChatPromptTemplate.from_template("""
            Answer the questions based on the provided context only.
            Please provide the most accurate response based on the question.
            <context>
            {context}
            <context>
            Question: {input}
        """)

    def get_response(self, retriever, user_input: str):
        '''
        Get the response from the model using the retriever and user input.
        '''
        chain = create_retrieval_chain(retriever, create_stuff_documents_chain(self.llm, self.prompt))
        return chain.invoke({'input': user_input})
