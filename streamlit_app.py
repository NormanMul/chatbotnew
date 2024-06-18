import streamlit as st
from langchain.llms import OpenAI  # Ensure this import is correct based on langchain documentation

st.set_page_config(page_title="🔗 DoaIbu Chatbot ")
st.title('🦜🔗 DoaIbu Chatbot')

openai_api_key = st.sidebar.text_input('OpenAI API Key, tell naufal@openmachine.co if you need it')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    response = llm.generate_response(input_text)  # Assuming the method to call is generate_response
    st.info(response)

with st.form('my_form'):
    text = st.text_area('Enter text:', 'bagaimana perkembangan keadaan finansial saat ini')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        else:
            generate_response(text)
