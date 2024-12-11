from flask import Flask, request, jsonify
import pyttsx3
from groq import Groq
import streamlit as st
from github import Github

# Initialize the Flask app
app = Flask(__name__)

# Initialize the speech engine for Jarvis voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Initialize Groq API client
client = Groq(api_key="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")

# Initialize GitHub client
g = Github("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")
repo = g.get_user().get_repo("Chat")

# Function to make Jarvis speak
def jarvis_speak(text):
    engine.say(text)
    engine.runAndWait()

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
        
        # Optionally, make Jarvis speak the response
        jarvis_speak(response)
        
        return jsonify({"response": response})
    return jsonify({"error": "No message provided"}), 400

# Streamlit integration
def streamlit_app():
    st.title("Jarvis Chat with Groq Integration")
    st.write("Enter your message below and Jarvis will respond.")
    
    user_message = st.text_input("Your Message")
    if st.button("Send Message"):
        if user_message:
            # Call Flask endpoint to process message
            response = send_message(user_message)
            st.write(f"Jarvis: {response.json().get('response')}")
            
            # Optionally save the interaction to GitHub
            repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {response.json().get('response')}")
        else:
            st.write("Please enter a message.")

if __name__ == '__main__':
    # Running both Streamlit and Flask
    streamlit_app()
    app.run(debug=True)
