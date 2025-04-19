import unittest
from rag_app.document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        '''
        Initialize the test case with a DocumentProcessor instance.
        '''
        self.processor = DocumentProcessor()

    def test_embedding_generation(self):
        '''
        Test the embedding generation process.
        '''
        # Load and embed documents
        vectorstore = self.processor.load_and_embed()
        self.assertIsNotNone(vectorstore)
        self.assertTrue(hasattr(vectorstore, "similarity_search"))

