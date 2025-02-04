# Sentiment Analysis API

This project provides a FastAPI-based sentiment analysis API that uses two models: a custom Hugging Face model and Llama 3. The API allows you to analyze the sentiment of a given text and get a confidence score for either model. The API supports the following:

- **Custom model**: A fine-tuned Hugging Face model (DistilBERT) for sentiment analysis.
- **Llama 3**: Sentiment analysis using the Llama 3.3-70B versatile model from Groq.

## Requirements

Before running the code, ensure you have Python 3.x installed.

### Install Dependencies

This project requires the following Python packages:

fastapi
uvicorn
transformers
torch
groq
pyngrok
pydantic
requests


### Using the API Endpoints
There is one endpoint available in the FastAPI app:

POST /analyze/
{
  "text": "Your input text here",
  "model": "custom"  # or "llama"
}

Response:
{
  "sentiment": "positive",  # or "negative"
  "confidence": number
}
