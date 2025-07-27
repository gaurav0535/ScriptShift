# app/graph/graph.py
from langgraph.graph import StateGraph, END, START
from app.graph.state import ScriptShiftState
from app.graph.nodes.ask_for_content import ask_for_content_node # <-- Crucial import
from app.graph.nodes.parse_user_content import parse_user_content_node
from app.graph.nodes.clarify import clarify_intent_node
from app.graph.nodes.parse_user_response import parse_user_response_node
from app.graph.nodes.analyze import analyze_content_node
from app.graph.nodes.repurpose import repurpose_content_node
from app.graph.nodes.polish import polish_content_node
from app.graph.nodes.finalize import finalize_content_node
from app.graph.nodes.process_feedback import process_feedback_node
from app.graph.nodes.regenerate import regenerate_content_node
from app.graph.nodes.router import route_next_step 

def build_graph():
    builder = StateGraph(ScriptShiftState)

    builder.add_node("ask_for_content", ask_for_content_node)
    builder.add_node("parse_user_content", parse_user_content_node)
    builder.add_node("clarify", clarify_intent_node)
    builder.add_node("parse_user_response", parse_user_response_node)
    builder.add_node("analyze", analyze_content_node)
    builder.add_node("repurpose", repurpose_content_node)
    builder.add_node("polish", polish_content_node)
    builder.add_node("finalize", finalize_content_node)
    builder.add_node("process_feedback", process_feedback_node)
    builder.add_node("regenerate", regenerate_content_node) 

    builder.add_conditional_edges(
        START,
        route_next_step,
        {
            "ask_for_content": "ask_for_content",
            "parse_user_content": "parse_user_content",
            "parse_user_response": "parse_user_response",
            "process_feedback":"process_feedback",
            "analyze": "analyze",
            "repurpose": "repurpose",
            "polish": "polish",
            "finalize": "finalize",
            END: END,
        }
    )

    builder.add_edge("ask_for_content", END)
    builder.add_edge("clarify", END)
    builder.add_edge("parse_user_content", "clarify")
    builder.add_edge("parse_user_response", "analyze")
    builder.add_edge("analyze", "repurpose")
    builder.add_edge("repurpose", "polish")

    # builder.add_conditional_edges(
    #     "polish",
    #     route_next_step, 
    #     {
    #         "finalize": "finalize",
    #         "regenerate": "repurpose",
    #         END: END,   
    #     }
    # )
    builder.add_edge("polish", END)
    builder.add_conditional_edges(
        "process_feedback",
        lambda state: state.get("next_action"), 
        {
            "finalize": "finalize",       # If user wants to finalize
            "regenerate": "regenerate",   # If user wants to regenerate
            END: END                      # Fallback if process_feedback decides to end (e.g., ambiguous input)
        }
     )
    builder.add_edge("regenerate", "polish")
    builder.add_edge("finalize", END)

    return builder.compile()