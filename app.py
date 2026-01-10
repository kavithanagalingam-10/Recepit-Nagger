import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="Gemini 1.5 Chatbot", layout="centered")
st.title("🚀 Gemini 2.5 Flash Chatbot")

# 2. Initialize the New Gemini Client
# Replace 'YOUR_API_KEY' or set it in your environment/secrets
API_KEY = "AIzaSyD8teRHHuWSFARwdr8aqkrJdueM-hUU3bc"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash" 

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input
if prompt := st.chat_input("Ask me anything..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # We pass the history to the model in the required format
            # The new SDK uses 'contents' rather than 'history' for simple calls
            response = client.models.generate_content_stream(
                model=MODEL_ID,
                contents=prompt
            )
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")