from django import forms
from .models import EnvVariable,ChatbotInteraction,ChatbotInteractionNew

class UploadQueryForm(forms.Form):

    model_choice = forms.ChoiceField(
        choices=[('Gemini', 'Google Gemini'), ('openai', 'OpenAI')],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        }),
        required=True,
        label="Choose Model"
    )


    db_type_choices = [
        ('faiss', 'FAISS'),
        ('chromadb', 'ChromaDB'),
    ]
    file = forms.FileField(
        label="Upload File",
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        })
    )
    db_type = forms.ChoiceField(
        choices=db_type_choices, 
        label="Select Vector Store",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        })
    )
    query = forms.CharField(
        max_length=255, 
        label="Query", 
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'rows': 4,
            'placeholder': 'Enter your query here...'
        })
    )

########################################################################################################


class ChatbotInteractionForm(forms.Form):
    model_choice = forms.ChoiceField(
        choices=[('Gemini', 'Google Gemini'), ('openai', 'OpenAI')],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        }),
        required=True
    )

    db_type_choices = [
        ('faiss', 'FAISS'),
        ('chromadb', 'ChromaDB'),
    ]

    db_type = forms.ChoiceField(
        choices=[("", "None")] + db_type_choices,
        label="Select Database",
        widget=forms.Select(attrs={
            'class': 'db-type-selector',
        })
    )

    query = forms.CharField(
        max_length=255,
        label="Query",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'rows': 4,
            'placeholder': 'Enter your query here...'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            file_records = ChatbotInteractionNew.objects.all()
            self.fields['vectorDB_field'] = forms.ChoiceField(
                choices=[("", "None")] + [
                    (file.file_name, f"{file.file_name} ({file.db_type})")  
                    for file in file_records
                ],
                label="Select Vector Store",
                widget=forms.Select(attrs={
                    'class': 'vector-db-selector',
                })
            )
        except Exception as e:
            self.fields['vectorDB_field'] = forms.ChoiceField(
                choices=[("", "None")],
                label="Select Vector Store"
            )
            print(f"Error fetching vectorDB data: {e}")




# class ChatbotInteractionForm(forms.Form):
#         model_choice = forms.ChoiceField(
#             choices=[('Gemini', 'Google Gemini'), ('openai', 'OpeanAI')],
#             widget=forms.Select(attrs={
#             'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
#         }),
#             # widget=forms.RadioSelect,
#             required=True
#         )
#         # openai_api_key = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g.,sk-proj-rzBHG4.............................'}), required=False, label="OpenAI API Key")
#         db_type_choices = [
#             ('faiss', 'FAISS'),
#             ('chromadb', 'ChromaDB'),
#         ]
#         file_records = ChatbotInteraction.objects.all()
#         print(file_records,"--------------->>>>>>>>>>>>>>>>>>")
#         # for file in file_records:
#         #     print(file.file_name)
            
#         # file = forms.FileField(label="Upload File", required=False)
#         db_type = forms.ChoiceField(choices=[("", "None")] +db_type_choices, label="Select Data Base")
#         vectorDB=forms.ChoiceField(choices=[("", "None")] + [(file.file_name,file.file_name) for file in file_records], label="Select Vector Store")
#         # print("vectorDB================================================",vectorDB)
#         query = forms.CharField(max_length=255, label="Query", required=False,
#                                 widget=forms.Textarea(attrs={
#             'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
#             'rows': 4,
#             'placeholder': 'Enter your query here...'
#         }))




class vectorDBForm(forms.Form):
    vectorDatabase = forms.CharField(
        max_length=255, 
        label="Vector Database Name", 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'placeholder': 'Enter vector database name...'
        })
    )

class MyForm(forms.Form):
    db_type = forms.ChoiceField(
        label='Select Database', 
        choices=[('faiss', 'FAISS'), ('chromadb', 'ChromaDB')],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        })
    )
    vectorstore = forms.ChoiceField(
        label='Select Vector Store', 
        choices=[],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        })
    )
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'rows': 4,
            'placeholder': 'Enter your query here...'
        }), 
        required=False, 
        label="Enter your query"
    )


class EnvVariableForm(forms.ModelForm):
        API_KEY_CHOICES = [
            ('GOOGLE_API_KEY', 'Google API Key'),
            ('OPENAI_API_KEY', 'OpenAI API Key'),
        ]

        env_variable_name = forms.ChoiceField(
            label="Select API Key Type",
            choices=API_KEY_CHOICES,
            widget=forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'})
        )

        class Meta:
            model = EnvVariable
            fields = ['env_variable_name', 'env_value']
            widgets = {
                'env_value': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'rows': 4, 'placeholder': 'Enter value'}),
            }



######################################################################################################################################

class ChatbotInteractionNewForm(forms.ModelForm):
    model_choice = forms.ChoiceField(
        choices=[('Gemini', 'Google Gemini'), ('openai', 'OpenAI')],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        }),
        required=True
    )

    db_type_choices = [
        ('faiss', 'FAISS'),
        ('chromadb', 'ChromaDB'),
    ]
    db_type = forms.ChoiceField(
        choices=db_type_choices,
        label="Select Database",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
        }),
        required=True
    )

    class Meta:
        model = ChatbotInteractionNew
        fields = ['file_name', 'file_type', 'db_type','query']
        labels = {
            'file_name': 'Upload File',
            'file_type': 'Select File Type',
            'query': 'Query',
        }
        widgets = {
            'file_name': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
            }),
            'file_type': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600'
            }),
            'query': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
                'rows': 4,
                'placeholder': 'Enter your query here...'
            }),
        }