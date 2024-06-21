import streamlit as st
import openai

# Initialize session state for chat history if not already set
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page Configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot as Your Personal Financial Advisor')

# Handling API Key securely
if 'openai_api_key' not in st.secrets:
    openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key')
else:
    openai_api_key = st.secrets["openai_api_key"]

openai.api_key = openai_api_key

# Sidebar configurations for model parameters
temperature = st.sidebar.slider('Temperature', 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider('Maximum Tokens', 100, 1000, 256, 50)
top_p = st.sidebar.slider('Top P', 0.0, 1.0, 1.0, 0.1)
frequency_penalty = st.sidebar.slider('Frequency Penalty', 0.0, 2.0, 0.0, 0.1)
presence_penalty = st.sidebar.slider('Presence Penalty', 0.0, 2.0, 0.0, 0.1)

def generate_response(input_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Use an appropriate engine name
            prompt=input_text,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        answer = response['choices'][0]['text'].strip()
        st.session_state['chat_history'].append(("You", input_text))
        st.session_state['chat_history'].append(("Bot", answer))
        return answer
    except Exception as e:
        return str(e)  # For debugging purposes

# Display and other interactive elements follow...
