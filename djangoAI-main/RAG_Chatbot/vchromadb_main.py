from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader , TextLoader, UnstructuredWordDocumentLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from uuid import uuid4
import os
from langchain.prompts import PromptTemplate
# from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import glob
from pathlib import Path
import os 
import openai
from translator.llm import llm_gemini,llm_open_ai


print("this for test")



current_path = Path.cwd()


custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""



# DATA_PATH = '../data/'
# DB_CHROMA_PATH = 'chromavectorstore1/db_chroma'

def create_chroma_vector_db(filename,DB_CHROMA_PATH='chromavectorstore1/db_chroma',DATA_PATH= 'uploads/others'):
    if not os.path.exists(DATA_PATH):
        print(f"Data path '{DATA_PATH}' does not exist.")
        return
    print("===================filename------>>>>",filename)
    pattern = os.path.join(DATA_PATH,filename)
    target_path = current_path / pattern
    pattern =target_path
    print("------------pattern =============>",str(pattern))
    # Define loaders for each file type
    extension=filename.split(".")[-1]
    loader_type={"pdf":DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader),
     "txt":DirectoryLoader(DATA_PATH, glob='*.txt', loader_cls=TextLoader),
     "docx":DirectoryLoader(DATA_PATH, glob='*.docx', loader_cls=UnstructuredWordDocumentLoader),
     "json": DirectoryLoader(DATA_PATH, glob='*.json', loader_cls=JSONLoader)
     }
    loader=loader_type.get(extension)
    # pdf_loader = DirectoryLoader(DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)
    # txt_loader = DirectoryLoader(DATA_PATH, glob='*.txt', loader_cls=TextLoader)
    # docx_loader = DirectoryLoader(DATA_PATH, glob='*.docx', loader_cls=UnstructuredWordDocumentLoader)
    # json_loader = DirectoryLoader(DATA_PATH, glob='*.json', loader_cls=JSONLoader)

    # Load the documents
    if loader:
        documents = loader.load()
    # txt_documents = txt_loader.load()
    # docx_documents = docx_loader.load()
    # json_documents = json_loader.load()

    # Combine all documents into a single list
        all_documents = documents

        if not all_documents:
            print("No documents found. Ensure there are PDF files in the specified directory.")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(all_documents)


        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                        model_kwargs={'device': 'cpu'})
        


        chroma_vectordb = Chroma.from_documents(texts, embeddings,persist_directory=DB_CHROMA_PATH)



        os.makedirs(os.path.dirname(DB_CHROMA_PATH), exist_ok=True)
        # chroma_vectordb.save_local(DB_CHROMA_PATH)
        print(f"Vector database saved at '{DB_CHROMA_PATH}'")


        return f"Vector database saved at '{DB_CHROMA_PATH}'"
    else:
        return f"Extension loader not define please provide file ['text','pdf','docs','json']"

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return qa_chain

def load_llm():
    # llm = ChatOpenAI(model_name="MODEL_NAME", temperature=0.0,api_key=OPEN_API_KEY)
    # llm = CTransformers(
    #     model="/home/in2itadmin/Desktop/Llama2-Medical-Chatbot/llmmodel/llama-2-7b-chat.ggmlv3.q8_0.bin",
    #     model_type="llama",
    #     max_new_tokens=512,
    #     temperature=0.5
    # )
    llm = llm_gemini()
    return llm


def qa_bot(DB_CHROMA_PATH):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )


    #for chromaDB
    db=Chroma(persist_directory=DB_CHROMA_PATH,embedding_function=embeddings)

   

    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa


def final_result_chroma(query,DB_CHROMA_PATH):
    qa_result = qa_bot(DB_CHROMA_PATH)
    response = qa_result({'query': query})
    # print("----------------------------------------respone_chromadb==================================",response)
    return response['result']





######################################################### For openai ###############################################

def load_openai(prompt):
    """
    Load OpenAI and return the response for the given prompt.
    """
    openai.api_key = llm_open_ai()

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  
            messages=[{"role": "user", "content": prompt}], 
            temperature=0,  
            max_tokens=1000 
        )
        return response
    except Exception as e:
        raise ValueError(f"Failed to load OpenAI LLM: {e}")


def retrieval_qa_chain_openai(prompt, db):
    """
    Query OpenAI directly with the provided prompt and return results.
    """
    try:
        response = load_openai(prompt)  
        return response
    except Exception as e:
        raise ValueError(f"Failed to query OpenAI: {e}")


def qa_bot_openai(DB_CHROMA_PATH, query):
    """
    Prepare CHROMA retriever and query OpenAI.
    """
    try:
        # Load embeddings and database
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        db=Chroma(persist_directory=DB_CHROMA_PATH,embedding_function=embeddings)

        # Prepare prompt with query
        documents = db.similarity_search(query, k=2)  
        context = "\n".join([doc.page_content for doc in documents])  
        prompt = f"Context:\n{context}\n\nQuery:\n{query}\n\nAnswer:"
        
        # Query OpenAI
        response = retrieval_qa_chain_openai(prompt, db)
        return response
    except Exception as e:
        raise ValueError(f"Failed to initialize QA bot: {e}")



def final_result_chroma_openai(query, DB_CHROMA_PATH):
    """
    Execute the query using the QA bot and return the result.
    """
    try:
        response = qa_bot_openai(DB_CHROMA_PATH, query)
        print("Response:", response)
        return response['choices'][0]['message']['content']  
    except Exception as e:
        raise ValueError(f"Error during query execution: {e}")
