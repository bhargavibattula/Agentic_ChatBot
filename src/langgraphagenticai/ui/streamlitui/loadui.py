import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        # 1. Inject Modern SaaS CSS
        st.markdown("""
        <style>
        @import url('https://rsms.me/inter/inter.css');
        
        /* Global Styles */
        html, body, [class*="st-"] {
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #D1D5DB;
        }
        
        .stApp {
            background-color: #0F1117 !important;
        }

        /* Sidebar: Clean & Deep */
        [data-testid="stSidebar"] {
            background-color: #161922 !important;
            border-right: 1px solid #242933;
        }

        /* Typography */
        h1 {
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: #FFFFFF !important;
            margin-bottom: 2rem !important;
            font-size: 2.2rem !important;
        }

        /* Inputs & Selectors */
        div[data-baseweb="select"], .stTextInput > div > div > input {
            background-color: #1C212C !important;
            border: 1px solid #2D3544 !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }

        /* Primary Action Button */
        .stButton > button {
            background-color: #4F46E5 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #4338CA !important;
            transform: translateY(-1px);
        }

        /* Divider */
        hr { border-color: #2D3544 !important; }

        /* Card-style Containers */
        .content-card {
            background-color: #161922;
            border: 1px solid #242933;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        
        # Clean Greeting Logic
        from datetime import datetime
        hour = datetime.now().hour
        greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
        
        st.markdown(f"<h1>{greeting}, BHARU</h1>", unsafe_allow_html=True)
        
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            st.markdown("### Settings")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Intelligence", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("Groq API Key",type="password", placeholder="Paste key...")
            
            st.divider()
            
            self.user_controls["selected_usecase"]=st.selectbox("Mission Profile",usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "AI News"]:
                st.markdown("### Integrations")
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily API Key",type="password", placeholder="Paste key...")

            if self.user_controls['selected_usecase']=="AI News":
                st.markdown("### AI News Options")
                time_frame = st.selectbox("Timeline", ["Daily", "Weekly", "Monthly"], index=0)
                if st.button("Generate Dispatch", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_controls