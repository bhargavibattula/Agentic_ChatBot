import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit, HumanMessage, AIMessage

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    """

    # 1. Initialize History State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Load UI & Get Config
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # 3. Render Historical Messages (Synced with Extraordinary UI)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
             st.markdown(f'''
             <div class="avatar-container avatar-user">
                 <span style="background: #EEF2FF; padding: 6px 12px; border-radius: 8px;">◈ YOU</span>
             </div>
             <div class="chat-bubble user-bubble">{msg.content}</div>''', unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
             st.markdown(f'''
             <div class="avatar-container avatar-ai">
                 <span style="background: #ECFDF5; padding: 6px 12px; border-radius: 8px;">◈ AGENT</span>
             </div>
             <div class="chat-bubble assistant-bubble">{msg.content}</div>''', unsafe_allow_html=True)
    
    # 4. Handle Input
    if st.session_state.get('IsFetchButtonClicked', False):
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("What can I help you elevate today?")

    if user_message:
        try:
            # Configure The LLM
            obj_llm_config = GroqLLM(user_contols_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            usecase = user_input.get("selected_usecase")
            if not usecase:
                    st.error("Error: No use case selected.")
                    return
            
            # Graph Builder
            graph_builder = GraphBuilder(model)
            try:
                 graph = graph_builder.setup_graph(usecase)
                 
                 # Display result and append to history
                 dr = DisplayResultStreamlit(usecase, graph, user_message)
                 dr.display_result_on_ui()
                 
                 # 5. Reset button state to prevent loop
                 st.session_state.IsFetchButtonClicked = False
                 
            except Exception as e:
                 st.session_state.IsFetchButtonClicked = False
                 st.error(f"Error: Graph execution failed - {e}")
                 return

        except Exception as e:
             st.error(f"Error: Application error - {e}")
             return
