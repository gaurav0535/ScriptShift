
"""
Conversation Flow Router for ScriptShift
--------------------------------------
This module implements the routing logic for the ScriptShift conversation graph.
It determines the next appropriate node based on the conversation state and context.

Routing States:
1. Initial Entry: Routes to ask_for_content when conversation starts
2. Content Input: Routes to parse_user_content when user provides initial content
3. Clarification: Routes to parse_user_response when handling clarification responses
4. Feedback: Routes to process_feedback when awaiting user feedback
5. Terminal: Routes back to ask_for_content or ends the conversation

The router maintains conversation coherence by analyzing:
- Current message context
- Conversation history
- State flags (e.g., awaiting_feedback)
- Previous AI prompts and responses
"""

from langchain_core.messages import HumanMessage, AIMessage

def route_next_step(state: dict) -> str:
    """
    Routes the conversation flow to the next appropriate node based on current state.
    
    Args:
        state (dict): Current conversation state containing:
            - messages: List[BaseMessage] - Conversation history
            - awaiting_feedback: bool - Flag indicating feedback state
            - Other dynamic state variables
    
    Returns:
        str: Identifier of the next node to execute
        
    Routing Logic:
    1. Empty state → "ask_for_content"
    2. User feedback awaited → "process_feedback"
    3. Clarification response → "parse_user_response"
    4. Initial content → "parse_user_content"
    5. Default/fallback → "ask_for_content"
    """
    # Retrieve conversation history from state
    messages = state.get("messages", [])

    # Handle initial conversation state
    if not messages:
        return "ask_for_content"  # Start fresh conversation

    # Get most recent message for routing decisions
    last_message = messages[-1]

    # Process user messages (HumanMessage instances)
    if isinstance(last_message, HumanMessage):
        # Priority 1: Check feedback state
        # If we're explicitly waiting for user feedback, route to feedback processor
        if state.get("awaiting_feedback") is True:
            return "process_feedback"  # Handle user feedback on generated content

        # Priority 2: Analyze conversation context
        # Look backwards through message history to find the last AI message
        # This helps determine if user is responding to a clarification request
        # or providing initial content
        prev_ai_message = None
        for i in range(len(messages) - 2, -1, -1):  # Start from second-to-last message
            msg = messages[i]
            if isinstance(msg, AIMessage):
                prev_ai_message = msg  # Found last AI message
                break
            elif isinstance(msg, HumanMessage):
                break  # Stop if we hit another user message (non-consecutive AI messages)

        # Process based on previous AI message context
        if prev_ai_message:
            # Check message patterns to determine conversation state
            if "Before I can create your content effectively" in prev_ai_message.content:
                return "parse_user_response"  # Handle response to clarification request
            elif "What content would you like me to repurpose?" in prev_ai_message.content:
                return "parse_user_content"  # Handle initial content submission
        
        # Default handling: Treat as initial content
        # This covers cases where:
        # 1. No previous AI message was found
        # 2. AI message doesn't match known patterns
        # 3. User provided content without prompt
        return "parse_user_content" 
            
    # Handle AI message as last message
    # This indicates the graph has completed its current turn
    # Scenarios:
    # 1. AI just asked for content/clarification
    # 2. AI provided output and waiting for feedback
    # 3. Graph reached terminal state
    #
    # Note: This branch should rarely be hit in normal operation
    # as the main loop typically handles the next user interaction
    return "ask_for_content"  # Restart conversation flow if needed