from django.urls import path
# from .views import upload_query_view,vectorstore_view,upload_view
from .views import upload_interaction_view,vectorstore_view,upload_view,env_variable_view,delete_env_variable,uploaded_query_view

urlpatterns = [
    path('', upload_interaction_view, name='upload_query'),
    path('vectorstore_view',vectorstore_view,name='vectorstore_view'),
    path('upload_view',upload_view,name='upload_view'),
    path('uploaded_query_view',uploaded_query_view,name='uploaded_query_view'),
    path('env_variable', env_variable_view, name='env_variable_form'),
    path('delete-env-variable/<int:id>/',delete_env_variable, name='delete_env_variable'),
]

