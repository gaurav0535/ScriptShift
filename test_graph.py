from app.graph.graph import build_graph
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from typing import List, Dict, Any
from app.graph.state import ScriptShiftState 
import pdb

def print_message(message: BaseMessage):
    """Helper function to print messages clearly."""
    sender = "🤖 AI" if isinstance(message, AIMessage) else "🧑 You"
    print(f"{sender}: {message.content}\n")

def main():
    """Runs the LangGraph agent in a console-based interactive loop using invoke."""
    graph = build_graph()

    current_state: ScriptShiftState = {"messages": []} 

    print("🚀 Starting LangGraph session with invoke()...\n")

    current_state = graph.invoke(current_state)

    if current_state.get("messages") and current_state["messages"]:
        print_message(current_state["messages"][-1])
    
    while True: 
        #pdb.set_trace()  # Keep this commented out unless actively debugging
        user_input = input("💬 Your reply: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting the conversation.")
            break
        
        current_state["messages"].append(HumanMessage(content=user_input))
        
        current_state = graph.invoke(current_state) 
        
        # Check for the final action flag
        if current_state.get("final_action") == "print_output_and_exit":
            print("\n🎉 Finalizing content and exiting!")
            
            final_outputs = current_state.get("repurposed_outputs", {})
            if final_outputs:
                print("\n--- Final Generated Content ---\n")
                for platform, content_text in final_outputs.items():
                    print(f"**{platform.upper()}**:\n{content_text}\n") # Print full content here
                print("-------------------------------\n")

            repurposed_posts = current_state.get("repurposed_posts", {})

            if repurposed_posts:
                for platform, post in repurposed_posts.items():
                    print(f"📢 Platform: {platform}\n📝 Post:\n{post}\n{'-'*60}")
            else:
                print("No repurposed posts found.")    
            
            break # Exit the loop after printing final content

        # Normal message printing for ongoing turns
        last_output_message = None
        if current_state.get("messages") and current_state["messages"]:
            if isinstance(current_state["messages"][-1], AIMessage):
                last_output_message = current_state["messages"][-1]
        
        if last_output_message:
            print_message(last_output_message)
        else:
            print("🎉 Conversation completed by the AI.")
            # If the graph ended without a new AI message and no final_action flag,
            # this might mean an unexpected end or implicit completion.
            # You might want more sophisticated checks here if your graph can end cleanly in other ways.
            break 

if __name__ == "__main__":
    main()