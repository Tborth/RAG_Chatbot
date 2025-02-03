from django import forms

class TranslationForm(forms.Form):
    MODEL_CHOICES = [
        ('Gemini', 'Google Gemini'),
        ('openai', 'OpenAI'),
    ]

    model_choice = forms.ChoiceField(
        choices=MODEL_CHOICES,
        required=True,
        label="Choose Model",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
        }),
    )

    # openai_api_key = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
    #         'placeholder': 'Enter OpenAI API Key (if using OpenAI model)',
    #     }),
    #     required=False,
    #     label="OpenAI API Key",
    # )

    text = forms.CharField(
        label="Text to Translate",
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
            'rows': 5,
            'placeholder': 'Enter the text to translate...',
        }),
    )

    target_language = forms.ChoiceField(
        label="Target Language",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-600 focus:border-green-600',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate target language choices dynamically
        available_languages = [
            "Abkhazian", "Acehnese", "Acoli", "Afar", "Afrikaans", "Akan", "Albanian", "Alur", "Amharic", "Arabic",
            "Armenian", "Assamese", "Avaric", "Awadhi", "Aymara", "Azerbaijani", "Balinese", "Baluchi", "Bambara",
            "Bangla", "Baoulé", "Bashkir", "Basque", "Batak Karo", "Batak Simalungun", "Batak Toba", "Belarusian",
            "Bemba", "Betawi", "Bhojpuri", "Bikol", "Bosnian", "Breton", "Bulgarian", "Buriat", "Burmese", "Cantonese",
            "Catalan", "Cebuano", "Central Kurdish", "Chamorro", "Chechen", "Chiga", "Chinese (Simplified)",
            "Chinese (Traditional)", "Chuukese", "Chuvash", "Corsican", "Crimean Tatar", "Croatian", "Czech",
            "Danish", "Dari", "Dinka", "Divehi", "Dogri", "Dombe", "Dutch", "Dyula", "Dzongkha", "English",
            "Esperanto", "Estonian", "Ewe", "Faroese", "Fijian", "Filipino", "Finnish", "Fon", "French", "Friulian",
            "Fulani", "Ga", "Galician", "Ganda", "Georgian", "German", "Goan Konkani", "Greek", "Guarani", "Gujarati",
            "Haitian Creole", "Hakha Chin", "Hausa", "Hawaiian", "Hebrew", "Hiligaynon", "Hindi", "Hmong", "Hungarian",
            "Hunsrik", "Iban", "Icelandic", "Igbo", "Iloko", "Indonesian", "Irish", "Italian", "Jamaican Patois",
            "Japanese", "Javanese", "Jingpo", "Kalaallisut", "Kannada", "Kanuri", "Kazakh", "Khasi", "Khmer",
            "Kinyarwanda", "Kituba", "Kokborok", "Komi", "Kongo", "Korean", "Krio", "Kurdish", "Kyrgyz", "Lao",
            "Latgalian", "Latin", "Latvian", "Ligurian", "Limburgish", "Lingala", "Lithuanian", "Lombard", "Luo",
            "Luxembourgish", "Macedonian", "Madurese", "Maithili", "Makasar", "Malagasy", "Malay", "Malay (Arabic)",
            "Malayalam", "Maltese", "Mam", "Manipuri (Meitei Mayek)", "Manx", "Māori", "Marathi", "Marshallese",
            "Marwari", "Meadow Mari", "Minangkabau", "Mizo", "Mongolian", "Morisyen", "Nahuatl (Eastern Huasteca)",
            "Ndau", "Nepalbhasa (Newari)", "Nepali", "Nko", "Northern Sami", "Northern Sotho", "Norwegian", "Nuer",
            "Nyanja", "Occitan", "Odia", "Oromo", "Ossetic", "Pampanga", "Pangasinan", "Papiamento", "Pashto", "Persian",
            "Polish", "Portuguese", "Portuguese (Portugal)", "Punjabi", "Punjabi (Arabic)", "Q'eqchi'", "Quechua",
            "Romanian", "Romany", "Rundi", "Russian", "Samoan", "Sango", "Sanskrit", "Santali (Latin)",
            "Scottish Gaelic", "Serbian", "Seselwa Creole French", "Shan", "Shona", "Sicilian", "Silesian", "Sindhi",
            "Sinhala", "Slovak", "Slovenian", "Somali", "South Ndebele", "Southern Sotho", "Spanish", "Sundanese",
            "Susu", "Swahili", "Swati", "Swedish", "Tahitian", "Tajik", "Tamazight", "Tamazight (Tifinagh)", "Tamil",
            "Tatar", "Telugu", "Tetum", "Thai", "Tibetan", "Tigrinya", "Tiv", "Tok Pisin", "Tongan", "Tsonga",
            "Tswana", "Tulu", "Tumbuka", "Turkish", "Turkmen", "Tuvinian", "Udmurt", "Ukrainian", "Urdu", "Uyghur",
            "Uzbek", "Venda", "Venetian", "Vietnamese", "Waray", "Welsh", "Western Frisian", "Wolof", "Xhosa", "Yakut",
            "Yiddish", "Yoruba", "Yucatec Maya", "Zapotec", "Zulu"
        ]
        self.fields['target_language'].choices = [(lang, lang) for lang in available_languages]

    def clean(self):
        cleaned_data = super().clean()
        model_choice = cleaned_data.get('model_choice')
        # openai_api_key = cleaned_data.get('openai_api_key')

        # # Validate API key if OpenAI model is selected
        # if model_choice == 'openai' and not openai_api_key:
        #     self.add_error('openai_api_key', 'This field is required when using OpenAI.')
        return cleaned_data
