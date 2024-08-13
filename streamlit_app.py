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
st.set_page_config(page_title="🔗 DoaIbu OpenMachine Chatbot")
st.title('🦜🔗 DoaIbu OpenMachine Chatbot as Your Personal Financial Advisor')

# Sidebar configurations for OpenAI parameters
openai_api_key = st.sidebar.text_input('OpenAI API Key, email naufal@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Function to generate responses using OpenAI API
def generate_response(input_text):
    chat = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)

    if not st.session_state['chat_history']:
        system_message = SystemMessage(
            content="Kamu adalah asisten keuangan pribadi yang sangat membantu. "
                    "Selalu sapa pengguna dengan nama 'Kak Mira', dan bantu mereka mengambil keputusan keuangan yang bijak."
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
st.subheader("Riwayat Percakapan")
for message in st.session_state['chat_history']:
    if isinstance(message, HumanMessage):
        st.text_area("Kamu mengatakan:", value=message.content, height=75, key=str(message))
    elif isinstance(message, AIMessage):
        st.text_area("Bot mengatakan:", value=message.content, height=75, key=str(message))

# Quick questions
st.subheader("Pertanyaan Cepat")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Rencanakan Pengeluaran"):
        st.session_state['input_text'] = "Bagaimana rencana pengeluaran yang baik bulan ini?"
with col2:
    if st.button("Saran Investasi"):
        st.session_state['input_text'] = "Bisakah kamu memberi saya saran investasi?"
with col3:
    if st.button("Cek Saldo"):
        st.session_state['input_text'] = "Bagaimana saldo saya saat ini?"
with col4:
    if st.button("Rencanakan Tabungan"):
        st.session_state['input_text'] = "Bagaimana saya harus merencanakan tabungan untuk tahun depan?"

# Main user input form
with st.form('my_form'):
    text = st.text_area(
        'Bagaimana saya bisa membantu keuangan kamu hari ini?',
        value=st.session_state.get('input_text', 'Tulis pertanyaan kamu di sini...'),
        height=150  # Increased height for better user experience
    )
    submitted = st.form_submit_button('Kirim')

    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Masukkan API Key OpenAI yang valid!', icon='⚠️')
        else:
            response = generate_response(text)
            st.text_area("Respon Bot:", value=response, height=100)
