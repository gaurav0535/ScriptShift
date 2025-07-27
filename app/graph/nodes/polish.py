# app/graph/nodes/polish.py (or wherever polish_content_node is defined)
from langchain_core.messages import AIMessage
import pdb # Keep for debugging if needed

def polish_content_node(state):
    print("Polishing the content ...")
    #pdb.set_trace() # Keep this commented out unless actively debugging

    # 1. Retrieve the generated content
    # Assuming 'repurposed_outputs' holds the generated content for various platforms.
    # You might want to format this nicely or pick a specific one to display.
    generated_content = state.get("repurposed_posts", {})
    
    # Format the generated content for display
    content_display_str = ""
    if generated_content:
        content_display_str = "\n--- Generated Content ---\n"
        for platform, content_text in generated_content.items():
            content_display_str += f"**{platform.upper()}**:\n{content_text[:300]}...\n\n" # Display first 300 chars
        content_display_str += "-------------------------\n\n"
    else:
        content_display_str = "No specific repurposed content found in state.\n\n"


    # 2. Combine the generated content display with your question
    question = (
        "Your content has been generated for all the selected platforms.\n\n"
        f"{content_display_str}" # Include the generated content here
        "Would you like to :\n"
        "1. Change the tone?\n"
        "2. Regenerate content for a specific platform?\n"
        "3. Continue to finalize the content?\n\n"
        "Please respond with your preference, like :\n"
        "- Change tone to professional\n"  
        "- Regenerate content for LinkedIn\n"
        "- Finalize content\n"
    ) 

    # 3. Return the updated state including the new combined AI message
    # Ensure you are correctly appending to the 'messages' list within the state
    updated_messages = state.get("messages", []) + [AIMessage(content=question)]

    state["awaiting_feedback"] = True 
    
    # Return a new dictionary with updated messages, preserving all other state keys
    return {**state, "messages": updated_messages}

