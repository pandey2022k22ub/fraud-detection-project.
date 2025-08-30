from fastapi import FastAPI
from app.models import PredictionInput
from app.inference import load_model, predict

app = FastAPI(title="Fraud Detection ML Service")

# Load the model when the application starts
model = load_model()

@app.get("/")
def read_root():
    return {"message": "Fraud Detection ML Service is Running!"}

@app.post("/predict")
def make_prediction(input_data: PredictionInput):
    # This will call the real inference logic
    prediction = predict(model, input_data)
    return prediction