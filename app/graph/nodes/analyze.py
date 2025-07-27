import os
from dotenv import load_dotenv
from newspaper import Article
from langchain_core.prompts import PromptTemplate  
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
load_dotenv()
import pdb

#LLM for summarization
llm = ChatOpenAI(
    model = os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key = os.getenv("OPENAI_API_KEY"),
    
)

#Prompt template for summarization

summary_prompt = PromptTemplate.from_template("""
Summarize the following content into 4-5 clear and concise bullet points.Keep it informative and focused.

Content: {article_text}                                              

""")

def analyze_content_node(state):
    #pdb.set_trace()
    print("Analyzing and summarizing content ...")

    content_source = state.get("content_source", "").strip()

    article_text = ""

    #Step 1: Scrape content if it's a URL
    if content_source.startswith("http://") or content_source.startswith("https://"):
        try:
            article = Article(content_source)
            article.download()
            article.parse()
            article_text = article.text.strip()
        except Exception as e:
            print(f"Error scraping URL: {e}")
            article_text = ""
    else:
        #Use it as raw text
        article_text = content_source.strip()

    # Save raw content
    state["original_content"] = article_text

    #Step 2: Summarize the content
    if article_text.strip():
        prompt = summary_prompt.format(article_text=article_text[:3000])  # Limit to first 3000 chars
        response = llm.invoke([HumanMessage(content=prompt)])
        state["summary"] = response.content.strip()
    else:
        state["summary"] = "No content provided for analysis."

    return state



                                              
