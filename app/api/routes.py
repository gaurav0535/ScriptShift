from fastapi import APIRouter,Request
from app.graph.graph import build_graph

router = APIRouter()

graph_app = build_graph()

@router.get("/hello")
def hello():
    return {"message": "Hello World"}

@router.post("/repupose")
async def repurpose_content(request: Request):
    body = await request.json()

    #Expecting messages as list and content_source as string (optional if ask-for-content node handles it)

    initial_state = {
        "messages": body.get("messages", []),   
    }

    if "content_source" in body:
        initial_state["content_source"] = body["content_source"]

    result = graph_app.run(initial_state)

    return result






