from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from groq import Groq
import re

# Load fine-tuned Hugging Face model for 'custom'
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("Suomenlahti/results")

def custom_sentiment_analysis(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    confidence, sentiment_idx = torch.max(probabilities, dim=1)
    sentiment = "positive" if sentiment_idx.item() == 1 else "negative"
    return sentiment, confidence.item()

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def llama_sentiment_analysis(text: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Analyze the sentiment of this text: '{text}'. Return 'positive' or 'negative' and confidence score. Do not tell anything else."}
        ],
        model="llama-3.3-70b-versatile",
    )
    response_text = chat_completion.choices[0].message.content.strip()

    # Updated regex to handle responses like "positive, 1.0"
    try:
        match = re.search(r'(positive|negative),\s*([\d\.]+)', response_text)
        if match:
            sentiment = match.group(1).lower()  # "positive" or "negative"
            confidence = float(match.group(2))  # confidence score
            return sentiment, confidence
        else:
            raise ValueError(f"Unexpected response format from Llama model: {response_text}")
    
    except ValueError:
        raise ValueError(f"Error extracting sentiment from response: {response_text}")


app = FastAPI()

class SentimentRequest(BaseModel):
    text: str
    model: str  # 'custom' or 'llama'

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

def analyze_sentiment(text: str, model: str):
    if model == "custom":
        return custom_sentiment_analysis(text)
    elif model == "llama":
        return llama_sentiment_analysis(text)
    else:
        raise ValueError("Invalid model selection. Choose 'custom' or 'llama'")

@app.post("/analyze/", response_model=SentimentResponse)
def analyze(request: SentimentRequest):
    try:
        sentiment, confidence = analyze_sentiment(request.text, request.model)
        return SentimentResponse(sentiment=sentiment, confidence=confidence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


port = 8000
ngrok_tunnel = ngrok.connect(port)

# where we can visit our fastAPI app
print('Public URL:', ngrok_tunnel.public_url)


nest_asyncio.apply()

# finally run the app
uvicorn.run(app, port=port)