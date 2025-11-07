from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline


app = FastAPI()
analyzer = pipeline("sentiment-analysis")


class AnalyzeRequest(BaseModel):
    text: str | None = None

@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "EmoSync backend çalışıyor"}

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    text = req.text or ""

    result = analyzer(text)[0]

    emotion = result["label"]
    confidence = float(result["score"])

    return {"emotion": emotion, "confidence": round(confidence, 2)}

