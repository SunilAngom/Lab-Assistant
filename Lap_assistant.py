import streamlit as st
from groq import Groq

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="NIELIT Imphal AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ===============================
# LOAD NIELIT KNOWLEDGE
# ===============================
with open("nielit_knowledge.txt", "r", encoding="utf-8") as f:
    NIELIT_KNOWLEDGE = f.read()

# limit knowledge size (important for free tier)
NIELIT_KNOWLEDGE = NIELIT_KNOWLEDGE[:3000]

# ===============================
# GROQ CLIENT (FROM SECRETS)
# ===============================
groq = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
st.title("🤖 NIELIT Imphal AI Assistant")
st.caption("India AI Lab • NIELIT Imphal")

# ===============================
# DISPLAY CHAT HISTORY
# ===============================
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
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

    # get AI response
    with st.spinner("Thinking..."):
        response = groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

    # save & show assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
