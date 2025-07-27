# app/graph/nodes/ask_for_content.py
from langchain_core.messages import AIMessage

def ask_for_content_node(state):
    print("Asking user for content .......")
    question = (
        "What content would you like me to repurpose? \n\n"
        "Please either :\n"
        "Paste a blog/article URL , OR \n"
        "Paste the raw text of the content you want me to work with.\n"
    )

    updated_messages = state.get("messages", []) + [AIMessage(content=question)]

    return {
        **state,
        "messages": updated_messages
    }