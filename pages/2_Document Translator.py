import streamlit as st
import datetime
import base64
import time

from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient
from azure.storage.blob import BlobServiceClient, generate_container_sas

# Language mapping between names and codes
language_map_name = {'Afrikaans': 'af', 'Amharic': 'am', 'Arabic': 'ar', 'Assamese': 'as', 'Azerbaijani': 'az', 'Bashkir': 'ba', 'Bulgarian': 'bg', 'Bangla': 'bn', 'Tibetan': 'bo', 'Bosnian': 'bs', 'Catalan': 'ca', 'Czech': 'cs', 'Welsh': 'cy', 'Danish': 'da', 'German': 'de', 'Lower Sorbian': 'dsb', 'Divehi': 'dv', 'Greek': 'el', 'English': 'en', 'Spanish': 'es', 'Estonian': 'et', 'Basque': 'eu', 'Persian': 'fa', 'Finnish': 'fi', 'Filipino': 'fil', 'Fijian': 'fj', 'Faroese': 'fo', 'French': 'fr', 'French (Canada)': 'fr-CA', 'Irish': 'ga', 'Galician': 'gl', 'Konkani': 'gom', 'Gujarati': 'gu', 'Hausa': 'ha', 'Hebrew': 'he', 'Hindi': 'hi', 'Croatian': 'hr', 'Upper Sorbian': 'hsb', 'Haitian Creole': 'ht', 'Hungarian': 'hu', 'Armenian': 'hy', 'Indonesian': 'id', 'Igbo': 'ig', 'Inuinnaqtun': 'ikt', 'Icelandic': 'is', 'Italian': 'it', 'Inuktitut': 'iu', 'Inuktitut (Latin)': 'iu-Latn', 'Japanese': 'ja', 'Georgian': 'ka', 'Kazakh': 'kk', 'Khmer': 'km', 'Kurdish (Northern)': 'kmr', 'Kannada': 'kn', 'Korean': 'ko', 'Kurdish (Central)': 'ku', 'Kyrgyz': 'ky', 'Lingala': 'ln', 'Lao': 'lo', 'Lithuanian': 'lt', 'Ganda': 'lug', 'Latvian': 'lv', 'Chinese (Literary)': 'lzh', 'Maithili': 'mai', 'Malagasy': 'mg', 'Māori': 'mi', 'Macedonian': 'mk', 'Malayalam': 'ml', 'Mongolian (Cyrillic)': 'mn-Cyrl', 'Mongolian (Traditional)': 'mn-Mong', 'Marathi': 'mr', 'Malay': 'ms', 'Maltese': 'mt', 'Hmong Daw': 'mww', 'Myanmar (Burmese)': 'my', 'Norwegian': 'nb', 'Nepali': 'ne', 'Dutch': 'nl', 'Sesotho sa Leboa': 'nso', 'Nyanja': 'nya', 'Odia': 'or', 'Querétaro Otomi': 'otq', 'Punjabi': 'pa', 'Polish': 'pl', 'Dari': 'prs', 'Pashto': 'ps', 'Portuguese (Brazil)': 'pt', 'Portuguese (Portugal)': 'pt-PT', 'Romanian': 'ro', 'Russian': 'ru', 'Rundi': 'run', 'Kinyarwanda': 'rw', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Samoan': 'sm', 'Shona': 'sn', 'Somali': 'so', 'Albanian': 'sq', 'Serbian (Cyrillic)': 'sr-Cyrl', 'Serbian (Latin)': 'sr-Latn', 'Sesotho': 'st', 'Swedish': 'sv', 'Swahili': 'sw', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Turkmen': 'tk', 'Klingon (Latin)': 'tlh-Latn', 'Klingon (pIqaD)': 'tlh-Piqd', 'Setswana': 'tn', 'Tongan': 'to', 'Turkish': 'tr', 'Tatar': 'tt', 'Tahitian': 'ty', 'Uyghur': 'ug', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek (Latin)': 'uz', 'Vietnamese': 'vi', 'Xhosa': 'xh', 'Yoruba': 'yo', 'Yucatec Maya': 'yua', 'Cantonese (Traditional)': 'yue', 'Chinese Simplified': 'zh-Hans', 'Chinese Traditional': 'zh-Hant', 'Zulu': 'zu'}

# Set the Streamlit page layout
st.set_page_config(layout="wide")

# File upload and output language selection
uploaded_files = st.file_uploader("Choose a PDF file", type=["pdf","doc","docx"], accept_multiple_files=False)
output_option = st.selectbox(
    'Output language?',
    language_map_name.keys())

# Azure Translator and Azure Storage configurations
endpoint = "translator_endpoint"
key = "translator_key"
storage_endpoint = "storage_endpoint"
storage_account_name = "storage_account_name"
storage_key = "storage_key"
storage_source_container_name = "storage_source_container_name"
storage_target_container_name = "storage_target_container_name"

# Initialize the DocumentTranslationClient and BlobServiceClient
translation_client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
blob_service_client = BlobServiceClient(storage_endpoint, credential=storage_key)

# Get the source and target containers
source_container = blob_service_client.get_container_client(container=storage_source_container_name)
target_container = blob_service_client.get_container_client(container=storage_target_container_name)

# Generate a shared access signature (SAS) URL for the containers
def generate_sas_url(container, permissions):
    sas_token = generate_container_sas(
        account_name=storage_account_name,
        container_name=container.container_name,
        account_key=storage_key,
        permission=permissions,
        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    )

    container_sas_url = storage_endpoint + container.container_name + "?" + sas_token
    return container_sas_url

# Display the translated PDF document
def show_pdf(document_name):
    blob_client = blob_service_client.get_blob_client(container=target_container.container_name, blob=document_name)
    base64_pdf = base64.b64encode(blob_client.download_blob().readall()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=100% height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Clean up the source and target containers
def clean_blobs():
    for blob in source_container.list_blobs():
        source_container.delete_blob(blob)
    for blob in target_container.list_blobs():
        target_container.delete_blob(blob)

# Perform translation when the "Translate" button is clicked and a file is uploaded
if st.button('Translate') and uploaded_files is not None:
    document_name = uploaded_files.name
    source_container.upload_blob(document_name, uploaded_files.getvalue())

    # Generate SAS URLs for the source and target containers
    source_container_sas_url = generate_sas_url(source_container, permissions="rl")
    target_container_sas_url = generate_sas_url(target_container, permissions="wl")

    # Start the translation and wait for it to complete
    poller = translation_client.begin_translation(source_container_sas_url, target_container_sas_url, language_map_name[output_option])
    result = poller.result()

    while poller.status() != "Succeeded":
        time.sleep(5)

    # Display the translated PDF document and clean up the containers
    show_pdf(document_name)
    clean_blobs()