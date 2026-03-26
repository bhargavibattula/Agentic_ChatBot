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

        # UI Container for centered chat
        chat_container = st.container()

        with chat_container:
            if usecase == "Basic Chatbot":
                # User Message
                st.session_state.messages.append(HumanMessage(content=user_message))
                st.markdown(f'''<div class="chat-bubble user-bubble">{user_message}</div>''', unsafe_allow_html=True)
                
                initial_state = {"messages": [HumanMessage(content=user_message)]}
                for event in graph.stream(initial_state):
                    for value in event.values():
                        if "messages" in value:
                            msg = value["messages"][-1] if isinstance(value["messages"], list) else value["messages"]
                            # Assistant Message
                            if isinstance(msg, AIMessage):
                                st.session_state.messages.append(msg)
                                st.markdown(f'''<div class="chat-bubble assistant-bubble">{msg.content}</div>''', unsafe_allow_html=True)

            elif usecase == "Chatbot With Web":
                # User Message
                st.session_state.messages.append(HumanMessage(content=user_message))
                st.markdown(f'''<div class="chat-bubble user-bubble">{user_message}</div>''', unsafe_allow_html=True)
                
                initial_state = {"messages": [HumanMessage(content=user_message)]}
                res = graph.invoke(initial_state)
                for message in res.get('messages', []):
                    if isinstance(message, ToolMessage):
                        with st.status("🔍 Researching...", expanded=False):
                            st.code(message.content, language="json")
                    elif isinstance(message, AIMessage) and message.content:
                        st.session_state.messages.append(message)
                        st.markdown(f'''<div class="chat-bubble assistant-bubble">{message.content}</div>''', unsafe_allow_html=True)

            elif usecase == "AI News":
                frequency = self.user_message
                st.session_state.messages.append(HumanMessage(content=f"Generate {frequency} news report"))
                
                with st.spinner("Compiling Dispatch..."):
                    initial_state = {"messages": [HumanMessage(content=frequency)]}
                    result = graph.invoke(initial_state)
                    try:
                        AI_NEWS_PATH = f"./src/AINews/{frequency.lower()}_summary.md"
                        with open(AI_NEWS_PATH, "r") as file:
                            markdown_content = file.read()

                        st.session_state.messages.append(AIMessage(content=markdown_content))
                        st.markdown(f'''<div class="chat-bubble assistant-bubble" style="border-left: 2px solid #4F46E5;">
                            <div style="font-weight: 700; color: #4F46E5; margin-bottom: 1rem;">NEWS DISPATCH</div>
                            {markdown_content}
                        </div>''', unsafe_allow_html=True)
                    except FileNotFoundError:
                        st.error(f"Error: Output not found at {AI_NEWS_PATH}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")