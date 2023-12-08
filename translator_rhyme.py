import streamlit as st
import openai
import os
from deep_translator import GoogleTranslator

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics with rhyming translations
def generate_rhyming_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False):
    original_prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}. Try your best to match the style of the artist. Unless specified, do not use slang or casual language in the lyrics generated."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        original_prompt += " You are allowed to use slang and casual language in the lyrics in this case."

    # Generate rhyming translations using OpenAI GPT-3
    translated_prompt = f"Translate the following lines into rhyming Hindi:\n"
    translated_prompt += f'"{original_prompt}"'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=translated_prompt,
        max_tokens=200,
        temperature=temperature,
    )

    translated_lyric = response['choices'][0]['text']
    return translated_lyric

# Function to translate text to Hindi
def translate_to_hindi(text):
    translator = GoogleTranslator(source='auto', target='hindi')
    translation = translator.translate(text)
    return translation

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
subject = st.text_input("Subject (Optional):", "Enter the subject for this particular song")
rhyme = st.text_input("Rhyme (Optional):", "Enter a particular word or phrase that you would like used")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.')
translate_hindi = st.checkbox("Translate to Hindi", value=False, help="Check this box if you want to translate the lyrics to Hindi.")

# Generate rhyming lyrics when the user clicks the button
if st.button("Generate Rhyming Lyrics"):
    if artist_name and genre:
        # Call the generate_rhyming_lyrics function
        generated_lyric = generate_rhyming_lyrics(artist_name, genre, subject, rhyme, temperature, use_slang)

        # Display the generated rhyming lyric
        st.success(f"Generated Rhyming Lyrics:\n{generated_lyric}")

        # Translate to Hindi if requested
        if translate_hindi:
            translated_lyric = translate_to_hindi(generated_lyric)
            st.success(f"Translated to Hindi:\n{translated_lyric}")

        # Ask for user feedback
        user_feedback = st.selectbox("How satisfied are you with the generated rhyming lyric?", ["Satisfied", "Neutral", "Dissatisfied"])

        # Use user feedback to refine the model if dissatisfied
        if user_feedback == "Dissatisfied":
            st.info("Thank you for your feedback! We will use this to improve our lyric generation.")

