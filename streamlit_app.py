import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title="🦜🔗 Financial Advisor Bot")
st.title('🦜🔗 Financial Advisor Bot')

# Check if history exists in the session state, if not initialize it
if 'history' not in st.session_state:
    st.session_state['history'] = []

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
    # Context initialization for the financial advisor
    context = "You are a personalized financial advisor specialized in banking and payment services. "
    full_prompt = context + " ".join(st.session_state['history']) + input_text
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    response = llm.generate_response(full_prompt)  # Assuming the method to generate response
    st.session_state['history'].append("Question: " + input_text)
    st.session_state['history'].append("Answer: " + response)
    return response

with st.form('my_form'):
    text = st.text_area('Enter your question:', placeholder='Ask me anything about banking or payments...')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠️')
        else:
            response = generate_response(text)
            st.info(response)

# Optionally, display the chat history
if st.checkbox('Show chat history'):
    st.write('\n'.join(st.session_state['history']))
