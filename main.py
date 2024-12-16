from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import pyttsx3
from groq import Groq
import streamlit as st
from github import Github
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'Zala_@_0007'  # Add a secret key for session management

# Initialize pyttsx3 for Windows (SAPI5 engine)
engine = pyttsx3.init(driverName='sapi5')  # SAPI5 is the default TTS engine for Windows

# Adjust speech properties
engine.setProperty('rate', 150)  # Adjust speech rate
engine.setProperty('volume', 1)  # Adjust volume (0.0 to 1.0)
engine.say("Hello, this is Jarvis speaking!")
engine.runAndWait()

# Initialize Groq API client
client = Groq(api_key="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")

# Initialize GitHub client
g = Github("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")
repo = g.get_user().get_repo("Chat")

# Function to make Jarvis speak
def jarvis_speak(text):
    engine.say(text)
    engine.runAndWait()

# Flask route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'JAYDEV' and password == 'ZALA':
            session['logged_in'] = True
            return redirect(url_for('chat'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')  # Assuming you have a login.html template for the login page

# Flask route for chat interface
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('chat.html')  # Assuming you have a chat.html template for the chat interface

# Flask route to handle incoming messages
@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message')
    if user_input:
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
        
        # Optionally, make Jarvis speak the response if voice command is enabled
        if session.get('voice_enabled'):
            jarvis_speak(response)
        
        return jsonify({"response": response})
    return jsonify({"error": "No message provided"}), 400

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
        session['voice_enabled'] = voice_enabled

        st.write("Enter your message below and Jarvis will respond.")
        user_message = st.text_input("Your Message")
        if st.button("Send Message"):
            if user_message:
                # Call Flask endpoint to process message
                response = send_message(user_message)
                st.write(f"Jarvis: {response.json().get('response')}")
                
                # Save the interaction to GitHub
                repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {response.json().get('response')}")
            else:
                st.write("Please enter a message.")
        else:
            st.write("The chatbot's responses will appear here.")

if __name__ == '__main__':
    # Running both Streamlit and Flask
    streamlit_app()
    app.run(debug=True)
