# # app/graph/state.py
# from typing import Optional, List, TypedDict, Dict
# from langchain_core.messages import BaseMessage

# class ScriptShiftState(TypedDict, total=False):
#     messages: List[BaseMessage]
#     content_source: str
#     original_content: Optional[str]
#     summary: Optional[str]
#     platforms: List[str]
#     audience: str
#     tone: str
#     repurposed_posts: Dict[str, str]
#     feedback: Optional[str] 

# app/graph/state.py
from typing import Optional, List, TypedDict, Dict
from langchain_core.messages import BaseMessage

class ScriptShiftState(TypedDict, total=False):
    messages: List[BaseMessage]
    content_source: Optional[str]
    original_content: Optional[str]
    summary: Optional[str]
    
    platforms: Optional[List[str]]
    audience: Optional[str]
    tone: Optional[str]
    
    repurposed_posts: Optional[Dict[str, str]] # The generated content
    
    feedback: Optional[str] # To store user's feedback
    
    # New flag to indicate we're waiting for specific feedback
    awaiting_feedback: Optional[bool] # True when we've asked for feedback and are waiting

    next_action: Optional[str]  # NEW: To store the next intended action (e.g., "finalize", "regenerate")
    final_action: Optional[str]  # NEW: To signal main.py to print output and exit (e.g., "print_output_and_exit")