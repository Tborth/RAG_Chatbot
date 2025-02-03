
User Guide for RAG (Retrieval-Augmented Generation) Project
![screenshot](djangoAI-main/images/screenshot1.png)
cd djangoAI-main

1. Setup and Configuration

Step 1: Add API Keys

Before starting, ensure you have set up the required API keys in your .env file.

1.1 Configure .env File

Create a .env file in your project directory and add the following:

GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

Replace your_google_api_key_here and your_openai_api_key_here with your actual API keys.

1.2 Install Required Dependencies

Ensure you have installed the required Python libraries:

pip install -r requirements.txt
please install requirements. txt file 

Then also run this line in terminal : pip install git+https://github.com/suno-ai/bark.git


2. Running the RAG System

Step 2: Start the Backend

Run the following command to start the FastAPI backend:

python3 manage.py runserver 0.0.0.0:8001 

This will start the API server at http://localhost:8001.

Step 3: Upload Documents
![screenshot](djangoAI-main/images/screenshot2.png)

Navigate to the /RAG_Chatbot endpoint for upload.

Upload a document (PDF, TXT, CSV, etc.).

The document will be processed and stored in the vector database (FAISS/ChromaDB).

Step 4: Querying the RAG System
![screenshot](djangoAI-main/images/screenshot3.png)
Use the /RAG_Chatbot/uploaded_query_view.

Provide a natural language query.

The system retrieves relevant documents and generates a response using LLM (e.g., OpenAI/Gemini).


3. Configuration Options

You can customize the retrieval and generation models in the config.py file:

VECTOR_DB = "faiss"  # Options: "faiss", "chromadb"
MODEL_TYPE = "openai"  # Options: "openai", "gemini"

