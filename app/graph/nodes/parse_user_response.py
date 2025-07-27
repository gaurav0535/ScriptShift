import os
import json
import pdb
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel , Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class UserContentDetails(BaseModel):
    platforms: List[str] = Field(description="List of platforms for which content is to be created (e.g., LinkedIn, Twitter, Instagram)")
    audience: str = Field(description="Group of people the content is intended for (e.g., startup founders, tech enthusiasts)")
    tone: str = Field(description="Desired tone of the content (e.g., professional, casual, motivational)")
    
llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL","gpt-4o"),
    api_key = os.getenv("OPENAI_API_KEY"),
  
)

#Define the prompt template  

prompt_template = ChatPromptTemplate.from_messages( # <--- This is the Runnable you want
    [
        ("system", "You are an AI assistant tasked with extracting content preferences."),
        (
            "human",
            """Extract the following 3 values from the user's message:
            1. Platforms they want content for
            2. Target audience
            3. Desired tone of the content

            Please correct the spelling of the output values if necessary.

            User message: {user_input}
            """
        )
    ]
)


structured_llm = llm.with_structured_output(UserContentDetails)
extraction_chain = prompt_template | structured_llm


#prompt = PromptTemplate.from_template(prompt_template)

def parse_user_response_node(state):
    print("Parsing user input into proper structured format")

    #Get user's latest message

    user_input = state["messages"][-1].content.strip()

    #Fill the prompt with the user's reply 

    #filled_prompt = prompt_template.format(user_input=user_input)
    parsed_response_object = extraction_chain.invoke({"user_input": user_input})
    #call the LLM with the filled prompt  

    #response = structured_llm([HumanMessage(content=filled_prompt)])
    
    #Parse the response to JSON
    # try:
    #     parsed_response = json.loads(response.content)
    # except json.JSONDecodeError as e:
    #     print(f"Error parsing JSON: {e}")
    #     return None
    #pdb.set_trace()
    # Update the state with the parsed response attributes
    state["platforms"] = parsed_response_object.platforms
    state["audience"] = parsed_response_object.audience
    state["tone"] = parsed_response_object.tone

    # print(f"Parsed response: {state}")

    return state


