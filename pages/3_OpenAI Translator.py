import streamlit as st
import requests
import json
import openai

# Set the Streamlit page layout
st.set_page_config(layout="wide")

# Configure OpenAI API credentials and settings
openai.api_key = "openai_key"
openai.api_base = "openai_endpoint"
openai.api_type = 'azure'
openai.api_version = '2023-05-15'
deployment_name = 'deployment_name'

# Language mapping between names and codes
language_map_name = {'Afrikaans': 'af', 'Amharic': 'am', 'Arabic': 'ar', 'Assamese': 'as', 'Azerbaijani': 'az', 'Bashkir': 'ba', 'Bulgarian': 'bg', 'Bangla': 'bn', 'Tibetan': 'bo', 'Bosnian': 'bs', 'Catalan': 'ca', 'Czech': 'cs', 'Welsh': 'cy', 'Danish': 'da', 'German': 'de', 'Lower Sorbian': 'dsb', 'Divehi': 'dv', 'Greek': 'el', 'English': 'en', 'Spanish': 'es', 'Estonian': 'et', 'Basque': 'eu', 'Persian': 'fa', 'Finnish': 'fi', 'Filipino': 'fil', 'Fijian': 'fj', 'Faroese': 'fo', 'French': 'fr', 'French (Canada)': 'fr-CA', 'Irish': 'ga', 'Galician': 'gl', 'Konkani': 'gom', 'Gujarati': 'gu', 'Hausa': 'ha', 'Hebrew': 'he', 'Hindi': 'hi', 'Croatian': 'hr', 'Upper Sorbian': 'hsb', 'Haitian Creole': 'ht', 'Hungarian': 'hu', 'Armenian': 'hy', 'Indonesian': 'id', 'Igbo': 'ig', 'Inuinnaqtun': 'ikt', 'Icelandic': 'is', 'Italian': 'it', 'Inuktitut': 'iu', 'Inuktitut (Latin)': 'iu-Latn', 'Japanese': 'ja', 'Georgian': 'ka', 'Kazakh': 'kk', 'Khmer': 'km', 'Kurdish (Northern)': 'kmr', 'Kannada': 'kn', 'Korean': 'ko', 'Kurdish (Central)': 'ku', 'Kyrgyz': 'ky', 'Lingala': 'ln', 'Lao': 'lo', 'Lithuanian': 'lt', 'Ganda': 'lug', 'Latvian': 'lv', 'Chinese (Literary)': 'lzh', 'Maithili': 'mai', 'Malagasy': 'mg', 'Māori': 'mi', 'Macedonian': 'mk', 'Malayalam': 'ml', 'Mongolian (Cyrillic)': 'mn-Cyrl', 'Mongolian (Traditional)': 'mn-Mong', 'Marathi': 'mr', 'Malay': 'ms', 'Maltese': 'mt', 'Hmong Daw': 'mww', 'Myanmar (Burmese)': 'my', 'Norwegian': 'nb', 'Nepali': 'ne', 'Dutch': 'nl', 'Sesotho sa Leboa': 'nso', 'Nyanja': 'nya', 'Odia': 'or', 'Querétaro Otomi': 'otq', 'Punjabi': 'pa', 'Polish': 'pl', 'Dari': 'prs', 'Pashto': 'ps', 'Portuguese (Brazil)': 'pt', 'Portuguese (Portugal)': 'pt-PT', 'Romanian': 'ro', 'Russian': 'ru', 'Rundi': 'run', 'Kinyarwanda': 'rw', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Albanian': 'sq', 'Serbian (Cyrillic)': 'sr-Cyrl', 'Serbian (Latin)': 'sr-Latn', 'Sesotho': 'st', 'Swedish': 'sv', 'Swahili': 'sw', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Turkmen': 'tk', 'Klingon (Latin)': 'tlh-Latn', 'Klingon (pIqaD)': 'tlh-Piqd', 'Setswana': 'tn', 'Tongan': 'to', 'Turkish': 'tr', 'Tatar': 'tt', 'Tahitian': 'ty', 'Uyghur': 'ug', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek (Latin)': 'uz', 'Vietnamese': 'vi', 'Xhosa': 'xh', 'Yoruba': 'yo', 'Yucatec Maya': 'yua', 'Cantonese (Traditional)': 'yue', 'Chinese Simplified': 'zh-Hans', 'Chinese Traditional': 'zh-Hant', 'Zulu': 'zu'}

# Input and output language selection
input_option_autodetect = list(language_map_name.keys())
input_option_autodetect.insert(0, "AUTODETECT")
input_option = st.selectbox(
    'Input language?',
    input_option_autodetect)

output_option = st.selectbox(
    'Output language?',
    language_map_name.keys())

# GPT model context input
header_context = ("Your only job is to translate text between two languages. Don't do anything else.\n" +
                    "If you don't know/recognize the input or output language, don't translate.\n")

if input_option == "AUTODETECT":
    context = st.text_area('GPT model context',
                        header_context + 
                        "Translate below text to " + output_option + ":\n")
else:
    context = st.text_area('GPT model context',
                        header_context +
                        "Translate below text from " + input_option + " to " + output_option + ":\n")

# Input text to translate
input_text = st.text_area('Text to translate')

# Max tokens slider
tokens = st.slider('Max number of tokens:', 0, 4000, 500)

# Perform translation when the "Translate" button is clicked
if st.button('Translate'):
    response = openai.Completion.create(
        engine=deployment_name, 
        prompt=context + input_text, 
        max_tokens=tokens)
    
    response_text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    st.write("Translated text:\n\n" + response_text)



