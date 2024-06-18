import streamlit as st
from langchain.llms import OpenAI  # Verify this import based on your project dependencies

# Setting the page configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot')

# Sidebar configurations
openai_api_key = st.sidebar.text_input('OpenAI API Key, email naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider('Maximum Tokens', min_value=100, max_value=1000, value=256, step=50)
top_p = st.sidebar.slider('Top P', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
frequency_penalty = st.sidebar.slider('Frequency Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)
presence_penalty = st.sidebar.slider('Presence Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)

# Function to generate responses using OpenAI API
def generate_response(input_text):
    llm = OpenAI(api_key=openai_api_key, temperature=temperature, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
    response = llm.generate_response(input_text)  # Ensure generate_response is the correct method to use
    st.info(response)

# Main user input form
with st.form('my_form'):
    text = st.text_area('Enter text:', 'How is the financial situation currently progressing?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        else:
            generate_response(text)
