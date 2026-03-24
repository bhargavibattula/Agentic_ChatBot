from langchain_groq import ChatGroq
import os

class GroqLLM:
    def __init__(self, user_contols_input):
        self.user_contols_input = user_contols_input

    def get_llm_model(self):
        selected_llm = self.user_contols_input.get("selected_llm")
        if selected_llm == 'Groq':
            model_name = self.user_contols_input.get("selected_groq_model")
            api_key = self.user_contols_input.get("GROQ_API_KEY")
            if model_name and api_key:
                return ChatGroq(model=model_name, groq_api_key=api_key)
        return None
