from django.contrib import admin
from .models import ChatbotInteraction,VectorStore,EnvVariable
# Register your models here.
admin.site.register((ChatbotInteraction,VectorStore,EnvVariable))