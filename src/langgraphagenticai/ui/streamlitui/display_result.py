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
        
        # Display the user message once
        with st.chat_message("user"):
            st.write(user_message)

        if usecase in ["Basic Chatbot", "Chatbot With Web"]:
            for event in graph.stream({'messages': [HumanMessage(content=user_message)]}):
                for value in event.values():
                    # value["messages"] could be a list of messages or a single message
                    messages = value.get("messages")
                    if messages:
                        # Grab the last message from the update
                        if isinstance(messages, list):
                            last_msg = messages[-1]
                        else:
                            last_msg = messages
                        
                        # Only display if it's an AIMessage and contains content
                        if isinstance(last_msg, AIMessage) and last_msg.content:
                            with st.chat_message("assistant"):
                                st.write(last_msg.content)
                        # Optionally handle ToolMessages or other types if needed