import streamlit as st
from groq import Groq
import requests

# Groq API setup
client = Groq(api_key="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")

# GitHub setup
username = "Jaydev007-ui"
token = "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"
repo_name = "Chat"

# Streamlit interface
st.title("AI Chat with Groq and GitHub Integration")
st.write("Ask a question, and the system will respond based on Groq's AI model!")

question = st.text_input("Enter your question:", "What is numpy?")

if question:
    # Send request to Groq API
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a college professor providing professional answers to students of CSE which are short and concise"
            },
            {
                "role": "user",
                "content": question
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

    st.write("**Answer:**")
    st.write(response)

    # Save answer to GitHub repository
    commit_message = f"Added answer for: {question}"
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{question}.txt"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    data = {
        "message": commit_message,
        "content": response.encode("utf-8").decode("utf-8"),  # base64 encode the content
    }
    
    # Make the request to create/update file on GitHub
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        st.success("Answer saved to GitHub!")
    else:
        st.error("Error saving to GitHub!")
