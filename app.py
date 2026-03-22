import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open('models.pkl', 'rb'))

st.set_page_config(page_title="Stroke Prediction", page_icon="🧠")

st.title("🧠 Stroke Prediction App")
st.write("Enter patient details to predict stroke risk")

# ---------------- USER INPUTS ---------------- #
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", 1, 100, 25)

hypertension = st.selectbox("Hypertension", [0, 1])
heart_disease = st.selectbox("Heart Disease", [0, 1])

ever_married = st.selectbox("Ever Married", ["Yes", "No"])

work_type = st.selectbox(
    "Work Type",
    ["Private", "Self-employed", "Govt_job", "children", "Never_worked"]
)

residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])

avg_glucose_level = st.number_input(
    "Average Glucose Level", min_value=0.0, format="%.2f"
)

bmi = st.number_input(
    "BMI", min_value=0.0, format="%.2f"
)

smoking_status = st.selectbox(
    "Smoking Status",
    ["formerly smoked", "never smoked", "smokes", "Unknown"]
)

# ---------------- ENCODING ---------------- #
gender = 1 if gender == "Male" else 0
ever_married = 1 if ever_married == "Yes" else 0
residence_type = 1 if residence_type == "Urban" else 0

work_map = {
    "Private": 0,
    "Self-employed": 1,
    "Govt_job": 2,
    "children": 3,
    "Never_worked": 4
}
work_type = work_map[work_type]

smoke_map = {
    "formerly smoked": 0,
    "never smoked": 1,
    "smokes": 2,
    "Unknown": 3
}
smoking_status = smoke_map[smoking_status]

# ---------------- PREDICTION ---------------- #
if st.button("Predict Stroke"):

    # Input validation
    if avg_glucose_level <= 0 or bmi <= 0:
        st.warning("⚠️ Please enter valid values for Glucose Level and BMI")
    else:
        # Convert all inputs to float (IMPORTANT FIX)
        input_data = np.array([[
            float(gender),
            float(age),
            float(hypertension),
            float(heart_disease),
            float(ever_married),
            float(work_type),
            float(residence_type),
            float(avg_glucose_level),
            float(bmi),
            float(smoking_status)
        ]], dtype=float)

        # Prediction
        prediction = model.predict(input_data)

        # Probability (optional)
        try:
            prob = model.predict_proba(input_data)[0][1]
            st.write(f"Stroke Probability: {prob:.2f}")
        except:
            pass

        # Result
        if prediction[0] == 1:
            st.error("⚠️ High Risk of Stroke")
        else:
            st.success("✅ Low Risk of Stroke")