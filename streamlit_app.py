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

    if not st.session_state['chat_history']:
        system_message = SystemMessage(
            content="You are a helpful financial advisor who helps people make good financial decisions. "
        )
        messages = [system_message, HumanMessage(content=input_text)] 
    else:
        messages = st.session_state['chat_history'] + [HumanMessage(content=input_text)]

    result = chat(messages)  # No need for system message if it's already in history
    response = result.content
    st.session_state['chat_history'].append(HumanMessage(content=input_text))
    st.session_state['chat_history'].append(AIMessage(content=response))
    return response



# Display previous interactions
st.subheader("Conversation History")
for message in st.session_state['chat_history']:
    if isinstance(message, HumanMessage):
        st.text_area("You said:", value=message.content, height=75, key=str(message))
    elif isinstance(message, AIMessage):
        st.text_area("Bot said:", value=message.content, height=75, key=str(message))

# Quick questions
st.subheader("Quick Questions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Plan My Spending"):
        st.session_state['input_text'] = "What's a good spending plan for this month?"
with col2:
    if st.button("Investment Advice"):
        st.session_state['input_text'] = "Can you give me some investment advice?"
with col3:
    if st.button("Check My Balance"):
        st.session_state['input_text'] = "What's my current account balance?"  # This will be a placeholder response
with col4:
    if st.button("Plan Future Savings"):
        st.session_state['input_text'] = "How should I plan my savings for the next year?"

# Main user input form
with st.form('my_form'):
    text = st.text_area(
        'How can I assist you with your finances today?',
        value=st.session_state.get('input_text', 'Type your question here...'),
        height=150  # Increased height for better user experience
    )
    submitted = st.form_submit_button('Submit')

    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        else:
            response = generate_response(text)
            st.text_area("Bot's response:", value=response, height=100)
