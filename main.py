import speech_recognition as sr
import pyttsx3
from groq import Groq
import streamlit as st
import git

# Initialize the speech engine for Jarvis voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust voice speed if needed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use a different voice if needed

# Function to make Jarvis speak
def jarvis_speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Groq API client
client = Groq(api_key="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")

# Function to recognize speech using microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            jarvis_speak("Sorry, I could not understand the audio.")
        except sr.RequestError:
            jarvis_speak("Could not request results; check your network connection.")
    return ""

# Function to interact with Groq API
def process_with_groq(user_input):
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a college professor providing professional answers to CSE students that are short and concise"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65,
        stream=True,
        stop=None,
    )
    
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    
    return response

# Function to push changes to GitHub
def push_to_github():
    username = "Jaydev007-ui"
    token = "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"
    repo_name = "Chat"
    
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    
    repo = git.Repo.init()
    repo.git.add(all=True)
    repo.index.commit("Updated via Streamlit app")
    origin = repo.create_remote('origin', repo_url)
    origin.push(refspec='master:master')

# Streamlit App Interface
st.title("Jarvis Assistant with Groq API")

if st.button("Start Listening"):
    user_input = recognize_speech()
    if user_input:
        st.write(f"You said: {user_input}")
        jarvis_speak(f"You said: {user_input}")
        
        response = process_with_groq(user_input)
        st.write(f"Jarvis: {response}")
        jarvis_speak(response)

if st.button("Push to GitHub"):
    push_to_github()
    st.success("Changes pushed to GitHub successfully!")

# Run Streamlit App
if __name__ == "__main__":
    main()
