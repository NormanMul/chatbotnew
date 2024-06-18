import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title="🦜🔗 Financial Advisor Bot")
st.title('🦜🔗 Financial Advisor Bot')

# Initialize session state for chat history and API key if not already done
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

# Function to generate responses using OpenAI
def generate_response(input_text):
    context = "You are a personalized financial advisor specialized in banking and payment services. "
    full_prompt = context + " ".join(st.session_state['history']) + input_text
    llm = OpenAI(temperature=0.7, openai_api_key=st.session_state['api_key'])
    response = llm.generate_response(full_prompt)  # Modify this line according to the actual function you have
    st.session_state['history'].append("Question: " + input_text)
    st.session_state['history'].append("Answer: " + response)
    return response

# Sidebar for API key input
api_key_input = st.sidebar.text_input('OpenAI API Key', value=st.session_state['api_key'])
if api_key_input:
    st.session_state['api_key'] = api_key_input

with st.form('my_form'):
    text = st.text_area('Enter your question:', placeholder='Ask me anything about banking or payments...')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not st.session_state['api_key'].startswith('sk-'):
            st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        else:
            response = generate_response(text)
            st.info(response)

# Display chat history if checkbox is checked
if st.checkbox('Show chat history'):
    st.write('\n'.join(st.session_state['history']))
