#from langgraph.graph import RETURN
from langchain_core.messages import AIMessage
from typing import TypedDict


def clarify_intent_node(state):

    print("Running the clarifications")
    
    question = (
        "Before I can create your content effectively , I need a few quick deatils :\n\n"
        "1. What platforms do you want this content to be published on? (e.g. LinkedIn, X, Instagram, TikTok)\n"
        "2. Who is your target audience? (e.g. startup founders, developers, marketers, etc.)\n"
        "3. What tone do you want the content to be in? (e.g. professional, casual, humorous, etc.)\n"
        "Please answer all three in one message. \n"
    )
    # import pdb
    # pdb.set_trace()
    updated_messages = state.get("messages", []) + [AIMessage(content=question)]
    return {**state, "messages": updated_messages}
    