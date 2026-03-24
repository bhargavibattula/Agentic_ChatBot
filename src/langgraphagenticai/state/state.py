from typing import Annotated
from typing_extensions import TypedDict , List 
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    Represent the state of the application
    """
    messages:Annotated[List , add_messages]

