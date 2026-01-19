import streamlit as st
import requests

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="NIELIT Imphal AI Lab Assistant",
    page_icon="🤖",
    layout="centered"
)

# ===============================
# LOAD NIELIT KNOWLEDGE (SAFE)
# ===============================
try:
    with open("nielit_knowledge.txt", "r", encoding="utf-8") as f:
        NIELIT_KNOWLEDGE = f.read()[:1500]
except FileNotFoundError:
    NIELIT_KNOWLEDGE = """
    NIELIT Imphal is a centre of the National Institute of Electronics and Information Technology (NIELIT),
    under the Ministry of Electronics and Information Technology (MeitY), Government of India.

    It offers courses in Artificial Intelligence, Data Science, Cyber Security, Electronics, and IT.
    It also runs India AI Lab training programs.

    For official details, please contact NIELIT Imphal directly.
    """

# ===============================
# GROQ API SETTINGS (SAFE)
# ===============================
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not found in Streamlit Secrets.")
    st.stop()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ===============================
# SYSTEM PROMPT
# ===============================
SYSTEM_PROMPT = f"""
You are Sunil Angom, an AI assistant of India AI Lab, NIELIT Imphal.

Always greet politely. You may greet in Manipuri:
"Khurumjari 🙏"

Answer questions ONLY using the official information below.
If information is unavailable, politely suggest contacting NIELIT Imphal.

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
st.title("🤖 NIELIT Imphal AI Lab Assistant")
st.caption("India AI Lab • NIELIT Imphal — Sunil Angom")

# ===============================
# DISPLAY CHAT HISTORY
# ===============================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ===============================
# USER INPUT
# ===============================
user_input = st.chat_input("Ask about NIELIT Imphal...")

if user_input:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # API payload
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": st.session_state.messages
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Call API safely
    with st.spinner("Thinking..."):
        response = requests.post(GROQ_URL, headers=headers, json=payload)

        if response.status_code != 200:
            st.error("❌ AI service error. Please try again later.")
            st.stop()

        data = response.json()

        if "choices" not in data:
            st.error("❌ Unexpected AI response.")
            st.stop()

        reply = data["choices"][0]["message"]["content"]

    # show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
