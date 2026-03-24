from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Process the input state and generates a chatbot response.
        """
        user_input = state.get("messages", [])
        llm_response = self.llm.invoke(user_input)
        return {"messages": [llm_response]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        # Bind the tools to the LLM so it knows how to call them
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input and deciding tool usage.
            """
            # Invoke the LLM with the current list of messages in the state
            response = llm_with_tools.invoke(state["messages"])
            
            # Return the updated messages list to the graph state
            return {"messages": [response]}

        return chatbot_node
