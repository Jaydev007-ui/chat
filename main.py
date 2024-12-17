import streamlit as st
import pyttsx3
from transformers import pipeline

# Initialize the TTS engine
engine = pyttsx3.init()

# Set up the chatbot model
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    
    # Speak the chatbot's response
    speak(response)
