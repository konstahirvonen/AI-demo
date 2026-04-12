import os
from fastapi import FastAPI
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

@app.post("/ask")
async def ask_ai(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            #Järjestelmän "ohjeet / promptit"
            {"role": "system", "content": "You are a helpful and direct AI assistant. You answer in English and keep"
                                          "your answers short, concise and clear."},
            {"role": "user", "content": request.message}
            #Tähän myöhemmin assistant, joka muistaa aikaisemman keskustelun, nyt ei ole ns muistia
        ]
    )

    return {"answer": response.choices[0].message.content}

#Home page
@app.get("/")
async def get_frontend():
    return FileResponse("index.html")