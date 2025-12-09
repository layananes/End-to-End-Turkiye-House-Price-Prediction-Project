import streamlit as st
import requests

# Set the page title and layout
st.set_page_config(page_title="Turkish Home Price Estimator", layout="centered")

st.title("🏡 Turkish Home Price Estimator")
st.markdown("Enter the house details below to get an AI-powered valuation.")

# --- 1. DEFINE THE OPTIONS (Based on your Data) ---
# Full list of cities from your dataset
CITIES = sorted([
    'adana', 'adiyaman', 'afyonkarahisar', 'agri', 'aksaray', 'amasya', 'ankara', 
    'antalya', 'ardahan', 'artvin', 'aydin', 'balikesir', 'bartin', 'batman', 
    'bayburt', 'bilecik', 'bingol', 'bitlis', 'bolu', 'burdur', 'bursa', 
    'canakkale', 'cankiri', 'corum', 'denizli', 'diyarbakir', 'duzce', 'edirne', 
    'elazig', 'erzincan', 'erzurum', 'eskisehir', 'gaziantep', 'giresun', 
    'gumushane', 'hakkari', 'hatay', 'igdir', 'isparta', 'istanbul', 'izmir', 
    'kahramanmaras', 'karabuk', 'karaman', 'kars', 'kastamonu', 'kayseri', 
    'kilis', 'kirikkale', 'kirklareli', 'kirsehir', 'kocaeli', 'konya'
])

HEATING_TYPES = [
    'Kombi Doğalgaz', 'Merkezi Doğalgaz', 'Merkezi (Pay Ölçer)', 'Klimalı', 
    'Sobalı', 'Doğalgaz Sobalı', 'Yerden Isıtma', 'Kat Kaloriferi', 
    'Merkezi Kömür', 'Jeotermal', 'Güneş Enerjisi', 'Isıtma Yok'
]

AGES = [
    '0 (Yeni)', '1', '2', '3', '4', '5-10', '11-15', '16-20', '21 Ve Üzeri'
]

FLOORS = [
    'Düz Giriş (Zemin)', 'Yüksek Giriş', 'Bahçe Katı', 'Müstakil', 'Villa Tipi', 
    'Bahçe Dublex', 'Çatı Dubleks', 'Çatı Katı', 'Bodrum Kat',
    '1.Kat', '2.Kat', '3.Kat', '4.Kat', '5.Kat', '6.Kat', '7.Kat', '8.Kat', 
    '9.Kat', '10.Kat', '11.Kat', '12.Kat', '13.Kat', '14.Kat', '15.Kat', 
    '16.Kat', '17.Kat', '18.Kat', '19.Kat', '20.Kat', '21.Kat', '22.Kat', 
    '26.Kat', '40+.Kat'
]

OCCUPANCY = ['Boş', 'Kiracı Oturuyor', 'Mülk Sahibi Oturuyor']
TITLE_DEED = ['Kat Mülkiyeti', 'Kat İrtifakı', 'Hisseli Tapu', 'Müstakil Tapulu', 'Arsa Tapulu', 'Unknown']
INVESTMENT = ['Uygun', 'Unknown']


# --- 2. THE INPUT FORM ---
col1, col2 = st.columns(2)

with col1:
    # City Selection
    city = st.selectbox("📍 City", CITIES, index=CITIES.index('istanbul') if 'istanbul' in CITIES else 0)
    
    # Numeric Inputs
    net_area = st.number_input("Net Area (m²)", min_value=10, max_value=1000, value=100)
    gross_area = st.number_input("Gross Area (m²)", min_value=10, max_value=1000, value=120)
    rooms = st.number_input("Room Count", min_value=1.0, max_value=10.0, step=0.5, value=3.0)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=1)
    
    # Investment & Title Deed
    title_deed = st.selectbox("Title Deed Status", TITLE_DEED)

with col2:
    # Categorical Features
    age = st.selectbox("Building Age", AGES)
    floor = st.selectbox("Floor Location", FLOORS)
    heating = st.selectbox("Heating Type", HEATING_TYPES)
    occupancy = st.selectbox("Occupancy Status", OCCUPANCY)
    invest = st.selectbox("Investment Eligibility", INVESTMENT)

# --- 3. PREDICTION BUTTON ---
st.markdown("---")
if st.button("🚀 Calculate Price", type="primary"):
    
    # Prepare the payload (Must match 'HouseInput' class in main.py)
    payload = {
        "Net_Area": net_area,
        "Gross_Area": gross_area,
        "Room_Count": rooms,
        "Bathroom_Count": bathrooms,
        "Floor_Location": floor,
        "Building_Age": age,
        "Heating_Type": heating,
        "City": city,
        "Occupancy_Status": occupancy,
        "Investment_Eligibility": invest,
        "Title_Deed_Status": title_deed
    }
    
    # Send request to the API
    try:
        # Assuming API is running locally on port 8000
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            price = result.get('price', 0)
            
            # Display Result
            st.success(f"### 🏷️ Estimated Value: {price:,.0f} TL")
            
            # Optional: Show details
            st.info(f"Prediction for a {rooms}-room property in **{city.title()}**.")
            
        else:
            st.error(f"Error from API: {response.status_code}")
            st.write(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("🚨 Connection Error: Could not connect to the API.")
        st.warning("Make sure you are running 'uvicorn main:app --reload' in a separate terminal!")