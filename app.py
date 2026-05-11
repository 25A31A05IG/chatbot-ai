import streamlit as st
from groq import Groq
import time

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.stChatMessage {
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.block-container {
    padding-top: 2rem;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GROQ CLIENT ---------------- #

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("---")

    model = st.selectbox(
        "Choose AI Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768"
        ]
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption("🚀 Built with Groq + Streamlit")

# ---------------- TITLE ---------------- #

st.title("🤖 AI Chatbot")
st.caption("Fast AI Assistant powered by Groq")

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- WELCOME MESSAGE ---------------- #

if len(st.session_state.messages) == 0:
    st.info("👋 Hello! Ask me anything.")

# ---------------- DISPLAY CHAT HISTORY ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ---------------- #

prompt = st.chat_input("Type your message here...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024
                )

                reply = response.choices[0].message.content

                # Typing animation
                placeholder = st.empty()

                full_response = ""

                for word in reply.split():

                    full_response += word + " "

                    time.sleep(0.03)

                    placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response
                    }
                )

            except Exception as e:

                st.error(f"Error: {e}")
