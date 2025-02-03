from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadQueryForm, vectorDBForm, MyForm ,ChatbotInteractionForm,EnvVariableForm,ChatbotInteractionNewForm
from .models import ChatbotInteraction, VectorStore,EnvVariable,ChatbotInteractionNew
from pathlib import Path
from django.contrib import messages
import os
from .vfaissdb import create_vector_db, final_result_faiss,final_result_faiss_openai
from .vchromadb_main import create_chroma_vector_db, final_result_chroma,final_result_chroma_openai
from django.shortcuts import get_object_or_404, redirect


# Define the upload directory
UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def document_to_dict(document):
    """Helper function to convert Document objects to dictionaries."""
    if isinstance(document, list):
        return [document_to_dict(doc) for doc in document]
    if hasattr(document, '__dict__'):
        return document.__dict__
    return str(document)  # Fallback to string representation if needed


def vectorstore_view(request):
    """View to manage the creation and listing of vector stores."""
    if request.method == 'POST':
        form = vectorDBForm(request.POST)
        if form.is_valid():
            vectordatabase = form.cleaned_data['vectorDatabase']
            exist = VectorStore.objects.filter(file_name=vectordatabase)
            
            # If the vector store doesn't exist, create a new one
            if not exist:
                interaction = VectorStore.objects.create(file_name=vectordatabase)
                VECTORDATABASE = Path(f"{vectordatabase}/")
                VECTORDATABASE.mkdir(parents=True, exist_ok=True)
            else:
                return render(request, 'vectorui/vectorstore.html', {
                    'form': form, "msg": "Vector store already exists."
                })
        
        records = VectorStore.objects.all()
        return render(request, 'vectorui/vectorstore.html', {
            'form': form, 'records': records
        })
    else:
        form = vectorDBForm()
        records = VectorStore.objects.all()
        return render(request, 'vectorui/vectorstore.html', {
            'form': form, 'records': records
        })




def upload_query_view(request):
    """Handle the uploading of files and querying vector stores (FAISS/ChromaDB)."""
    if request.method == 'POST':
        form = UploadQueryForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Extract form data
            file = form.cleaned_data['file']
            db_type = form.cleaned_data['db_type']
            print("============================== DB_TYPE============",db_type)
            query = form.cleaned_data['query']
            model_choice=form.cleaned_data['model_choice']
            print("################################ MODEL TYPE #################################", model_choice)
            filename = file.name
            
            # Save uploaded file to the correct directory
            subdir = UPLOAD_DIR / "others/"
            subdir.mkdir(parents=True, exist_ok=True)
            file_path = subdir / filename

            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # Vector DB creation based on selected type (FAISS or ChromaDB)
            if db_type == "faiss":
                res = create_vector_db(filename, f'vectorstore1/{filename}', 'uploads/others')
            elif db_type == "chromadb":
                res = create_chroma_vector_db(filename, f'vchromadb/chromavectorstore1/{filename}', 'uploads/others')

            # Handle the query if provided
            if query:
                if  model_choice=="Gemini" and db_type == "faiss":
                    DB_FAISS_PATH = f'vectorstore1/{filename}'
                    response = final_result_faiss(query, DB_FAISS_PATH)

                elif model_choice=="openai" and  db_type == "faiss" :
                       DB_FAISS_PATH = f'vectorstore1/{filename}'
                       response = final_result_faiss_openai(query,DB_FAISS_PATH)

                elif model_choice=="Gemini" and db_type == "chromadb":
                    DB_CHROMA_PATH = f'vchromadb/chromavectorstore1/{filename}'
                    response = final_result_chroma(query, DB_CHROMA_PATH)

                elif model_choice=="openai" and db_type == "chromadb":
                    DB_CHROMA_PATH = f'vchromadb/chromavectorstore1/{filename}'
                    response = final_result_chroma_openai(query, DB_CHROMA_PATH)

                # Save interaction to the database
                interaction = ChatbotInteraction.objects.create(
                    file_name=filename,
                    db_type=db_type,
                    query=query,
                    response=response if response else "No response generated"
                )

                # Convert results to JSON serializable format
                res_serialized = document_to_dict(res)
                response_serialized = document_to_dict(response)

                return render(request, 'vectorui/upload_query.html', {
                    'form': form,
                    'vector_result': res_serialized,
                    'query_response': response_serialized
                })

            # Ensure response is JSON serializable if no query
            res_serialized = document_to_dict(res)
            return render(request, 'vectorui/upload_query.html', {
                'form': form,
                'vector_result': res_serialized.get("query_response", "No response generated")
            })
    
    else:
        form = UploadQueryForm()

    return render(request, 'vectorui/upload_query.html', {'form': form})



##################################### ULOADED FILE QUERY VIEW ######################




def uploaded_query_view(request):
    if request.method == 'POST':
        form = ChatbotInteractionForm(request.POST)
        if form.is_valid():
            db_type = form.cleaned_data['db_type']
            vector_store = form.cleaned_data['vectorDB_field']
            vector_store1 =  vector_store
            query = form.cleaned_data['query']
            
            # Handle the query if provided
            if query:
                response = None  
                # Process query based on the database type and model choice
                if db_type == "faiss":
                         response = final_result_faiss(query, vector_store1)

                elif db_type == "chromadb":
                        response = final_result_chroma(query, vector_store1)
                    
            #     # Prepare response for the template
                response_serialized = response if isinstance(response, dict) else {"response": response}
                return render(
                    request, 
                    'vectorui/uploadedquery.html', 
                    {'form': form, 'query_response': response_serialized['response']}
                )

    else:
        form = ChatbotInteractionForm()

    return render(request, 'vectorui/uploadedquery.html', {'form': form})




