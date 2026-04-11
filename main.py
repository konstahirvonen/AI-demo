import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

#Pyynnön rakenne
class ChatRequest(BaseModel):
    message: str

@app.post("/ask")
async def ask_ai(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            #Järjestelmän "ohjeet / promptit"
            {"role": "system", "content": "Olet hyödyllinen ja suora tekoäly-assistentti. Vastaat suomeksi ja pidät"
                                          "vastauset lyhyinä, ytimekkäinä ja selkeinä"},
            {"role": "user", "content": request.message}
            #Tähän myöhemmin assistant, joka muistaa aikaisemman keskustelun, nyt ei ole ns muistia
        ]
    )

    return {"answer": response.choices[0].message.content}

@app.get("/")
async def home():
    return {"message": "Backend on käynnissä. Käytä /docs testaamiseen http://127.0.0.1:8000/docs"}