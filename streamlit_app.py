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
# Sidebar configurations
openai_api_key = st.sidebar.text_input('OpenAI API Key, email naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)
max_tokens = st.sidebar.slider('Maximum Tokens', min_value=100, max_value=1000, value=256, step=50)
top_p = st.sidebar.slider('Top P', min_value=0.0, max_value=1.0, value=1.0, step=0.1)
frequency_penalty = st.sidebar.slider('Frequency Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)
presence_penalty = st.sidebar.slider('Presence Penalty', min_value=0.0, max_value=2.0, value=0.0, step=0.1)

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
