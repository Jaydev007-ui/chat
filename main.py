import streamlit as st
from groq import Groq
from github import Github
import os

# Initialize Groq API client
client = Groq(api_key="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")

# Initialize GitHub client
g = Github("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")
repo = g.get_user().get_repo("chat")

# Streamlit integration
def streamlit_app():
    st.image("TSS.png", width=200)  # Display the logo
    st.title("Jarvis Chat with Groq Integration")
    
    # Login section
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.chat_history = []  # Store chat history in session state
    
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
        # Chat interface
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

                # Update chat history
                st.session_state.chat_history.append((user_message, response))

                # Display chat history
                st.write("Chat History:")
                for i, (msg, resp) in enumerate(st.session_state.chat_history):
                    st.write(f"**You:** {msg}")
                    st.write(f"**Jarvis:** {resp}")
                    st.write("---")

                # Save the interaction to GitHub
                repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {response}")
            else:
                st.write("Please enter a message.")

if __name__ == '__main__':
    streamlit_app()
