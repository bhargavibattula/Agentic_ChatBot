import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        # MUST be the absolute first Streamlit command
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide", page_icon="⚡")

        # 1. Inject Extra-Ordinary SaaS CSS
        st.markdown("""
        <style>
        @import url('https://rsms.me/inter/inter.css');
        
        /* Global Reset & Base */
        html, body, [class*="st-"] {
            font-family: 'Inter', -apple-system, system-ui, sans-serif !important;
            color: #1E293B !important;
        }
        
        .stApp {
            background: linear-gradient(135deg, #FDFDFD 0%, #F1F5F9 100%) !important;
        }

        /* Extraordinary Sidebar */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
            box-shadow: 10px 0 30px rgba(0,0,0,0.02);
        }
        
        /* Modern Sidebar Elements */
        .sidebar-brand {
            padding: 1.5rem 0;
            font-weight: 800;
            font-size: 1.4rem;
            background: linear-gradient(45deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            text-align: center;
        }

        /* Typography */
        h1 {
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            color: #0F172A !important;
            font-size: 3rem !important;
            text-align: center;
            margin-top: 5rem !important;
            margin-bottom: 3.5rem !important;
            background: linear-gradient(90deg, #0F172A 0%, #475569 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Modern Chat Bubbles */
        .chat-bubble {
            max-width: 850px;
            margin: 2rem auto;
            padding: 1.25rem 1.75rem;
            border-radius: 16px;
            line-height: 1.7;
            position: relative;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .chat-bubble:hover {
            transform: translateY(-2px);
        }
        
        .user-bubble {
            background-color: #FFFFFF;
            border: 1px solid #F1F5F9;
            color: #334155;
            border-bottom-right-radius: 4px;
        }
        
        .assistant-bubble {
            background-color: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            color: #0F172A;
            border-bottom-left-radius: 4px;
        }

        /* Avatar System */
        .avatar-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        
        .avatar-user { color: #6366F1; }
        .avatar-ai { color: #10B981; }

        /* Fancy Status Indicator */
        div[data-testid="stStatus"] {
            border: none !important;
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        }

        /* Enhanced Inputs */
        div[data-baseweb="select"], .stTextInput > div > div > input {
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 0.5rem !important;
            transition: border-color 0.2s;
        }
        
        /* Premium Buttons */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            border: none !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
            color: white !important;
        }
        
        .stButton > button:hover {
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
            transform: translateY(-1px);
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: #E2E8F0;
            border-radius: 10px;
        }
        
        /* News Dispatch Card */
        .news-dispatch {
            background: #F8FAFC;
            border-left: 4px solid #4F46E5;
            padding: 1.5rem;
            border-radius: 8px 16px 16px 8px;
        }
        
        /* Utility */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
        
        # Sidebar Actions
        with st.sidebar:
            st.markdown('<div class="sidebar-brand">NODE ENGINE v2</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border: 1px solid #E2E8F0; padding: 15px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <span style="font-weight: 700; color: #4F46E5; font-size: 0.8rem;">START NEW OPERATION</span>
                <p style="margin: 5px 0 15px; font-size: 0.85rem; color: #64748B;">Clear history and begin fresh task.</p>
                <div style="font-size: 1.5rem; font-weight: 800; cursor: pointer; text-align: right;">+</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Agent Specs")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Intelligence", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("Access Key",type="password", placeholder="Enter key...")
            
            st.divider()
            
            self.user_controls["selected_usecase"]=st.selectbox("Protocol",usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "AI News"]:
                st.markdown("### Integrations")
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("Tavily Data Key",type="password", placeholder="Bearer...")

            if self.user_controls['selected_usecase']=="AI News":
                st.markdown("### Deployment")
                time_frame = st.selectbox("Cycle Frequency", ["Daily", "Weekly", "Monthly"], index=0)
                if st.button("Launch Feed Pipeline", use_container_width=True, type="primary"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        # Main Area
        from datetime import datetime
        hour = datetime.now().hour
        greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"
        
        st.markdown(f"<h1>{greeting}, BHARU.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B; margin-top: -3rem; margin-bottom: 4rem; font-size: 1.1rem; font-weight: 500;'>How can I elevate your productivity today?</p>", unsafe_allow_html=True)
        
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        return self.user_controls