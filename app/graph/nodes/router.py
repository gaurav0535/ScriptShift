# # app/graph/nodes/router.py

# from langchain_core.messages import HumanMessage, AIMessage

# def route_next_step(state):
#     messages = state.get("messages", [])

#     if not messages:
#         # If no messages yet, start by asking for content
#         return "ask_for_content"

#     last_message = messages[-1]

#     # Check if the last message is a user's reply
#     if isinstance(last_message, HumanMessage):
#         # Now, look at the history to see what the AI's *previous* message was
#         # This determines if the current human message is a response to a clarification
        
#         # We need to find the most recent AIMessage that asked for clarification
#         # This requires looking backwards in the messages list *before* the current HumanMessage
#         clarification_requested_flag = False
#         for i in range(len(messages) - 2, -1, -1): # Iterate backwards from second to last message
#             msg = messages[i]
#             if isinstance(msg, AIMessage):
#                 # Simple check for clarification message content. Make this robust.
#                 if "Before I can create your content effectively" in msg.content:
#                     clarification_requested_flag = True
#                     break
#                 # If we encounter another AI message that's not a clarification, stop looking
#                 # (e.g., if it was a final output or an "ask for content")
#                 elif "What content would you like me to repurpose?" in msg.content:
#                      # This means the user replied to the initial content ask
#                      return "parse_user_content"
#                 else:
#                     # Some other AI message, assume no pending clarification from THIS AI message
#                     break
#             elif isinstance(msg, HumanMessage):
#                 # If we hit another HumanMessage, it means the current one is not a reply
#                 # to the *immediate* preceding AI message.
#                 break 

#         if clarification_requested_flag:
#             # User is replying to the clarification questions
#             return "parse_user_response"
#         else:
#             # This is a new initial user input or follow-up that wasn't a clarification
#             # You'll need more logic here to handle various initial inputs
#             # For now, let's assume it's the initial content if no clarification pending.
#             return "parse_user_content" # Or a more sophisticated router for initial input
            
#     # If the last message is an AIMessage (e.g., AI just asked for content or clarified)
#     # The graph would have ended, and `main()` should prompt for user input.
#     # This `route_next_step` likely won't be called if the graph ended.
#     # But if it were, it means the AI just spoke and is waiting.
#     # This path is generally for initial routing when the state is fresh or has just been updated
#     # with a user message.
    
#     # Fallback/Default for cases not explicitly handled
#     # This is important to ensure the graph always has a path.
#     return "ask_for_content"


# app/graph/nodes/router.py
from langchain_core.messages import HumanMessage, AIMessage

def route_next_step(state):
    messages = state.get("messages", [])

    if not messages:
        return "ask_for_content"

    last_message = messages[-1]

    # If the last message is a user's reply
    if isinstance(last_message, HumanMessage):
        # 1. Check if we are explicitly awaiting feedback from the user
        if state.get("awaiting_feedback") is True:
            return "process_feedback"

        # 2. Look backwards to determine context (initial content, clarification)
        prev_ai_message = None
        for i in range(len(messages) - 2, -1, -1):
            msg = messages[i]
            if isinstance(msg, AIMessage):
                prev_ai_message = msg
                break
            elif isinstance(msg, HumanMessage):
                break

        # Existing logic for initial content and clarification responses
        if prev_ai_message:
            if "Before I can create your content effectively" in prev_ai_message.content:
                return "parse_user_response"
            elif "What content would you like me to repurpose?" in prev_ai_message.content:
                return "parse_user_content"
        
        # Fallback for initial content if no specific AI prompt found (e.g., direct content input)
        return "parse_user_content" 
            
    # If the last message is an AIMessage (graph ended after AI spoke)
    # The `main` loop should have handled printing and prompting for user input.
    # This part of the router should ideally not be hit in a well-managed turn.
    # If it is, it means the graph ended, and we might default to asking for content
    # or just terminating.
    return "ask_for_content" # Or "ask_for_content" if you want to loop back to asking generally