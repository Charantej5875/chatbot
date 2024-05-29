import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model configuration and safety settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Create the GenerativeModel instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        "You are designed to help children under 18 reinforce AI concepts learned in class, "
        "including AI and generative AI. You provide summaries, practice exercises, quizzes, "
        "and coding challenges with instant feedback to enhance understanding. You answer AI-related "
        "questions with clear explanations and direct students to additional resources if needed. "
        "Using age-appropriate language and interactive elements like coding games, you keep students "
        "engaged and encourage curiosity. You ensure safe, respectful interactions without collecting "
        "personal information, and use moderation to prevent inappropriate content. Tailor your responses "
        "to suit different age groups and learning levels, and praise students for their efforts to foster "
        "a love for learning AI."
    ),
)

# Initialize Streamlit app
st.set_page_config(page_title="Chat bot")
st.header("Chat bot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to get responses from the model
def get_gemini_response(question):
    chat_session = model.start_chat(history=st.session_state['chat_history'])
    response = chat_session.send_message(question)
    return response

# User input and button
input_text = st.text_input("Ask a question:", key="input")
submit = st.button("Enter")

if submit and input_text:
    # Get the response from the model
    response = get_gemini_response(input_text)
    
    # Add user query and response to chat history
    st.session_state['chat_history'].append({"role": "user", "content": input_text})
    st.session_state['chat_history'].append({"role": "assistant", "content": response.text})

    # Display the response
    st.subheader("Response")
    st.write(response.text)

# Display chat history
st.subheader("Chat History")
for message in st.session_state['chat_history']:
    st.write(f"{message['role'].capitalize()}: {message['content']}")
