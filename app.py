import streamlit as st
import pickle
import numpy as np

# 1. Load the model and scaler
with open("credit_risk_model.pkl", "rb") as f:
    model = pickle.load(f)

# Only include this line if you saved a scaler.pkl
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

st.set_page_config(page_title="Credit Risk AI", layout="centered")

st.title("🚀 Credit Risk Prediction System")
st.write("Input customer details below to assess loan default risk.")

# ... (Keep your imports and loading code at the top)

# --- STEP 2: CLEAN UI ---
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", value=25)
    income = st.number_input("Annual Income ($)", value=50000)
    emp_length = st.number_input("Employment Length (Years)", value=5)
    loan_amount = st.number_input("Loan Amount ($)", value=10000)
    int_rate = st.number_input("Interest Rate (%)", value=11.0)
    loan_percent = st.number_input("Loan Percent of Income (e.g., 0.15)", value=0.15)

with col2:
    # 1. Home Ownership Dictionary
    home_dict = {"Mortgage": 0, "Own": 1, "Rent": 2, "Other": 3}
    home_selection = st.selectbox("Home Ownership", list(home_dict.keys()))
    home = home_dict[home_selection] # This converts "Rent" -> 2 for the model

    # 2. Loan Intent Dictionary
    intent_dict = {"Education": 0, "Medical": 1, "Personal": 2, "Venture": 3, "Home Improvement": 4, "Debt Consolidation": 5}
    intent_selection = st.selectbox("Loan Intent", list(intent_dict.keys()))
    intent = intent_dict[intent_selection]

    # 3. Loan Grade Dictionary
    grade_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    grade_selection = st.selectbox("Loan Grade", list(grade_dict.keys()))
    grade = grade_dict[grade_selection]

    # 4. Default History
    default_dict = {"No": 0, "Yes": 1}
    default_selection = st.selectbox("Historical Default?", list(default_dict.keys()))
    default_history = default_dict[default_selection]

    cred_hist_length = st.number_input("Credit History Length (Years)", value=3)

# --- STEP 3: PREDICTION LOGIC ---
if st.button("Analyze Risk"):
    # Features must stay in the EXACT order of your X.columns
    features = np.array([[
        age, income, emp_length, loan_amount, int_rate, 
        loan_percent, home, intent, grade, default_history, cred_hist_length
    ]]) 
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    probability = model.predict_proba(features_scaled)[0][1]

    st.divider()
    if prediction[0] == 1:
        st.error(f"⚠️ HIGH RISK: {probability:.2%} probability of default.")
    else:
        st.success(f"✅ LOW RISK: {probability:.2%} probability of default.")