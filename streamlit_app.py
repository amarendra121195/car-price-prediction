import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
scaler = StandardScaler()

st.title("🚗 Car Price Prediction App")
st.markdown("Fill the details below to predict the **car resale value**.")

# Input form
with st.form("prediction_form"):
    year = st.number_input("Year of Purchase", min_value=1990, max_value=2024, value=2015)
    present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=5.0)
    kms_driven = st.number_input("Kms Driven", min_value=0, value=10000)
    owner = st.selectbox("Owner (0 = First, 1 = Second, etc)", [0, 1, 2, 3])
    
    fuel_type = st.radio("Fuel Type", ("Petrol", "Diesel"))
    seller_type = st.radio("Seller Type", ("Dealer", "Individual"))
    transmission = st.radio("Transmission", ("Manual", "Automatic"))

    submit = st.form_submit_button("Predict Price")

if submit:
    kms_driven_log = np.log(kms_driven + 1)
    fuel_type_petrol = 1 if fuel_type == "Petrol" else 0
    fuel_type_diesel = 1 if fuel_type == "Diesel" else 0
    seller_type_individual = 1 if seller_type == "Individual" else 0
    transmission_manual = 1 if transmission == "Manual" else 0
    year_diff = 2020 - year

    features = np.array([[present_price, kms_driven_log, owner, year_diff,
                          fuel_type_diesel, fuel_type_petrol,
                          seller_type_individual, transmission_manual]])

    prediction = model.predict(features)[0]
    output = round(prediction, 2)

    if output < 0:
        st.error("❌ Sorry, you cannot sell this car.")
    else:
        st.success(f"✅ You can sell the car at ₹ {output} lakhs.")

