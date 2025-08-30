from pydantic import BaseModel

class PredictionInput(BaseModel):
    # Define the input features your model expects
    user_id: str
    coupon_code: str
    ip_address: str
    # ... add other features like device_id, time of day, etc.