import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import time

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def stream_text(self, text, placeholder, dispatch=False):
        """
        Simulates token-by-token streaming for an extraordinary typing effect.
        """
        if not text:
            return
            
        full_response = ""
        bubble_class = "assistant-bubble" + (" news-dispatch" if dispatch else "")
        for word in text.split(" "):
            full_response += word + " "
            placeholder.markdown(f'<div class="chat-bubble {bubble_class}">{full_response}▌</div>', unsafe_allow_html=True)
            time.sleep(0.015)
        placeholder.markdown(f'<div class="chat-bubble {bubble_class}">{full_response}</div>', unsafe_allow_html=True)

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if "messages" not in st.session_state:
            st.session_state.messages = []

        chat_container = st.container()

        with chat_container:
            # 1. User Message
            st.session_state.messages.append(HumanMessage(content=user_message))
            st.markdown(f'''
            <div class="avatar-container avatar-user">
                <span style="background: #EEF2FF; padding: 6px 12px; border-radius: 8px;">◈ YOU</span>
            </div>
            <div class="chat-bubble user-bubble">{user_message}</div>''', unsafe_allow_html=True)
            
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            
            # Use a simple spinner for all instead of intrusive status boxes
            with st.spinner("Processing operation..."):
                final_msg = None
                final_summary = None
                
                # Execute graph
                for event in graph.stream(initial_state):
                    for value in event.values():
                        if isinstance(value, dict):
                            if "messages" in value:
                                msgs = value["messages"]
                                msg = msgs[-1] if isinstance(msgs, list) else msgs
                                if isinstance(msg, AIMessage):
                                    final_msg = msg
                                    final_summary = msg.content
                            if "summary" in value:
                                final_summary = value["summary"]

            # 2. Rendering Agent Output (Streaming)
            if usecase == "AI News":
                if final_summary:
                    st.markdown(f'''
                    <div class="avatar-container avatar-ai">
                        <span style="background: #EEF2FF; padding: 6px 12px; border-radius: 8px; color: #4F46E5;">◈ PIPELINE DISPATCH</span>
                    </div>''', unsafe_allow_html=True)
                    placeholder = st.empty()
                    self.stream_text(final_summary, placeholder, dispatch=True)
                    st.session_state.messages.append(AIMessage(content=final_summary))
                else:
                    st.warning("No summary was generated.")
            else:
                # Generic Chatbot / Web Search
                if final_msg:
                    st.markdown(f'''
                    <div class="avatar-container avatar-ai">
                        <span style="background: #ECFDF5; padding: 6px 12px; border-radius: 8px;">◈ AGENT</span>
                    </div>''', unsafe_allow_html=True)
                    placeholder = st.empty()
                    self.stream_text(final_msg.content, placeholder)
                    st.session_state.messages.append(final_msg)
                elif final_summary:
                    # Fallback for when summary key is provided but no AIMessage object
                    st.markdown(f'''
                    <div class="avatar-container avatar-ai">
                        <span style="font-size: 0.8rem; background: #ECFDF5; padding: 6px 12px; border-radius: 8px;">◈ AGENT</span>
                    </div>''', unsafe_allow_html=True)
                    placeholder = st.empty()
                    self.stream_text(final_summary, placeholder)
                    st.session_state.messages.append(AIMessage(content=final_summary))