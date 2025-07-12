import streamlit as st
import requests
import json
import time
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="CalmSpace - Mental Health AI Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .user-message {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 0.5rem;
    }
    
    .assistant-message {
        background: white;
        color: #2C3E50;
        margin-right: 20%;
        border-bottom-left-radius: 0.5rem;
        border: 1px solid #E3F2FD;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.1);
    }
    
    .crisis-message {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);
        color: white;
        margin-right: 20%;
        border-bottom-left-radius: 0.5rem;
        animation: crisisPulse 2s infinite;
    }
    
    .response-source {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        font-style: italic;
    }
    
    .assistant-message .response-source {
        border-top: 1px solid #E3F2FD;
        color: #5D6D7E;
    }
    
    .crisis-message .response-source {
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        color: rgba(255, 255, 255, 0.9);
    }
    
    @keyframes crisisPulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #E3F2FD;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
    }
    
    .stButton > button {
        border-radius: 25px;
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1976D2; margin-bottom: 0.5rem;">🌿 CalmSpace</h1>
        <p style="color: #5D6D7E; font-size: 1.1rem;">Your supportive mental health companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API key
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        
        # API key input
        api_key = st.text_input(
            "GROQ API Key",
            type="password",
            placeholder="Enter your GROQ API key here...",
            help="Get your API key from https://console.groq.com/"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API key configured!")
        else:
            st.warning("⚠️ Please enter your GROQ API key to start chatting")
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        
        if st.button("🆘 Crisis Resources"):
            st.markdown("""
            **Emergency Hotlines:**
            - National Suicide Prevention: 988
            - Crisis Text Line: Text HOME to 741741
            - Emergency Services: 911
            """)
        
        st.markdown("---")
        st.markdown("### 💡 About")
        st.markdown("""
        CalmSpace uses advanced AI to provide empathetic mental health support.
        
        **Features:**
        - 🧠 Emotion Detection
        - 🚨 Crisis Detection
        - 💙 Empathetic Responses
        - 📊 Dataset Integration
        """)
    
    # Main chat area
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "source" in message:
                    st.caption(f"💡 {message['source']}")
        
        # Chat input
        if prompt := st.chat_input("Share what's on your mind..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Check if API key is configured
            if not st.session_state.api_key:
                with st.chat_message("assistant"):
                    st.error("Please configure your GROQ API key in the sidebar to start chatting.")
                return
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = get_chat_response(prompt, st.session_state.messages)
                        st.markdown(response["message"])
                        if "source" in response:
                            st.caption(f"💡 {response['source']}")
                        
                        # Add to session state
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response["message"],
                            "source": response.get("source", "AI Generated")
                        })
                        
                    except Exception as e:
                        st.error(f"Sorry, I'm having trouble connecting. Please try again. Error: {str(e)}")

def get_chat_response(user_message, conversation_history):
    """Get response from the chatbot API"""
    
    # Prepare the request
    url = "https://your-backend-url.com/api/chat"  # Replace with your actual backend URL
    
    # For now, we'll simulate the response since we need to deploy the backend
    # In production, this would call your Flask backend
    
    # Simulate API call
    time.sleep(1)  # Simulate processing time
    
    # For demonstration, return a sample response
    return {
        "message": "I understand you're reaching out for support. That's a brave step. I'm here to listen and help you through whatever you're experiencing. Would you like to tell me more about what's on your mind?",
        "source": "AI Generated",
        "emotion": "neutral",
        "crisis_detected": False
    }

if __name__ == "__main__":
    main() 