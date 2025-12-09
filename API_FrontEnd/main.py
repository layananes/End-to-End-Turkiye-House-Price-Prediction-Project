from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# --- CITY TRANSLATION MAP ---
CITY_TO_TIER_MAP = {
    # Tier 1 (Luxury)
    "antalya": "Tier_1", "aydin": "Tier_1", "balikesir": "Tier_1", 
    "bursa": "Tier_1", "canakkale": "Tier_1", "hatay": "Tier_1", 
    "isparta": "Tier_1", "istanbul": "Tier_1", "izmir": "Tier_1", 
    "kocaeli": "Tier_1", "konya": "Tier_1",

    # Tier 2 (Mid-Range)
    "adana": "Tier_2", "adiyaman": "Tier_2", "afyonkarahisar": "Tier_2", 
    "aksaray": "Tier_2", "amasya": "Tier_2", "artvin": "Tier_2", 
    "bartin": "Tier_2", "bayburt": "Tier_2", "bilecik": "Tier_2", 
    "bingol": "Tier_2", "bolu": "Tier_2", "burdur": "Tier_2", 
    "corum": "Tier_2", "denizli": "Tier_2", "diyarbakir": "Tier_2", 
    "duzce": "Tier_2", "edirne": "Tier_2", "elazig": "Tier_2", 
    "erzincan": "Tier_2", "eskisehir": "Tier_2", "gaziantep": "Tier_2", 
    "giresun": "Tier_2", "gumushane": "Tier_2", "igdir": "Tier_2", 
    "kahramanmaras": "Tier_2", "karabuk": "Tier_2", "karaman": "Tier_2", 
    "kastamonu": "Tier_2", "kayseri": "Tier_2", "kirklareli": "Tier_2", 
    "kirsehir": "Tier_2",

    # Tier 3 (Budget)
    "agri": "Tier_3", "ankara": "Tier_3", "ardahan": "Tier_3", 
    "batman": "Tier_3", "bitlis": "Tier_3", "cankiri": "Tier_3", 
    "erzurum": "Tier_3", "hakkari": "Tier_3", "kars": "Tier_3", 
    "kilis": "Tier_3", "kirikkale": "Tier_3"
}



app = FastAPI()

# 1. Load the Model & The Map
model = joblib.load("LGBM_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# 2. Define the Input Format (The "Menu")
class HouseInput(BaseModel):
    Net_Area: float
    Gross_Area: float
    Room_Count: float
    Bathroom_Count: float
    Floor_Location: str
    Building_Age: str
    Heating_Type: str
    City: str
    Occupancy_Status: str
    Investment_Eligibility: str
    Title_Deed_Status: str

# 3. The "Kitchen" (Preprocessing)
def preprocess_input(data: dict):
    # 1. Extract the City
    raw_city = data.pop("City").lower()  # e.g., "Istanbul" -> "istanbul"
    
    # 2. Translate City -> Tier
    # The .get() method handles unknown cities safely!
    city_tier = CITY_TO_TIER_MAP.get(raw_city, "Tier_2") # Default to Tier 2 if unknown
    
    # 3. Create DataFrame
    df = pd.DataFrame([data])
    
    # 4. Manually Add the Tier Columns (This is faster/safer than get_dummies for just 1 row)
    df['City_Tier_2'] = 1 if city_tier == "Tier_2" else 0
    df['City_Tier_3'] = 1 if city_tier == "Tier_3" else 0
    # Note: Tier_1 is implied if both are 0 (Baseline)
    
    # 5. One-Hot Encode remaining columns (Heating, etc.)
    df_encoded = pd.get_dummies(df)
    
    # 6. Align with Model (The Critical Step)
    df_final = df_encoded.reindex(columns=model_columns, fill_value=0)
    
    return df_final
@app.post("/predict")
def predict(input_data: HouseInput):
    # 1. Process Data
    processed_df = preprocess_input(input_data.dict())
    
    # # 2. Predict (This returns Log Price)
    # log_prediction = model.predict(processed_df)[0]
    
    # # 3. Inverse Log Transform (Get Real Money)
    # real_price = np.expm1(log_prediction)
    prediction = model.predict(processed_df)[0]
    return {"price": int(prediction)}