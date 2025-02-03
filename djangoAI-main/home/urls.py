from django.urls import path
from .views import index

app_name = 'home'  # Add this line

urlpatterns = [
    path('', index, name='index'),
]

