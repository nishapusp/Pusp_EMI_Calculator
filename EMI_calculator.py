import streamlit as st

# Function to calculate EMI
def calculate_emi(principal, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return emi

# Function to determine ROI based on loan type, credit score, category, and other factors
def determine_roi(loan_type, credit_score, customer_category, ltv_ratio=0, house_count=1, vehicle_type="Standard"):
    roi_data = {
        "Home Loan": {
            "Salaried": {
                "Male": {800: 8.35, 750: 8.50, 700: 9.15, 650: 9.45, 600: 10.25},
                "Female": {800: 8.30, 750: 8.45, 700: 9.10, 650: 9.40, 600: 10.20},
                "PSU/Govt": {800: 8.25, 750: 8.40, 700: 9.05, 650: 9.35, 600: 10.15}
            },
            "Non-Salaried": {
                "Male": {800: 8.35, 750: 8.50, 700: 9.25, 650: 9.50, 600: 10.75},
                "Female": {800: 8.30, 750: 8.45, 700: 9.20, 650: 9.45, 600: 10.70}
            },
        },
        "Vehicle Loan": {
            "Salaried": {
                "Male": {"Standard": {800: 8.80, 750: 9.00, 700: 9.45, 650: 10.25, 600: 10.70},
                         "Electric": {800: 7.80, 750: 8.00, 700: 8.45, 650: 9.25, 600: 9.70}},
                "Female": {"Standard": {800: 8.75, 750: 8.95, 700: 9.40, 650: 10.20, 600: 10.65},
                           "Electric": {800: 7.75, 750: 7.95, 700: 8.40, 650: 9.20, 600: 9.65}},
                "PSU/Govt": {"Standard": {800: 8.70, 750: 8.90, 700: 9.35, 650: 10.15, 600: 10.60},
                             "Electric": {800: 7.70, 750: 7.90, 700: 8.35, 650: 9.15, 600: 9.60}}
            },
            "Non-Salaried": {
                "Male": {"Standard": {800: 8.85, 750: 9.05, 700: 9.50, 650: 10.30, 600: 10.75},
                         "Electric": {800: 7.85, 750: 8.05, 700: 8.50, 650: 9.30, 600: 9.75}},
                "Female": {"Standard": {800: 8.80, 750: 9.00, 700: 9.45, 650: 10.25, 600: 10.70},
                           "Electric": {800: 7.80, 750: 8.00, 700: 8.45, 650: 9.25, 600: 9.70}}
            },
        }
    }

    min_credit_scores = {"Home Loan": 600, "Vehicle Loan": 600}

    if credit_score < min_credit_scores.get(loan_type, 600):
        return "Not Eligible"

    employment = customer_category["employment"]
    gender = customer_category["gender"]

    if loan_type == "Home Loan":
        base_roi = roi_data[loan_type][customer_category["type"]][employment if employment == "PSU/Govt" else gender].get(credit_score, 10.25)
        if house_count >= 3:
            base_roi += 1.5
        if ltv_ratio > 0.8:
            base_roi += 0.5
    elif loan_type == "Vehicle Loan":
        base_roi = roi_data[loan_type][customer_category["type"]][employment if employment == "PSU/Govt" else gender][vehicle_type].get(credit_score, 10.25)

    return base_roi

# Streamlit UI
st.set_page_config(page_title="EMI and ROI Calculator", page_icon="🏦", layout="centered")

st.title("🏦 EMI and ROI Calculator")

# User inputs
loan_type = st.selectbox("Select Loan Type", ["Home Loan", "Vehicle Loan"])
loan_amount = st.number_input("Loan Amount (in Rupees)", min_value=1000, step=1000, value=100000)

# Adjust tenure based on loan type
if loan_type == "Home Loan":
    tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, max_value=30, step=1, value=5)
else:  # Vehicle Loan
    tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, max_value=7, step=1, value=5)

credit_score = st.number_input("Credit Score", min_value=300, max_value=900, step=50, value=750)
customer_type = st.selectbox("Customer Category", ["Salaried", "Non-Salaried"])
employment_type = st.selectbox("Employment Type", ["General", "PSU/Govt"])
gender = st.selectbox("Gender", ["Male", "Female"])

# Loan-specific inputs
house_count = 1
ltv_ratio = 0
vehicle_type = "Standard"

if loan_type == "Home Loan":
    house_count = st.number_input("Number of Houses Owned (including this one)", min_value=1, step=1, value=1)
    house_value = st.number_input("Value of the House (in Rupees)", min_value=10000, step=10000, value=200000)
    if house_value > 0:
        ltv_ratio = loan_amount / house_value
elif loan_type == "Vehicle Loan":
    vehicle_type = st.selectbox("Vehicle Type", ["Standard", "Electric"])

# Combine category information
customer_category = {"type": customer_type, "employment": employment_type, "gender": gender}

# Calculate ROI and EMI
roi = determine_roi(loan_type, credit_score, customer_category, ltv_ratio, house_count, vehicle_type)

# Display results
if roi == "Not Eligible":
    st.error("You are not eligible for this loan due to a low credit score.")
else:
    emi = calculate_emi(loan_amount, roi, tenure_years)
    st.success(f"Applicable ROI: {roi:.2f}%")
    st.success(f"EMI: ₹{emi:.2f}")