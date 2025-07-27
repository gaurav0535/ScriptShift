import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import pdb
load_dotenv()

llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key = os.getenv("OPENAI_API_KEY"),
    
)

plateform_prompt = PromptTemplate.from_template("""
You are a social media content strategist.

Repurpose the following into a post for the {platform} platform:
                                                
Target Audience: {target_audience}
                                                
Tone: {tone}

Summary: 
{summary}

Rules:
- Make it engaging for the platform
- Follow the style conversation (e.g., emojis for Instagram , punchy lines for Twitter)
-Use call-to-action when appropriate

Return only the post content                                                                                                                                            
                    
""")

def repurpose_content_node(state):
    print("Creating platform-specific posts ...")
    #pdb.set_trace()
    summary = state.get("summary", "").strip()
    platforms = state.get("platforms", ["LinkedIn", "Twitter", "Instagram"])
    audiance = state.get("audience", "general audience").strip()
    tone = state.get("tone", "professional").strip()

    repurposed_outputs = {}

    for platform in platforms:
        print(f"Repurposing content for {platform} ...")
        
        prompt = plateform_prompt.format(
            platform=platform,
            target_audience=audiance,
            tone=tone,
            summary=summary
        )
        
        response = llm.invoke([HumanMessage(content=prompt)])
        repurposed_outputs[platform] = response.content.strip()

    state["repurposed_posts"] = repurposed_outputs

    return state
