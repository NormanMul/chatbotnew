import streamlit as st
import time
from openai.error import RateLimitError
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
openai_api_key = st.sidebar.text_input('OpenAI API Key, email mira@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Function to generate responses using OpenAI API
def generate_response(input_text):
    # Predefined responses for specific requests
    if input_text.lower() == "bagaimana saldo saya":
        response = "Haloo Kak Mira.. Saldo anda 2.2 juta rupiah saat ini"
    elif input_text.lower() == "tolong bayar iuran pln bulan ini":
        response = "Transaksi saat ini terkonfirmasi oleh suara anda, nominal RP. 750.000 telah ter-debet oleh akun anda ke pembayaran listrik PLN, saldo Kakak saat ini 1.45 juta Rupiah"
    elif "plan investasi" in input_text.lower():
        response = """Untuk membuat rencana investasi dengan saldo sebesar 1,4 juta rupiah pada bulan ini, berikut adalah rencana yang bisa kamu pertimbangkan:
        
1. Dana Darurat (20%) - Rp 280,000
Instrumen: Reksa dana pasar uang atau tabungan berjangka.
Tujuan: Menyimpan dana ini sebagai cadangan jika terjadi keadaan darurat yang memerlukan uang tunai cepat.

2. Investasi Jangka Pendek (30%) - Rp 420,000
Instrumen: Reksa dana pendapatan tetap atau tabungan emas.
Tujuan: Mengamankan modal dengan potensi keuntungan sedikit lebih tinggi dari pasar uang, bisa digunakan dalam 1-2 tahun ke depan.

3. Investasi Jangka Menengah (30%) - Rp 420,000
Instrumen: Reksa dana campuran atau saham blue chip.
Tujuan: Menumbuhkan modal dengan risiko yang lebih tinggi, disarankan untuk dipegang dalam 3-5 tahun ke depan.

4. Investasi Jangka Panjang (20%) - Rp 280,000
Instrumen: Reksa dana saham atau saham individual di perusahaan dengan fundamental kuat.
Tujuan: Menumbuhkan modal secara signifikan dengan toleransi risiko yang lebih tinggi, cocok untuk tujuan keuangan 5 tahun atau lebih."""
    else:
        # Handle other queries with OpenAI API
        retries = 3
        for attempt in range(retries):
            try:
                chat = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)
                system_message = SystemMessage(content="You are a helpful financial advisor who helps people make good financial decisions.")
                messages = [system_message, HumanMessage(content=input_text)]
                result = chat(messages)
                response = result.content
                break
            except RateLimitError:
                if attempt < retries - 1:
                    wait = 2 ** attempt
                    time.sleep(wait)
                else:
                    response = "Sorry, I'm unable to process your request right now due to rate limits. Please try again later."
                    break

    # Store the conversation history
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
        st.session_state['input_text'] = "What's my current account balance?"
with col4:
    if st.button("Plan Future Savings"):
        st.session_state['input_text'] = "How should I plan my savings for the next year?"

# Main user input form
with st.form('my_form'):
    text = st.text_area(
        'How can I assist you with your finances today?',
        value=st.session_state.get('input_text', 'Type your question here...'),
        height=150
    )
    submitted = st.form_submit_button('Submit')
    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        else:
            response = generate_response(text)
            st.text_area("Bot's response:", value=response, height=100)
