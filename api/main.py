from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from perplexity import Perplexity
import os

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    session_token = authorization.split(" ")[1]
    
    try:
        # helallao/perplexity-ai library usage
        perplexity = Perplexity(session_token)
        answer = perplexity.search(request.prompt)
        return {"answer": str(answer)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "ok", "message": "Perplexity Bridge is running"}
