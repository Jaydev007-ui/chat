import requests
import streamlit as st

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
                # Call Flask API to process message
                response = requests.post("http://localhost:5000/send_message", json={'message': user_message})
                jarvis_response = response.json().get('response')
                st.write(f"Jarvis: {jarvis_response}")

                # Save the interaction to GitHub
                repo.create_file(f"logs/{user_message[:10]}.txt", "Added message log", f"Message: {user_message}\nResponse: {jarvis_response}")
            else:
                st.write("Please enter a message.")
        else:
            st.write("The chatbot's responses will appear here.")

if __name__ == '__main__':
    streamlit_app()
