import streamlit as st
import time
import openai  # Directly import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Configure Streamlit page
st.set_page_config(page_title="🔗 DoaIbu OpenMachine Chatbot")
st.title('🦜🔗 DoaIbu OpenMachine Chatbot as Your Personal Financial Advisor')

# OpenAI API key configuration
openai_api_key = st.sidebar.text_input('OpenAI API Key, email mira@openmachine.co if you need it')
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Define function to generate chatbot responses
def generate_response(input_text):
    input_text_lower = input_text.lower()
    if "saldo" in input_text_lower:
        response = "Haloo Kak Mira.. Saldo anda 2.2 juta rupiah saat ini"
    elif "bayar iuran pln" in input_text_lower:
        response = "Transaksi saat ini terkonfirmasi oleh suara anda, nominal RP. 750.000 telah ter-debet oleh akun anda ke pembayaran listrik PLN, saldo Kakak saat ini 1.45 juta Rupiah"
    elif "plan investasi" in input_text_lower or "investasi" in input_text_lower:
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
        response = "Maaf, saya tidak mengerti pertanyaan Anda. Bisa Anda ulangi dengan lebih jelas?"

    # Store the conversation history
    st.session_state['chat_history'].append(HumanMessage(content=input_text))
    st.session_state['chat_history'].append(AIMessage(content=response))
    return response

# Layout for displaying chat history and input form
st.subheader("Conversation History")
for message in st.session_state['chat_history']:
    if isinstance(message, HumanMessage):
        st.text_area("You said:", value=message.content, height=75, key=str(message))
    elif isinstance(message, AIMessage):
        st.text_area("Bot said:", value=message.content, height=75, key=str(message))

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
