import pytest
from unittest.mock import patch, MagicMock
from rag_app.app import RAGApp


@pytest.fixture
def mock_env(monkeypatch):
    '''
    
    '''
    monkeypatch.setenv("GROQ_API_KEY", "fake-key")


@pytest.fixture
def app(mock_env):
    return RAGApp()


def test_initialization_sets_up_dependencies(app):
    '''
    Test that the app initializes dependencies correctly
    '''
    assert app.processor is not None
    assert app.model is not None
    assert app.api_key == "fake-key"



    


def test_query_documents_with_context(monkeypatch, app):
    '''
    Test that the query documents method works with context
    '''
    mock_retriever = MagicMock()
    mock_response = {
        "answer": "This is a test answer.",
        "context": [MagicMock(page_content="Page 1 content"), MagicMock(page_content="Page 2 content")]
    }

    # Mock vectorstore and its retriever
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.return_value = mock_retriever
    app.model.get_response = MagicMock(return_value=mock_response)

    monkeypatch.setitem(__import__("streamlit").session_state, "vectorstore", mock_vectorstore)

    # Run query_documents
    app.query_documents("What is the purpose?")

    # Assert response was processed
    app.model.get_response.assert_called_once_with(mock_retriever, "What is the purpose?")



