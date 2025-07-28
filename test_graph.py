"""
ScriptShift Interactive Console
-----------------------------
This module provides a console-based interface for interacting with the ScriptShift content
repurposing system. It manages the conversation flow, handles user input, and displays
the generated content in a user-friendly format.

Key Features:
- Interactive conversation with the LangGraph agent
- Real-time content processing and generation
- Support for multiple output formats
- Clean exit handling and final content display
"""

from app.graph.graph import build_graph
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from typing import List, Dict, Any
from app.graph.state import ScriptShiftState 
import pdb

def print_message(message: BaseMessage):
    """
    Formats and prints conversation messages with clear sender identification.
    
    Args:
        message (BaseMessage): The message to print (either AIMessage or HumanMessage)
    
    Output Format:
        🤖 AI: [AI message content]
        or
        🧑 You: [User message content]
    """
    sender = "🤖 AI" if isinstance(message, AIMessage) else "🧑 You"
    print(f"{sender}: {message.content}\n")

def main():
    """
    Main execution loop for the ScriptShift content repurposing system.
    
    Flow:
    1. Initializes the LangGraph conversation graph
    2. Maintains conversation state and handles user input
    3. Processes content through the graph nodes
    4. Displays intermediate and final outputs
    5. Handles graceful exit conditions
    
    State Management:
    - messages: List of conversation messages
    - final_action: Indicates when to terminate and display results
    - repurposed_outputs: Stores generated content per platform
    """
    # Initialize the conversation graph
    graph = build_graph()

    # Create initial state with empty message history
    current_state: ScriptShiftState = {"messages": []} 

    print("🚀 Starting LangGraph session with invoke()...\n")

    # Initialize the conversation with the first graph node
    current_state = graph.invoke(current_state)

    # Display the initial AI message if present
    if current_state.get("messages") and current_state["messages"]:
        print_message(current_state["messages"][-1])
    
    # Main conversation loop
    while True: 
        #pdb.set_trace()  # Debugging breakpoint (uncomment when needed)
        
        # Get and process user input
        user_input = input("💬 Your reply: ").strip()
        
        # Handle exit commands
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting the conversation.")
            break
        
        # Add user message to conversation history
        current_state["messages"].append(HumanMessage(content=user_input))
        
        # Process through the graph
        current_state = graph.invoke(current_state) 
        
        # Check if we've reached a final state
        if current_state.get("final_action") == "print_output_and_exit":
            print("\n🎉 Finalizing content and exiting!")
            
            # Display final generated content for each platform
            final_outputs = current_state.get("repurposed_outputs", {})
            if final_outputs:
                print("\n--- Final Generated Content ---\n")
                for platform, content_text in final_outputs.items():
                    print(f"**{platform.upper()}**:\n{content_text}\n")
                print("-------------------------------\n")

            # Display platform-specific repurposed posts
            repurposed_posts = current_state.get("repurposed_posts", {})
            if repurposed_posts:
                for platform, post in repurposed_posts.items():
                    print(f"📢 Platform: {platform}\n📝 Post:\n{post}\n{'-'*60}")
            else:
                print("No repurposed posts found.")    
            
            # End conversation after displaying final content
            break

        # Handle normal conversation flow
        last_output_message = None
        
        # Extract the last AI message from conversation history
        if current_state.get("messages") and current_state["messages"]:
            if isinstance(current_state["messages"][-1], AIMessage):
                last_output_message = current_state["messages"][-1]
        
        # Display AI response or handle conversation end
        if last_output_message:
            print_message(last_output_message)
        else:
            print("🎉 Conversation completed by the AI.")
            # Handle unexpected or implicit completion
            # This occurs when the graph ends without a new AI message
            # and without setting the final_action flag
            # Future enhancement: Add more sophisticated completion detection
            break 

if __name__ == "__main__":
    main()