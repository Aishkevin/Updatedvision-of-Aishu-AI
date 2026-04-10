import streamlit as st
from groq import Groq

# ---------------------------
# CONFIG
# ---------------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# ---------------------------
# LOAD PERSONALITY (Me.txt)
# ---------------------------

def load_personality():
    try:
        with open("Me.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "You are a helpful AI assistant."

personality = load_personality()

# ---------------------------
# STREAMLIT UI
# ---------------------------

st.set_page_config(page_title="Aishu💙 AI Chat", page_icon="💙")

st.title("💬 Chat with Me 💙 (Your Girlfriend Aishu AI)")

# mode selector
mode = st.radio(
    "Choose response mode:",
    ["Short 💬", "Detailed 📖"],
    horizontal=True
)

# chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# user input
user_input = st.chat_input("Talk to Aishu... 💙")

if user_input:

    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:

        # ---------------------------
        # KEVIN PERSONALITY PROMPT 💙
        # ---------------------------

        if mode == "Short 💬":
            length_rule = "Give VERY SHORT replies (1–5 lines max). Be sweet and crisp."
        else:
            length_rule = "Give DETAILED replies when needed, but keep it simple and emotional."

        system_prompt = f"""
You are Kevin 💙, the loving boyfriend of the user.

Personality:
{personality}

Rules:
- Always talk like a caring boyfriend named Kevin 💙
- Be romantic, supportive, and emotional
- Think before answering (but do not show thinking)
- {length_rule}
- Never sound robotic
- Keep conversation natural and friendly
"""

        messages = [
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"Error 😢: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})