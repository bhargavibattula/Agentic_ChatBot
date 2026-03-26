import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        # MUST be the absolute first Streamlit command
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide", page_icon="🤖")

        # 1. Inject Premium High-End CSS
        st.markdown("""
        <style>
        @import url('https://rsms.me/inter/inter.css');
        
        /* Base Styles */
        html, body, [class*="st-"] {
            font-family: 'Inter', -apple-system, system-ui, sans-serif !important;
            color: #1a1a1b !important;
        }
        
        /* App Background */
        .stApp {
            background: #FFFFFF !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F8F9FA !important;
            border-right: 1px solid #E5E7EB;
        }
        
        /* Sidebar Action Button */
        .new-chat-btn {
            background: white;
            border: 1px solid #E5E7EB;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .new-chat-btn:hover {
            background: #F3F4F6;
        }

        /* Typography */
        h1 {
            font-weight: 600 !important;
            letter-spacing: -0.01em !important;
            color: #000000 !important;
            font-size: 2rem !important;
            text-align: center;
            margin-top: 4rem !important;
            margin-bottom: 3rem !important;
        }
        
        /* Input Area Container (Simulated) */
        .chat-input-container {
            max-width: 768px;
            margin: 0 auto;
            position: relative;
        }

        /* Message Bubbles / Cards */
        .chat-bubble {
            max-width: 800px;
            margin: 1.5rem auto;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            line-height: 1.6;
        }
        
        .user-bubble {
            background-color: #F4F4F4;
            color: #000000;
        }
        
        .assistant-bubble {
            background-color: transparent;
            color: #000000;
            border-left: 2px solid #10a37f;
        }

        /* Form Inputs & Buttons */
        div[data-baseweb="select"], .stTextInput > div > div > input {
            border: 1px solid #E5E7EB !important;
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s;
        }
        
        /* Primary CTA: Like ChatGPT's Green */
        .stButton > button[kind="primary"] {
            background-color: #10a37f !important;
            color: white !important;
            border: none;
        }
        
        .stButton > button:hover {
            opacity: 0.9;
            transform: scale(0.98);
        }

        /* Hide elements for cleaner UI */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Horizontal Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #D1D5DB;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Sidebar Actions
        with st.sidebar:
            st.markdown("""
            <div style="background: white; border: 1px solid #E5E7EB; padding: 10px; border-radius: 8px; margin-bottom: 20px; font-weight: 500; display: flex; align-items: center; justify-content: space-between;">
                <span>New Chat</span>
                <span style="font-size: 1.2rem;">+</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Configuration")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Brain Engine", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Model Architecture", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("Access Secret (API Key)",type="password", placeholder="Bearer sk-...")
            
            st.divider()
            
            self.user_controls["selected_usecase"]=st.selectbox("Operations Profile",usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "AI News"]:
                st.markdown("### External Connections")
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily Token",type="password", placeholder="Paste token here...")

            if self.user_controls['selected_usecase']=="AI News":
                st.markdown("### Pipeline Delivery")
                time_frame = st.selectbox("Update Cycle", ["Daily", "Weekly", "Monthly"], index=0)
                if st.button("Initialize News Pipeline", use_container_width=True, type="primary"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        # Main Area
        from datetime import datetime
        hour = datetime.now().hour
        greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
        
        st.markdown(f"<h1>{greeting}, BHARU.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6B7280; margin-top: -2rem; margin-bottom: 3rem;'>What's on the agenda today?</p>", unsafe_allow_html=True)
        
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        return self.user_controls