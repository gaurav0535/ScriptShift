from langchain_core.messages import HumanMessage

def parse_user_content_node(state):
    print("Extracting content source from user message ...")

    messages = state.get("messages",[])

    #find the last human message in the conversation
    user_messages = [m for m in messages if isinstance(m, HumanMessage)]
    if not user_messages:
        raise ValueError("No user messages found in the conversation history.")
    
    last_user_message = user_messages[-1].content.strip()

    # Store it in state as content_source

    state["content_source"] = last_user_message
    # import pdb
    # pdb.set_trace()
    return state 
