import os
import streamlit as st
from openai import OpenAI

# Set your API key (or ensure OPENAI_API_KEY is in your environment)
OPENAI_API_KEY = "xxxx"  #Replace with actual API key

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt for the chatbot
system_prompt = (
    "You are a helpful Moodle technical support chatbot. "
    "You provide clear, concise, and accurate answers to Moodle-related questions."
)

# Initialize conversation state if not already set
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Inject CSS to style the floating chat widget
st.markdown("""
<style>
.chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 350px;
    max-height: 500px;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
    border-radius: 10px;
    overflow: hidden;
    z-index: 9999;
    display: flex;
    flex-direction: column;
}
.chat-header {
    background-color: #0073aa;
    color: #fff;
    padding: 10px;
    font-weight: bold;
}
.chat-body {
    padding: 10px;
    flex: 1;
    overflow-y: auto;
}
.chat-input {
    border-top: 1px solid #ccc;
    padding: 10px;
}
.chat-input input[type="text"] {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
}
.chat-input button {
    width: 100%;
    margin-top: 5px;
    padding: 8px;
    background-color: #0073aa;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.chat-input button:hover {
    background-color: #005a8c;
}
</style>
""", unsafe_allow_html=True)

# Render the chat widget
with st.container():
    # Create a placeholder for our floating chat widget
    chat_container = st.empty()
    with chat_container.container():
        # Widget container start
        st.markdown('<div class="chat-widget">', unsafe_allow_html=True)
        st.markdown('<div class="chat-header">Moodle Support Chatbot</div>', unsafe_allow_html=True)
        
        # Build the conversation HTML from session state
        conversation_html = ""
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                conversation_html += f'<p><strong>User:</strong> {msg["content"]}</p>'
            elif msg["role"] == "assistant":
                conversation_html += f'<p><strong>Chatbot:</strong> {msg["content"]}</p>'
        st.markdown(f'<div class="chat-body">{conversation_html}</div>', unsafe_allow_html=True)
        
        # Chat input area
        st.markdown('<div class="chat-input">', unsafe_allow_html=True)
        user_message = st.text_input("", key="chat_input", placeholder="Type your message here...")
        if st.button("Send Chat"):
            # If user types exit/quit, clear conversation
            if user_message.lower() in ["exit", "quit"]:
                st.session_state.messages = [{"role": "system", "content": system_prompt}]
                st.experimental_rerun()
            else:
                # Append user's message to the conversation
                st.session_state.messages.append({"role": "user", "content": user_message})
                try:
                    response = client.chat.completions.create(
                        model="ft:gpt-4o-mini-2024-07-18:personal:moodle-bot-training-test1:BAYDWJiA",  # update as needed
                        messages=st.session_state.messages,
                        temperature=0.2,
                    )
                    answer = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": "Sorry, I'm having trouble responding right now."})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
