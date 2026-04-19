import os
from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")

#Pyynnön rakenne
class ChatRequest(BaseModel):
    message: str

chat_history = [
    {"role": "system", "content": "You are a helpful and direct AI assistant. You answer in English and keep"
                                          "your answers short, concise and clear."}
]

@app.post("/ask")
async def ask_ai(request: ChatRequest):

    chat_history.append({"role": "user", "content": request.message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_history
    )

    ai_answer = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": ai_answer})

    return {"answer": ai_answer}

#Home page
@app.get("/")
async def get_frontend():
    return FileResponse("index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content="", media_type="image/x-icon")

@app.get("/history")
async def get_history():
    return {
        "history": [
            msg for msg in chat_history
            if msg["role"] != "system"
        ]
    }