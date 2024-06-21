import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Session state initialization for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page Configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot as Your Personal Financial Advisor')

# Sidebar configurations for OpenAI parameters
openai_api_key = st.sidebar.text_input('OpenAI API Key, email naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Function to generate responses using OpenAI API
def generate_response(input_text):
    chat = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)
    
    # Check if chat history is empty to give instructions to the model. 
    if not st.session_state['chat_history']:
        system_message = SystemMessage(
            content="You are a helpful financial advisor who helps people make good financial decisions. "
        )
    else: 
        system_message = None 

    # Combine chat history with new user input in a format understandable by the LLM
    messages = st.session_state['chat_history'] + [HumanMessage(content=input_text)]

    result = chat(messages, system_message)
    response = result.content
    st.session_state['chat_history'].append(HumanMessage(content=input_text))
    st.session_state['chat_history'].append(AIMessage(content=response))
    return response

# ... (rest of the code for conversation history, quick buttons, and user input form)
