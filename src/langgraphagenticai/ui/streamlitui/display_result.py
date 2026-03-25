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
        
        if usecase == "Basic Chatbot":
            # Initialize state with a HumanMessage
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            for event in graph.stream(initial_state):
                for value in event.values():
                    if "messages" in value:
                        msg = value["messages"][-1] if isinstance(value["messages"], list) else value["messages"]
                        
                        # User Section
                        st.markdown(f'''<div style="font-size: 0.8rem; color: #4F46E5; font-weight: 700; margin-bottom: 0.5rem;">YOU</div>
                        <div class="content-card">{user_message}</div>''', unsafe_allow_html=True)
                        
                        # Assistant Section
                        st.markdown(f'''<div style="font-size: 0.8rem; color: #10B981; font-weight: 700; margin-bottom: 0.5rem;">ASSISTANT</div>
                        <div class="content-card">{msg.content}</div>''', unsafe_allow_html=True)

        elif usecase == "Chatbot With Web":
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)
            for message in res.get('messages', []):
                if isinstance(message, HumanMessage):
                    st.markdown(f'''<div style="font-size: 0.8rem; color: #4F46E5; font-weight: 700; margin-bottom: 0.5rem;">YOU</div>
                    <div class="content-card">{message.content}</div>''', unsafe_allow_html=True)
                elif isinstance(message, ToolMessage):
                    with st.expander("🛠️ Tool Trace"):
                        st.code(message.content, language="json")
                elif isinstance(message, AIMessage) and message.content:
                    st.markdown(f'''<div style="font-size: 0.8rem; color: #10B981; font-weight: 700; margin-bottom: 0.5rem;">ASSISTANT</div>
                    <div class="content-card">{message.content}</div>''', unsafe_allow_html=True)

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Processing news feed..."):
                initial_state = {"messages": [HumanMessage(content=frequency)]}
                result = graph.invoke(initial_state)
                try:
                    # Read the markdown file from the correct src directory
                    AI_NEWS_PATH = f"./src/AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    st.markdown(f'''<div style="font-size: 0.8rem; color: #4F46E5; font-weight: 700; margin-bottom: 0.5rem;">NEWS DISPATCH</div>
                    <div class="content-card">{markdown_content}</div>''', unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"Error: Output not found at {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")