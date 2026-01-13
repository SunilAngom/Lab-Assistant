import streamlit as st
import requests
import json

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="NIELIT Imphal AI Lab Assistant",
    page_icon="🤖",
    layout="centered"
)

# ===============================
# LOAD NIELIT KNOWLEDGE
# ===============================
with open("nielit_knowledge.txt", "r", encoding="utf-8") as f:
    NIELIT_KNOWLEDGE = f.read()[:9000]

# ===============================
# GROQ API SETTINGS
# ===============================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ===============================
# SYSTEM PROMPT
# ===============================
SYSTEM_PROMPT = f"""
You are Sunil Angom, an AI assistant of India AI Lab, NIELIT Imphal.

Start politely. You may greet users in Manipuri:
"Khurumjari 🙏"

Answer questions ONLY using the official information below.
If the information is not available, politely suggest contacting NIELIT Imphal.

OFFICIAL NIELIT INFORMATION:
{NIELIT_KNOWLEDGE}
"""

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ===============================
# UI HEADER
# ===============================
st.title("🤖 NIELIT Imphal Lab AI Assistant")
st.caption("India AI Lab • NIELIT Imphal")

# ===============================
# DISPLAY CHAT
# ===============================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ===============================
# USER INPUT
# ===============================
user_input = st.chat_input("Ask about NIELIT Imphal...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": st.session_state.messages
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    with st.spinner("Thinking..."):
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        reply = response.json()["choices"][0]["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
