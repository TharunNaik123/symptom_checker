from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input format
class SymptomInput(BaseModel):
    symptoms: str

# API endpoint
@app.post("/check")
def check_symptoms(data: SymptomInput):
    prompt = f"""
    Based on these symptoms: {data.symptoms},
    suggest possible conditions and next steps.
    Add a disclaimer: This is not medical advice.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return {"result": result["response"]}
