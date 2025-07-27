# app/graph/nodes/process_feedback.py
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
import pdb

def process_feedback_node(state):
    #pdb.set_trace()  # Keep this commented out unless actively debugging
    print("Processing user feedback...")
    
    user_feedback_message = None
    if state.get("messages"):
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                user_feedback_message = msg
                break
    
    if not user_feedback_message:
        print("Error: No user feedback found to process.")
        # Fallback: Ask for feedback again or route to an error state
        return {**state, "error": "No user feedback to process", "next_action": END} # Default to END if no feedback

    feedback_text = user_feedback_message.content.strip().lower()
    state["feedback"] = feedback_text # Store the raw feedback

    # Clear the awaiting_feedback flag after processing
    state["awaiting_feedback"] = False 

    # Determine action based on feedback
    if "finalize" in feedback_text:
        print("User chose to finalize. Signaling final output.")
        state["next_action"] = "finalize"
        state["final_action"] = "print_output_and_exit" # NEW FLAG for main.py
    elif "regenerate" in feedback_text or "make it" in feedback_text or "change" in feedback_text:
        print(f"User provided feedback for regeneration: {feedback_text}")
        state["next_action"] = "regenerate"
        state["final_action"] = None # Ensure this is cleared
    else:
        # Default or ambiguous feedback
        print("Ambiguous feedback, defaulting to finalize for now.")
        state["next_action"] = "finalize" # Default to finalize if unclear
        state["final_action"] = "print_output_and_exit" # Also print and exit on ambiguous feedback for now

    return state