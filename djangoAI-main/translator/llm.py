from langchain_google_genai import ChatGoogleGenerativeAI
from RAG_Chatbot.models import EnvVariable
import logging

# Set up logging for better debugging
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
import os
# Initialize variables
OPENAI_API_KEY = None
GOOGLE_API_KEY = None
llm_gemini = None

load_dotenv() 

# # Exception handling for OPENAI API key
# try:
#     openai_api_key_record = EnvVariable.objects.filter(env_variable_name="OPENAI_API_KEY").first()
#     if openai_api_key_record:
#         OPENAI_API_KEY = openai_api_key_record.env_value
#     else:
#         logger.error("OpenAI API key not found in the database.")
# except Exception as e:
#     logger.error(f"Error fetching OpenAI API key: {e}")

# # Exception handling for GOOGLE API key
# try:
#     google_api_key_record = EnvVariable.objects.filter(env_variable_name="GOOGLE_API_KEY").first()
#     if google_api_key_record:
#         GOOGLE_API_KEY = google_api_key_record.env_value
#     else:
#         logger.error("Google API key not found in the database.")
# except Exception as e:
#     logger.error(f"Error fetching Google API key: {e}")

# Initialize llm_gemini with exception handling
def llm_gemini():
    try:
        google_api_key_record = EnvVariable.objects.filter(env_variable_name="GOOGLE_API_KEY").first()
        if google_api_key_record:
            GOOGLE_API_KEY = google_api_key_record.env_value
        else:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "GOOGLE_API_KEY")
            logger.error("Google API key not found in the database.")
    except Exception as e:
        logger.error(f"Error fetching Google API key: {e}")
 
    # Initialize llm_gemini with exception handling
    try:
        if GOOGLE_API_KEY:
            llm_gemini_obj = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                api_key=GOOGLE_API_KEY
            )
            return llm_gemini_obj
        else:
            logger.error("Google API key is missing. Cannot initialize llm_gemini.")
    except Exception as e:
        logger.error(f"Error initializing llm_gemini: {e}")

def llm_open_ai():
    try:
        openai_api_key_record = EnvVariable.objects.filter(env_variable_name="OPENAI_API_KEY").first()
        if openai_api_key_record:
            OPENAI_API_KEY = openai_api_key_record.env_value
        else:
            logger.error("OpenAI API key not found in the database.")
    except Exception as e:
        logger.error(f"Error fetching OpenAI API key: {e}")

    try:
        if OPENAI_API_KEY:
            return OPENAI_API_KEY
        else:
            logger.error("OPEN AI API key is missing.")
    except Exception as e:
        logger.error(f"Error initializing open_ai: {e}")




def google_gen_ai():
    """
    Initialize and return a Google Generative AI model using the API key retrieved from the database.
    """
    try:
        # Fetch the API key from the database
        google_api_key_record = EnvVariable.objects.filter(env_variable_name="GOOGLE_API_KEY").first()
        
        if google_api_key_record:
            google_api_key = google_api_key_record.env_value
        else:
            google_api_key = os.getenv("GOOGLE_API_KEY", "GOOGLE_API_KEY")
            logger.error("Google API key not found in the database.")
            return None  # Exit early if no API key is found

        # Configure the Google Generative AI library
        import google.generativeai as genai
        genai.configure(api_key=google_api_key)

        # Initialize the generative model
        try:
            llm_gemini_genai = genai.GenerativeModel("gemini-1.5-flash")
            return llm_gemini_genai
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {e}")
            return None  # Exit gracefully on failure to initialize the model

    except Exception as e:
        logger.error(f"Error fetching Google API key: {e}")
        return None  # Ensure the function always returns a predictable value


