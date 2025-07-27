import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
load_dotenv()

llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key = os.getenv("OPENAI_API_KEY"),
    
)

# Regenerate the final content

finalize_prompt = PromptTemplate.from_template("""
You are an AI content strategist. Regenerate the final content based on the following inputs:
Platforms: {platforms}
Target Audience: {target_audience}
Tone: {tone}
Based on this summary: {summary}
Only return the new post content                                   
""")


def finalize_content_node(state):
    print("Finalizing the content ...")

    last_message = state.get("messages", [])[-1].content.strip().lower()
    
    summary = state.get("summary").strip()

    audiance = state.get("audience").strip()
