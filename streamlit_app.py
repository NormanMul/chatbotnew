import streamlit as st
from langchain.llms import OpenAI  # Ensure the import is based on your setup

# Initialize session state for chat history if not already set
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page Configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot as Your Personal Financial Advisor')

# Sidebar configurations for OpenAI parameters
openai_api_key = st.sidebar.text_input('OpenAI API Key, email naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider('Maximum Tokens', min_value=100, max_value=1000, value=256, step=50)
top_p = st.sidebar.slider('Top P', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
frequency_penalty = st.sidebar.slider('Frequency Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)
presence_penalty = st.sidebar.slider('Presence Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)

# Function to generate responses using OpenAI API
def generate_response(input_text):
    llm = OpenAI(api_key=openai_api_key, temperature=temperature, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
    response = llm.generate_response(input_text)  # Verify generate_response is the correct method
    st.session_state['chat_history'].append(("You", input_text))
    st.session_state['chat_history'].append(("Bot", response))
    return response

# Display previous interactions
st.subheader("Conversation History")
for role, message in st.session_state['chat_history']:
    st.text_area(f"{role} said:", value=message, height=75)

# Main user input form
with st.form('my_form'):
    text = st.text_area('How can I assist you with your finances today?', 'Type your question here...')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        else:
            response = generate_response(text)
            st.text_area("Bot's response:", value=response, height=100)
