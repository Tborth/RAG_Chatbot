from django.shortcuts import render
from .forms import TranslationForm
from langdetect import detect, DetectorFactory, LangDetectException
import langcodes
from langchain.prompts import PromptTemplate
import openai
from openai import OpenAI

from .llm import llm_gemini,llm_open_ai

DetectorFactory.seed = 0

# Prompt template for translation
prompt_template = PromptTemplate(
    input_variables=["text", "target_language"],
    template="""
    You are an expert translation AI tasked with accurately translating text while preserving the original meaning and tone.
    Do not add, omit, or modify any content beyond what is necessary for accurate translation. Provide only the translated text.
    
    Translate the following text to {target_language}:
    
    "{text}"
    
    Ensure the translation is precise, contextually appropriate, and captures the original nuances.
    """
)

def detect_language(text):
    try:
        lang_code = detect(text)
        language_name = langcodes.get(lang_code).language_name()
        return language_name
    except LangDetectException:
        return "Unknown"

def get_translation(text, target_language):
    try:
        # Generate prompt for translation
        prompt = prompt_template.format(text=text, target_language=target_language)
        response = llm_gemini().invoke(prompt).content
        return response
    except Exception as e:
        return f"Error during translation: {e}"


def get_translation_openai(text, target_language):
    try:
        openai.api_key = llm_open_ai()
        client = OpenAI(api_key=llm_open_ai())
        prompt = f"Translate the following text to {target_language}: {text}"
        response =  client.chat.completions.create(
            model="GPT-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        # Corrected return to access the content properly
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Translation Error: {type(e).__name__}: {e}"


def translate_text(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            target_language = form.cleaned_data['target_language']
            model_type = form.cleaned_data['model_choice']
            print("-----------------------------model_type",model_type)
            # openai_api_key = form.cleaned_data['openai_api_key']
            # print("-------------------------------api_key______________________",openai_api_key)

            detected_language = detect_language(text)

            if model_type == 'openai':
                translation = get_translation_openai(text, target_language)
                # print("---------------model type----->>>>>>>>>",model_type)
                # print("-------------------api_key-------------->>>>>>>>>>>",openai_api_key)
                # if not openai_api_key:
                #     form.add_error('api_key', 'API Key is required for the selected model.')
                #     return render(request, 'translator/translate.html', {'form': form})

                
            elif model_type == 'Gemini':
                translation = get_translation(text, target_language)
            else:
                translation = "Invalid model selection."

            return render(request, 'translator/translate.html', {
                'form': form,
                'detected_language': detected_language,
                'translation': translation
            })
    else:
        form = TranslationForm()

    return render(request, 'translator/translate.html', {'form': form})




