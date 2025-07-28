# app/graph/graph.py
"""
ScriptShift Graph Definition
---------------------------
This file defines the conversation flow for content repurposing using LangGraph.
The graph represents a series of steps from content input to final output,
with conditional branching based on user interactions.

Graph Structure:
1. Content Input Phase:
   - ask_for_content → Initial content collection
   - parse_user_content → Process URL or raw text input
   
2. Understanding Phase:
   - clarify → Get additional context from user
   - parse_user_response → Process user's clarifications
   - analyze → Deep content analysis
   
3. Transformation Phase:
   - repurpose → Content adaptation
   - polish → Content refinement
   
4. Finalization Phase:
   - process_feedback → Handle user feedback
   - regenerate → Recreate content if needed
   - finalize → Generate final output
"""

from langgraph.graph import StateGraph, END, START
from app.graph.state import ScriptShiftState

# Node Imports
# Each node represents a specific step in the content transformation pipeline
from app.graph.nodes.ask_for_content import ask_for_content_node  # Prompts user for content input (URL/text)
from app.graph.nodes.parse_user_content import parse_user_content_node  # Processes and validates user input
from app.graph.nodes.clarify import clarify_intent_node  # Gets additional context about target audience/tone
from app.graph.nodes.parse_user_response import parse_user_response_node  # Processes user's clarification responses
from app.graph.nodes.analyze import analyze_content_node  # Performs content analysis
from app.graph.nodes.repurpose import repurpose_content_node  # Adapts content for target platform
from app.graph.nodes.polish import polish_content_node  # Refines and improves content quality
from app.graph.nodes.finalize import finalize_content_node  # Generates final version
from app.graph.nodes.process_feedback import process_feedback_node  # Handles user feedback
from app.graph.nodes.regenerate import regenerate_content_node  # Recreates content based on feedback
from app.graph.nodes.router import route_next_step  # Manages flow control

def build_graph():
    """
    Constructs the LangGraph conversation flow for content repurposing.
    
    The graph is structured in phases:
    1. Input Collection: ask_for_content → parse_user_content
    2. Context Gathering: clarify → parse_user_response
    3. Processing: analyze → repurpose → polish
    4. Feedback Loop: process_feedback → (regenerate or finalize)
    
    Returns:
        Compiled StateGraph: The executable conversation flow
    """
    builder = StateGraph(ScriptShiftState)

    # Phase 1: Input Collection Nodes
    builder.add_node("ask_for_content", ask_for_content_node)  # Initial prompt for content
    builder.add_node("parse_user_content", parse_user_content_node)  # Process URL/text input

    # Phase 2: Context Gathering Nodes
    builder.add_node("clarify", clarify_intent_node)  # Get audience/tone preferences
    builder.add_node("parse_user_response", parse_user_response_node)  # Process user preferences

    # Phase 3: Content Processing Nodes
    builder.add_node("analyze", analyze_content_node)  # Content analysis
    builder.add_node("repurpose", repurpose_content_node)  # Platform adaptation
    builder.add_node("polish", polish_content_node)  # Content refinement

    # Phase 4: Feedback and Finalization Nodes
    builder.add_node("process_feedback", process_feedback_node)  # Handle user feedback
    builder.add_node("finalize", finalize_content_node)  # Generate final version
    builder.add_node("regenerate", regenerate_content_node)  # Recreate if needed

    # Define conditional routing from START
    # This determines the entry point based on the current state
    builder.add_conditional_edges(
        START,
        route_next_step,
        {
            "ask_for_content": "ask_for_content",      # Initial entry point
            "parse_user_content": "parse_user_content", # After content submission
            "parse_user_response": "parse_user_response", # After clarification
            "process_feedback":"process_feedback",      # After initial content generation
            "analyze": "analyze",                      # Content analysis phase
            "repurpose": "repurpose",                  # Content adaptation phase
            "polish": "polish",                        # Refinement phase
            "finalize": "finalize",                    # Final generation
            END: END,                                  # Terminal state
        }
    )

    # Define the main flow paths
    # These edges represent the primary conversation flow through the graph
    builder.add_edge("ask_for_content", END)          # Allow stopping after content request
    builder.add_edge("clarify", END)                  # Allow stopping after clarification
    builder.add_edge("parse_user_content", "clarify") # Move to clarification after parsing input
    builder.add_edge("parse_user_response", "analyze") # Start analysis after getting preferences
    builder.add_edge("analyze", "repurpose")          # Move to repurposing after analysis
    builder.add_edge("repurpose", "polish")           # Polish the repurposed content
    builder.add_edge("polish", END)                   # Allow completion after polishing

    # Feedback Loop Configuration
    # This defines how user feedback is handled and content is regenerated if needed
    builder.add_conditional_edges(
        "process_feedback",
        lambda state: state.get("next_action"), 
        {
            "finalize": "finalize",       # User accepts the content
            "regenerate": "regenerate",   # User requests changes
            END: END                      # Exit feedback loop
        }
     )
    
    # Final flow paths
    builder.add_edge("regenerate", "polish")          # Polish regenerated content
    builder.add_edge("finalize", END)                 # Complete process after finalization

    return builder.compile()