import streamlit as st
import openai

# Page Configuration
st.set_page_config(page_title="🔗 Financial Advisor Chatbot")
st.title('🦜🔗 Financial Advisor Chatbot')

# Initialize session state for storing chat messages if not already set
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Handling API Key securely and setup OpenAI client
if 'openai_api_key' not in st.secrets:
    openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key')
else:
    openai_api_key = st.secrets["openai_api_key"]

client = openai.OpenAI(api_key=openai_api_key)

def generate_response(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f"You: {prompt}")  # Display user message
    response = client.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use an appropriate model
        messages=st.session_state.messages
    )
    msg = response.choices[0].message['content']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.write(f"Assistant: {msg}")  # Display assistant response

# Main user input form
with st.form('user_input_form'):
    user_input = st.text_input('How can I assist you with your finances today?', '')
    submitted = st.form_submit_button('Submit')
    if submitted and user_input:
        generate_response(user_input)
