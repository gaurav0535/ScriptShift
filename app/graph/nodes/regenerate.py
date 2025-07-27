from langchain_core.messages import AIMessage
def regenerate_content_node(state):
    print(f"Regenerating content based on feedback: {state.get('feedback', 'No specific feedback')}")
    
    new_repurposed_outputs = state.get("repurposed_outputs", {})
    new_repurposed_outputs["Regen_Example_Platform"] = "This is regenerated content based on feedback: " + state.get('feedback', '')
    
    updated_messages = state.get("messages", []) + [AIMessage(content="Content has been regenerated. Please review.")]
    
    return {
        **state,
        "repurposed_outputs": new_repurposed_outputs,
        "messages": updated_messages,
        "next_action": "review_regenerated" # A new state to go back to polish/review
    }



