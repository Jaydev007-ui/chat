import streamlit as st
from gtts import gTTS
import os
import requests
from github import Github

# Function to make Jarvis speak using gTTS
def jarvis_speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    st.audio("response.mp3")  # Streamlit plays the mp3 file directly

# Initialize GitHub client
g = Github("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")
repo = g.get_user().get_repo("Chat")

# Streamlit app
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
        st.session_state.voice_enabled = voice_enabled

        st.write("Enter your message below and Jarvis will respond.")
        user_message = st.text_input("Your Message")
        if st.button("Send Message"):
            if user_message:
                # Simulate Groq API call (replace this with real logic or API call if needed)
                response = simulate_groq_response(user_message)

                # Display the response in the Streamlit app
                st.write(f"Jarvis: {response}")

                # Optionally, make Jarvis speak the response
                if voice_enabled:
                    jarvis_speak(response)

                # Save the interaction to GitHub
                try:
                    repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {response}")
                    st.success("Interaction saved to GitHub!")
                except Exception as e:
                    st.error(f"Failed to save to GitHub: {e}")
            else:
                st.write("Please enter a message.")
        else:
            st.write("The chatbot's responses will appear here.")

# Simulated response from the Groq API (You can replace this with actual logic or API calls)
def simulate_groq_response(user_message):
    # For now, it just echoes the input. You can add your actual processing logic here.
    return f"I received your message: {user_message}. I'm Jarvis, how can I help further?"

if __name__ == '__main__':
    streamlit_app()
