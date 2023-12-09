import streamlit as st
import os
import openai

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
# ... (unchanged)

# Function to translate text to the selected language and add rhyming translations
def translate_and_rhyme(text, language, rhyme, temperature=0.7):
    translation_prompt = f"Translate the following lines into rhyming {language}:\n"
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
selected_language = st.selectbox("Select Language", ["Fante", "Hindi", "French", "Arabic", "German", "Italian", "Spanish"])
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

