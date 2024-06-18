import streamlit as st
from langchain.llms import OpenAI  # Ensure this import is correct based on langchain documentation

# Page Configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot')

# Sidebar for API Key and Parameters
openai_api_key = st.sidebar.text_input('OpenAI API Key, tell naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider('Maximum Tokens', min_value=1, max_value=500, value=256)
top_p = st.sidebar.slider('Top P', min_value=0.0, max_value=1.0, value=1.0)
frequency_penalty = st.sidebar.slider('Frequency Penalty', min_value=0.0, max_value=2.0, value=0.0)
presence_penalty = st.sidebar.slider('Presence Penalty', min_value=0.0, max_value=2.0, value=0.0)

# Function to Generate Responses
def generate_response(input_text):
    llm = OpenAI(temperature=temperature, openai_api_key=openai_api_key, max_tokens=max_tokens, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty)
    response = llm.generate_response(input_text)  # Assuming the method to call is generate_response
    st.info(response)

# Main Form
with st.form('my_form'):
    text = st.text_area('Enter text:', 'How is the financial situation currently progressing?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        else:
            generate_response(text)
