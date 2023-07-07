import streamlit as st

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

# Azure Translator API credentials
key = "translator_key"
endpoint = "translator_endpoint"
region = "translator_region"

# Create TranslatorCredential and TextTranslationClient instances
credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

# Create language maps for language names and codes
language_map_name = {}
language_map_code = {}

try:
    scope = "translation"
    response = response = text_translator.get_languages(scope=scope)

    # Populate language maps with language names and codes
    for key in response.translation.keys():
        language_map_name[response.translation[key].name] = key
        language_map_code[key] = response.translation[key].name

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")

def translateTextAutodetect(output_language, txt):
    try:
        # Convert output language name to code
        output_language = language_map_name[output_language]
        input_text_elements = [InputTextItem(text=txt)]

        # Perform translation with autodetection
        response = text_translator.translate(content=input_text_elements, to=[output_language])
        translation = response[0] if response else None

        if translation:
            detected_language = translation.detected_language
            if detected_language:
                print(f"Detected languages of the input text: {detected_language.language} with score: {detected_language.score}.")
            for translated_text in translation.translations:
                print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")
            message = translated_text.text
            detected_language = detected_language.language

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
        message = exception.error.message
        detected_language = None

    return message, detected_language

def translateText(input_language, output_language, txt):
    try:
        # Convert input and output language names to codes
        input_language = language_map_name[input_language]
        output_language = language_map_name[output_language]
        input_text = [InputTextItem(text=txt)]

        # Perform translation with specified input and output languages
        response = text_translator.translate(content=input_text, to=[output_language], from_parameter=input_language)
        translation = response[0] if response else None

        if translation:
            message = ""
            for translated_text in translation.translations:
                message = message + translated_text.text            

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")
        message = exception.error.message

    return message

# Set the Streamlit page layout
st.set_page_config(layout="wide")

# Create input and output language options
input_option_autodetect = [value['name'] for value in response.translation.values()]
input_option_autodetect.insert(0, "AUTODETECT")
input_option = st.selectbox(
    'Input language?',
    input_option_autodetect)

output_option = st.selectbox(
    'Output language?',
    [value['name'] for value in response.translation.values()])

# Get the input text
input_text = st.text_area('Text to translate')

# Translate button
if st.button('Translate'):
    if input_option == 'AUTODETECT':
        # Perform translation with autodetection
        output_text, detected_language = translateTextAutodetect(output_option, input_text)
        st.write("Detected language: " + language_map_code[detected_language])
        st.write("Translated text:\n\n" + output_text)
    else:
        # Perform translation with specified input and output languages
        output_text = translateText(input_option, output_option, input_text)
        st.write(output_text)
