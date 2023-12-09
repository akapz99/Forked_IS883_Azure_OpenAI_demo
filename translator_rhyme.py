import streamlit as st
import openai
import os
from deep_translator import GoogleTranslator

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False):
    prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to the style of this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}. Try your best to match the style of the artist. Unless specified, do not use slang or casual language in the lyrics generated. Unless specified, do not translate the lyrics. If translation is specified, try to ensure that the translation rhymes."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        prompt += " You are allowed to use slang and casual language in the lyrics in this case."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']
    return generated_lyric

# Function to translate text to Hindi and add rhyming translations
def translate_to_hindi_with_rhyme(text, rhyme, temperature=0.7):
    # Add rhyming component to the translation prompt
    prompt = f"Translate the following lines into rhyming Hindi:\n"
    prompt += f'"{text}"'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=temperature,
    )

    translated_lyric = response['choices'][0]['text']
    return translated_lyric

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

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, subject, rhyme, temperature, use_slang)

        # Display the generated lyric
        st.success(f"Generated Lyric:\n{generated_lyric}")

        # Translate to Hindi with rhyming if requested
        if translate_hindi:
            translated_lyric = translate_to_hindi_with_rhyme(generated_lyric, rhyme, temperature)
            st.success(f"Translated to Hindi with Rhyme:\n{translated_lyric}")

        # Ask for user feedback
        user_feedback = st.selectbox("How satisfied are you with the generated lyric?", ["Satisfied", "Neutral", "Dissatisfied"])

        # Use user feedback to refine the model if dissatisfied
        if user_feedback == "Dissatisfied":
            st.info("Thank you for your feedback! We will use this to improve our lyric generation.")
