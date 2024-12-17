import speech_recognition as sr
from groq import Groq
import streamlit as st
from github import Github
import os

# Initialize the speech recognition module
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Initialize Groq API client
client = Groq(api_key="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")

# Initialize GitHub client
g = Github("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")
repo = g.get_user().get_repo("Chat")

# Function to capture voice input
def recognize_speech():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"Recognized: {user_input}")
        return user_input
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, I'm having trouble connecting to Google's service."

# Streamlit integration
def streamlit_app():
    st.image("TSS.png", width=200)  # Display the logo
    st.title("Jarvis Chat with Groq Integration")
    
    # Login section
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "JAYDEV" and password == "ZALA":
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials")
    else:
        # Voice command control
        voice_enabled = st.checkbox("Enable voice command")

        if voice_enabled:
            st.write("Click the button and speak to Jarvis.")
            if st.button("Record Voice"):
                user_message = recognize_speech()
                st.write(f"You said: {user_message}")
        else:
            user_message = st.text_input("Your Message")

        if st.button("Send Message"):
            if user_message:
                # Process the user input with Groq
                completion = client.chat.completions.create(
                    model="llama3-groq-70b-8192-tool-use-preview",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a college professor providing professional answers to CSE students that are short and concise"
                        },
                        {
                            "role": "user",
                            "content": user_message
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

                st.write(f"Jarvis: {response}")
                
                # Save the interaction to GitHub
                repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {response}")
            else:
                st.write("Please enter a message.")

if __name__ == '__main__':
    streamlit_app()
