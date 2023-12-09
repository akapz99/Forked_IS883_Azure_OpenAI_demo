import streamlit as st
import os
import openai
from deep_translator import GoogleTranslator

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False):
    prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}. Every song should have at least 2 verses, 1 chorus and 1 bridge. The song should follow the structure of Verse 1, Chorus, Verse 2, Chorus, Bridge, Chorus. Try your best to match the style of the artist. Unless specified, do not use slang or casual language in the lyrics generated."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        prompt += " You are allowed to use slang and casual language in the lyrics in this case."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']
    return generated_lyric


# Function to translate text to the selected language and add rhyming translations
def translate_and_rhyme(text, language, rhyme, temperature=0.7): 
    translation_prompt = f"I want you to act as a translator and songwriter, and create a cover version of the {generated_lyric} in {language}. The cover version should match the style and structure of the {generated_lyric}. Every section of the {generated_lyric} should be translated. The translation should follow the structure of Verse 1, Chorus, Verse 2, Chorus, Bridge, Chorus. The translation should be in the script, and use the alphabet of the {language}. Your objective is to seamlessly blend the linguistic and artistic elements to produce a cover that resonates authentically with the spirit of the original.:\n"
    translation_prompt += f'"{text}"'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=translation_prompt,
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
temperature = st.slider("Select how much personal (random) input you would like from me (the AI)", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.')
selected_language = st.selectbox("Select Language", ["Select a Language", "Fante", "Hindi", "French", "Arabic", "German", "Italian", "Spanish"])
translate_selected_language = st.checkbox(f"Translate to {selected_language}", value=False, help=f"Check this box if you want to translate the lyrics to {selected_language}.")

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, subject, rhyme, temperature, use_slang)

        # Display the generated lyric
        st.success(f"Generated Lyric:\n{generated_lyric}")

        # Translate to the selected language with rhyming if requested
        if translate_selected_language:
            translated_lyric = translate_and_rhyme(generated_lyric, selected_language.lower(), rhyme, temperature)
            st.success(f"Translated to {selected_language} with Rhyme:\n{translated_lyric}")

        # Ask for user feedback
        user_feedback = st.selectbox("How satisfied are you with the generated lyric?", ["Satisfied", "Neutral", "Dissatisfied"])

        # Use user feedback to refine the model if dissatisfied
        if user_feedback == "Dissatisfied":
            st.info("Thank you for your feedback! We will use this to improve our lyric generation.")

