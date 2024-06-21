import streamlit as st
import openai

# Ensure the OpenAI API key is set directly using the client configuration
openai.api_key = st.secrets["openai_api_key"]

# Initialize session state for chat history if not already set
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Page Configuration
st.set_page_config(page_title="🔗 DoaIbu Chatbot")
st.title('🦜🔗 DoaIbu Chatbot as Your Personal Financial Advisor')

# Sidebar configurations
temperature = st.sidebar.slider('Temperature', 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider('Maximum Tokens', 100, 1000, 256, 50)
top_p = st.sidebar.slider('Top P', 0.0, 1.0, 1.0, 0.1)
frequency_penalty = st.sidebar.slider('Frequency Penalty', 0.0, 2.0, 0.0, 0.1)
presence_penalty = st.sidebar.slider('Presence Penalty', 0.0, 2.0, 0.0, 0.1)

def generate_response(input_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Confirm this engine name based on your API subscription
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

# Conversation history display
st.subheader("Conversation History")
for role, message in st.session_state['chat_history']:
    st.text_area(f"{role} said:", value=message, height=75)

# Quick questions for user convenience
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
        st.session_state['input_text'] = "What's my current account balance?"
with col4:
    if st.button("Plan Future Savings"):
        st.session_state['input_text'] = "How should I plan my savings for the next year?"

# Main user input form
with st.form('my_form'):
    text = st.text_area('How can I assist you with your finances today?', value=st.session_state.get('input_text', 'Type your question here...'))
    submitted = st.form_submit_button('Submit')
    if submitted:
        response = generate_response(text)
        st.text_area("Bot's response:", value=response, height=100)
