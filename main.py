import streamlit as st
from gtts import gTTS
from io import BytesIO
from transformers import pipeline

# Set up the chatbot model
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Function for text-to-speech using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

# Streamlit UI
st.title("Chatbot with Text-to-Speech")

st.write("Talk to the chatbot below:")

# Create a chat input box
user_input = st.text_input("You: ")

# Process the user input and generate a response
if user_input:
    # Generate response from the chatbot
    response = chatbot(user_input)[0]['generated_text']

    # Display the chatbot's response
    st.write(f"Bot: {response}")

    # Generate TTS and play the response
    audio_file = speak(response)
    st.audio(audio_file, format="audio/mp3")
