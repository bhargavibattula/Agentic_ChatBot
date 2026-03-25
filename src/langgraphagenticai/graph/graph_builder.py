from langgraph.graph import StateGraph, END, START
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        return self.graph_builder.compile()

    def chatbot_with_tools_build_graph(self):
        """
        Builds a chatbot graph with tools using LangGraph.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        llm = self.llm
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node_func = obj_chatbot_with_node.create_chatbot(tools)
        
        self.graph_builder.add_node("chatbot", chatbot_node_func)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        # Define conditional edges: from chatbot, based on tools_condition, 
        # it goes to "tools" or END.
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        # From tools, we go back to chatbot
        self.graph_builder.add_edge("tools", "chatbot")

        return self.graph_builder.compile()

    def setup_graph(self, usecase):
        """
        Sets up the graph based on the selected use case.
        """
        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            return self.chatbot_with_tools_build_graph()
        if usecase == 'AI News':
            return self.ai_news_builder_graph()
        return None


    def ai_news_builder_graph(self):

        ai_news_node = AINewsNode(self.llm)
        ### added the nodes 
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        ### added the edges 
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

        return self.graph_builder.compile()
        
        
