import pytest
from unittest.mock import patch, MagicMock
from rag_app.app import RAGApp


@pytest.fixture
def mock_env(monkeypatch):
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


def test_query_documents_no_vectorstore(monkeypatch, app):
    '''
    Test that query_documents handles missing vectorstore gracefully
    '''
    # Ensure vectorstore is not in session state
    if "vectorstore" in __import__("streamlit").session_state:
        monkeypatch.delitem(__import__("streamlit").session_state, "vectorstore")

    # Mock st.warning to verify it's called
    with patch("streamlit.warning") as mock_warning:
        app.query_documents("Test query")
        mock_warning.assert_called_once_with("Please click 'Document Embeddings' first to prepare the data.")


def test_query_documents_retriever_failure(monkeypatch, app):
    '''
    Test that query_documents handles retriever creation failure
    '''
    # Mock vectorstore that returns None for retriever
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.return_value = None
    monkeypatch.setitem(__import__("streamlit").session_state, "vectorstore", mock_vectorstore)

    # Mock st.error to verify it's called
    with patch("streamlit.error") as mock_error:
        app.query_documents("Test query")
        mock_error.assert_called_once_with("Failed to create retriever. Please try preparing the documents again.")


def test_query_documents_model_failure(monkeypatch, app):
    '''
    Test that query_documents handles model response failure
    '''
    mock_retriever = MagicMock()
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.return_value = mock_retriever
    monkeypatch.setitem(__import__("streamlit").session_state, "vectorstore", mock_vectorstore)

    # Mock model to return invalid response
    app.model.get_response = MagicMock(return_value={})

    # Mock st.error to verify it's called
    with patch("streamlit.error") as mock_error:
        app.query_documents("Test query")
        mock_error.assert_called_once_with("Failed to get response from the model. Please try again.")


def test_query_documents_exception_handling(monkeypatch, app):
    '''
    Test that query_documents handles unexpected exceptions
    '''
    mock_vectorstore = MagicMock()
    mock_vectorstore.as_retriever.side_effect = Exception("Test exception")
    monkeypatch.setitem(__import__("streamlit").session_state, "vectorstore", mock_vectorstore)

    # Mock st.error and st.info to verify they're called
    with patch("streamlit.error") as mock_error, patch("streamlit.info") as mock_info:
        app.query_documents("Test query")
        mock_error.assert_called_once_with("An error occurred while processing your query: Test exception")
        mock_info.assert_called_once_with("Please try preparing the documents again or check your internet connection.")



