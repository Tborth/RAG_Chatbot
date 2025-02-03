# models.py in RAG_Chatbot app
from django.db import models
import os

class ChatbotInteraction(models.Model):
    file_name = models.CharField(max_length=255)
    db_type = models.CharField(max_length=50)
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.db_type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class VectorStore(models.Model):
    file_name = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class EnvVariable(models.Model):
    env_variable_name = models.TextField()
    env_value = models.TextField()

    def __str__(self):
        return f"{self.env_variable_name}"
    

##############################################################################


def upload_to_dynamic(instance, filename):
    # Generate a unique file name
    ext = filename
    # unique_filename = f"{uuid.uuid4()}.{ext}"

    if instance.file_type == 'Faiss_folder':
        folder = 'FaissVectorStore'
    elif instance.file_type == 'ChromaDB_folder':
        folder = 'ChromaDBVectorStore'
    else:
        folder = 'OtherVectorStore'

    return os.path.join(folder, ext)

class ChatbotInteractionNew(models.Model):
    FILE_TYPE_CHOICES = [
        ('Faiss_folder', 'FaissDB_Folder'),
        ('ChromaDB_folder', 'ChromaDB_Folder'),
    ]

    file_name = models.FileField(upload_to=upload_to_dynamic, max_length=255)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    db_type = models.CharField(max_length=50)
    query = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        file_name = self.file_name.name if self.file_name else "No File"
        return f"{file_name} - {self.file_type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
