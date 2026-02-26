import streamlit as st
from openai import OpenAI

# 1. Konfigurasi Tampilan Website
st.set_page_config(page_title="Bot", page_icon="🤖")
st.title("🤖 Moving")
st.caption("Ditenagai oleh DeepSeek melalui OpenRouter")

# 2. Setup API (Ganti 'ISI_API_KEY_LO' dengan key dari OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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", 
)

# 3. Inisialisasi Memori Chat (Biar gak lupa konteks)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Tampilkan Riwayat Chat di Layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Logika Utama Chat
if prompt := st.chat_input("Tanya apa saja, brok..."):
    # Simpan chat user ke memori
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ambil respon dari DeepSeek
    with st.chat_message("assistant"):
        with st.spinner("Si DeepSeek lagi mikir..."):
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat", # Lo bisa ganti ke 'deepseek/deepseek-r1' kalau mau versi lebih pinter
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
    
    # Simpan respon AI ke memori
    st.session_state.messages.append({"role": "assistant", "content": full_response})