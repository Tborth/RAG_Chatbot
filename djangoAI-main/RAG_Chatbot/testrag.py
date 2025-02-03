from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch
from .models import ChatbotInteraction

class UploadQueryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('upload_query')
        self.test_file = SimpleUploadedFile("test.txt", b"Hello, world!")
        
    @patch('RAG_Chatbot.views.create_vector_db')
    @patch('RAG_Chatbot.views.create_chroma_vector_db')
    @patch('RAG_Chatbot.views.final_result_faiss')
    @patch('RAG_Chatbot.views.final_result_faiss_openai')
    @patch('RAG_Chatbot.views.final_result_chroma')
    @patch('RAG_Chatbot.views.final_result_chroma_openai')
    @patch('RAG_Chatbot.views.document_to_dict', side_effect=lambda x: x)
    def test_upload_file_faiss_gemini(self, mock_doc_dict, mock_chroma_openai, mock_chroma, mock_faiss_openai, mock_faiss, mock_create_chroma, mock_create_faiss):
        """Test file upload with FAISS and Gemini model."""
        mock_create_faiss.return_value = {'status': 'success'}
        mock_faiss.return_value = "Gemini response"
        
        response = self.client.post(self.url, {
            'file': self.test_file,
            'db_type': 'faiss',
            'query': 'Test query',
            'model_choice': 'Gemini'
        }, format='multipart')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gemini response")
        self.assertTrue(ChatbotInteraction.objects.filter(file_name="test.txt").exists())

    @patch('RAG_Chatbot.views.create_vector_db')
    @patch('RAG_Chatbot.views.create_chroma_vector_db')
    @patch('RAG_Chatbot.views.final_result_faiss')
    @patch('RAG_Chatbot.views.final_result_faiss_openai')
    @patch('RAG_Chatbot.views.final_result_chroma')
    @patch('RAG_Chatbot.views.final_result_chroma_openai')
    @patch('RAG_Chatbot.views.document_to_dict', side_effect=lambda x: x)
    def test_upload_file_chromadb_openai(self, mock_doc_dict, mock_chroma_openai, mock_chroma, mock_faiss_openai, mock_faiss, mock_create_chroma, mock_create_faiss):
        """Test file upload with ChromaDB and OpenAI model."""
        mock_create_chroma.return_value = {'status': 'success'}
        mock_chroma_openai.return_value = "OpenAI response"
        
        response = self.client.post(self.url, {
            'file': self.test_file,
            'db_type': 'chromadb',
            'query': 'Test query',
            'model_choice': 'openai'
        }, format='multipart')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OpenAI response")
        self.assertTrue(ChatbotInteraction.objects.filter(file_name="test.txt").exists())

    def test_upload_get_request(self):
        """Test GET request returns the upload form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'RAG_Chatbot/upload_query.html')
