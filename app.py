from groq import Groq
import streamlit as st

# Create client
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# Title
st.title("Mini ChatBot App")
st.divider()

# Input
prompt = st.text_input("Ask anything")

# Button
gptbutton = st.button("Enter")

st.caption("Press Enter to proceed")
st.divider()

# Generate response
if gptbutton and prompt:

    with st.spinner("Generating response..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI tutor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.balloons()

        st.write(response.choices[0].message.content)