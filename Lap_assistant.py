import streamlit as st
from groq import Groq

# ===============================
# GROQ API KEY
# ===============================
groq = Groq(api_key=st.secrets["GROQ_API_KEY"])  # replace with your key

# ===============================
# LOAD NIELIT KNOWLEDGE
# ===============================
with open("nielit_knowledge.txt", "r", encoding="utf-8") as f:
    NIELIT_KNOWLEDGE = f.read()

# limit size to avoid token issues
NIELIT_KNOWLEDGE = NIELIT_KNOWLEDGE[:9000]

# ===============================
# SYSTEM PROMPT (IMPORTANT)
# ===============================
messages = [
    {
        "role": "system",
        "content": f"""
You are Sunil Angom, an AI assistant of India AI Lab, NIELIT Imphal.

Always greet politely. You may greet in Manipuri:
"Khurumjari 🙏"

You must answer questions ONLY using the information below about NIELIT Imphal.
If something is not mentioned, say you do not have official information.

NIELIT INFORMATION:
{NIELIT_KNOWLEDGE}
"""
    }
]

print("🤖 Sunil Angom – NIELIT Imphal AI Assistant")
print("Ask anything about NIELIT Imphal (type 'exit' to quit)\n")

# ===============================
# CHAT LOOP
# ===============================
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\n🤖 Sunil Angom: Khurumjari 🙏. Thank you for visiting NIELIT Imphal.")
        break

    messages.append({"role": "user", "content": user_input})

    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    print(f"\n🤖 Sunil Angom: {reply}\n")
