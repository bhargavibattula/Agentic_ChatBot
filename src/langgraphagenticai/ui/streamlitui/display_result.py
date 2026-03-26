import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # 1. Initialize History if not exists
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # UI Container for live chat
        chat_container = st.container()

        with chat_container:
            # 2. Display the User's Message Immediately 
            st.session_state.messages.append(HumanMessage(content=user_message))
            st.markdown(f'''<div class="chat-bubble user-bubble">{user_message}</div>''', unsafe_allow_html=True)
            
            # 3. Handle Streaming with Status Updates
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            
            if usecase == "Basic Chatbot":
                with st.status("🧠 Thinking...", expanded=False) as status:
                    final_msg = None
                    for event in graph.stream(initial_state):
                        for value in event.values():
                            if "messages" in value:
                                msg = value["messages"][-1] if isinstance(value["messages"], list) else value["messages"]
                                if isinstance(msg, AIMessage):
                                    final_msg = msg
                    status.update(label="Response generated", state="complete")
                    if final_msg:
                        st.session_state.messages.append(final_msg)
                        st.markdown(f'''<div class="chat-bubble assistant-bubble">{final_msg.content}</div>''', unsafe_allow_html=True)

            elif usecase == "Chatbot With Web":
                with st.status("🔍 Researching...", expanded=True) as status:
                    final_msg = None
                    for event in graph.stream(initial_state):
                        if "chatbot" in event:
                             status.update(label="Analyzing query...", state="running")
                        if "tools" in event:
                             status.update(label="Searching the web...", state="running")
                             # Display tool output for transparency
                             tool_msg = event["tools"]["messages"][-1]
                             st.code(tool_msg.content, language="json")
                        
                        for value in event.values():
                            if "messages" in value:
                                msg = value["messages"][-1] if isinstance(value["messages"], list) else value["messages"]
                                if isinstance(msg, AIMessage) and msg.content:
                                    final_msg = msg
                    status.update(label="Analysis complete", state="complete", expanded=False)
                    if final_msg:
                        st.session_state.messages.append(final_msg)
                        st.markdown(f'''<div class="chat-bubble assistant-bubble">{final_msg.content}</div>''', unsafe_allow_html=True)

            elif usecase == "AI News":
                with st.status("📡 Fetching News Pipeline...", expanded=True) as status:
                    final_summary = None
                    for event in graph.stream(initial_state):
                        if "fetch_news" in event:
                            status.update(label="Scanning global AI headlines...", state="running")
                        elif "summarize_news" in event:
                            status.update(label="Synthesizing news articles...", state="running")
                        elif "save_result" in event:
                            status.update(label="Finalizing report...", state="running")
                        
                        for value in event.values():
                            if isinstance(value, dict):
                                if "messages" in value:
                                    msg = value["messages"][-1]
                                    if isinstance(msg, AIMessage):
                                        final_summary = msg.content
                                if "summary" in value:
                                    final_summary = value["summary"]
                    
                    status.update(label="Dispatch ready", state="complete", expanded=False)

                    
                    if final_summary:
                        summary_msg = AIMessage(content=final_summary)
                        st.session_state.messages.append(summary_msg)
                        st.markdown(f'''<div class="chat-bubble assistant-bubble" style="border-left: 2px solid #4F46E5;">
                            <div style="font-weight: 700; color: #4F46E5; margin-bottom: 1rem;">NEWS DISPATCH</div>
                            {final_summary}
                        </div>''', unsafe_allow_html=True)
                    else:
                        st.warning("No summary was generated.")