def env_variable_view(request):
    if request.method == 'POST':
        form = EnvVariableForm(request.POST)
        if form.is_valid():
            env_variable_name = form.cleaned_data['env_variable_name']
            # Check if an entry with the same name already exists
            if EnvVariable.objects.filter(env_variable_name=env_variable_name).exists():
                messages.error(request, 'An environment variable with this name already exists.')
            else:
                form.save()
                messages.success(request, 'Environment variable added successfully.')
                return redirect('env_variable_form')  
    else:
        form = EnvVariableForm()

    env_variables = EnvVariable.objects.all()
    return render(request, 'vectorui/env_template.html', {'form': form, 'env_variables': env_variables})

def delete_env_variable(request, id):
    variable = get_object_or_404(EnvVariable, id=id)
    variable.delete()
    messages.success(request, 'Environment variable deleted successfully.')
    return redirect('env_variable_form')  





def upload_view(request):
    """View to handle file upload and database selection for FAISS or ChromaDB."""
    # Define directories for FAISS and ChromaDB vector stores
    faiss_dir = 'vectorstore1'
    chromadb_dir = 'vchromadb/chromavectorstore1'

    # Get available databases from these directories
    faiss_dbs = [f for f in os.listdir(faiss_dir) if os.path.isdir(os.path.join(faiss_dir, f))]
    chromadb_dbs = [f for f in os.listdir(chromadb_dir) if os.path.isdir(os.path.join(chromadb_dir, f))]
    
    form = MyForm(request.POST or None)
    
    # Provide dynamic choices for the db_type field (FAISS or ChromaDB)
    form.fields['db_type'].choices = [('faiss', 'FAISS'), ('chromadb', 'ChromaDB')]  
    
    if form.is_valid():
        db_type = form.cleaned_data.get('db_type')
        
        # Based on db_type, set the available vector store choices
        if db_type == 'faiss':
            form.fields['vectorstore'].choices = [(db, db) for db in faiss_dbs]
        elif db_type == 'chromadb':
            form.fields['vectorstore'].choices = [(db, db) for db in chromadb_dbs]
        
        vectorstore = form.cleaned_data.get('vectorstore')
        query = form.cleaned_data.get('query')
        
        # Handle the query and selected vector store logic
        if vectorstore and query:
            pass  # Logic for handling the query and vectorstore selection will go here
        
    return render(request, 'vectorui/my_template.html', {
        'form': form, 'faiss_dbs': faiss_dbs, 'chromadb_dbs': chromadb_dbs
    })





#######################################################  NEW UPLOADER THAT IS WORKING IN PROJECT #########################################################################

def upload_interaction_view(request):
    if request.method == 'POST':
        form = ChatbotInteractionNewForm(request.POST, request.FILES)
        if form.is_valid():
            model_type = form.cleaned_data['model_choice']
            file = form.cleaned_data['file_name']
            path = form.cleaned_data['file_type']
            db_type=form.cleaned_data['db_type']
            query=form.cleaned_data['query']
            filename = file.name
            
            ####### Save uploaded file to the correct directory
            subdir = UPLOAD_DIR / "others/"
            subdir.mkdir(parents=True, exist_ok=True)
            file_path = subdir / filename

            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)


            dir=f'{path}/{filename}'
            
           
            # Vector DB creation based on selected type (FAISS or ChromaDB)
            if db_type == "faiss":
                res = create_vector_db(filename, dir, 'uploads/others')
            elif db_type == "chromadb" :
                res = create_chroma_vector_db(filename, dir, 'uploads/others') 

            ## Handle the query if provided
            if query:
                if  model_type=="Gemini" and db_type == "faiss":
                    DB_FAISS_PATH = dir
                    response = final_result_faiss(query, DB_FAISS_PATH)

                elif model_type=="openai" and  db_type == "faiss" :
                       DB_FAISS_PATH = dir
                       response = final_result_faiss_openai(query,DB_FAISS_PATH)

                elif model_type=="Gemini" and db_type == "chromadb":
                    DB_CHROMA_PATH = dir
                    response = final_result_chroma(query, DB_CHROMA_PATH)

                elif model_type=="openai" and db_type == "chromadb":
                    DB_CHROMA_PATH = dir
                    response = final_result_chroma_openai(query, DB_CHROMA_PATH)

                ## Save interaction to the database
                interaction = ChatbotInteractionNew.objects.create(
                    file_name=dir,
                    file_type=path,
                    db_type=db_type,
                    query=query,
                    response=response if response else "No response generated"
                )


                # Convert results to JSON serializable format
                res_serialized = document_to_dict(res)
                response_serialized = document_to_dict(response)

                return render(request, 'vectorui/upload_interaction.html', {
                    'form': form,
                    'vector_result': res_serialized,
                    'query_response': response_serialized
                })

            # # Ensure response is JSON serializable if no query
            res_serialized = document_to_dict(res)
            return render(request, 'vectorui/upload_interaction.html', {
                'form': form,
                'vector_result': res_serialized.get("query_response", "No response generated")
            })              

           
    else:
        form = ChatbotInteractionNewForm()
    
    return render(request, 'vectorui/upload_interaction.html', {'form': form})

