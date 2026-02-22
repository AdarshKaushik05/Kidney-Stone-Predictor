import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Kidney Stone Predictor", page_icon="🩺", layout="centered")

try:
    model = joblib.load('kidney_stone_model.pkl')
except FileNotFoundError:
    st.error("Model file not found! Please ensure 'kidney_stone_model.pkl' is in the same folder.")
    st.stop()

# 3. App Header
st.title("🩺 Kidney Stone Risk Predictor")
st.markdown("""
This application uses a Machine Learning model (Random Forest) trained on urine analysis data to predict the likelihood of kidney stone formation.
""")
st.divider()

# 4. User Input Section
st.subheader("Enter Patient Urine Analysis Data")

col1, col2 = st.columns(2)

with col1:
    gravity = st.number_input("Specific Gravity (e.g., 1.005 - 1.040)", min_value=1.000, max_value=1.060, value=1.020, format="%.3f")
    ph = st.number_input("pH Level (e.g., 4.5 - 8.0)", min_value=0.0, max_value=14.0, value=6.0, format="%.2f")
    osmo = st.number_input("Osmolarity (mOsm) (e.g., 180 - 1250)", min_value=0, max_value=2000, value=600)

with col2:
    cond = st.number_input("Conductivity (mMho) (e.g., 5.0 - 40.0)", min_value=0.0, max_value=100.0, value=20.0, format="%.1f")
    urea = st.number_input("Urea Concentration (e.g., 10 - 650)", min_value=0, max_value=1000, value=300)
    calc = st.number_input("Calcium Concentration (e.g., 0.1 - 15.0)", min_value=0.0, max_value=50.0, value=4.0, format="%.2f")

st.divider()

# 5. Prediction Button and Logic
if st.button("Analyze Risk 🚀", type="primary", use_container_width=True):
    # Format the input
    input_features = np.array([[gravity, ph, osmo, cond, urea, calc]])
    
    # Get the PROBABILITY instead of just the 0/1 prediction
    probabilities = model.predict_proba(input_features)[0]
    stone_risk_percent = probabilities[1] * 100  # Probability of class 1 (Stone)
    
    st.divider()
    st.subheader("Diagnosis Result:")
    
    # Show a progress bar for visual impact
    st.progress(int(stone_risk_percent))
    
    if stone_risk_percent >= 50:
        st.error(f"⚠️ HIGH RISK DETECTED: {stone_risk_percent:.1f}% Probability")
        st.write("The model predicts a high probability of a Kidney Stone. High Calcium is usually the primary driver.")
    else:
        st.success(f"✅ LOW RISK: {stone_risk_percent:.1f}% Probability")
        st.write("The model predicts no kidney stones.")

# 6. Footer
st.markdown("---")
st.caption("Developed using Scikit-Learn • Model Accuracy: ~81%")