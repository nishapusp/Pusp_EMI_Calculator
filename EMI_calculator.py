import streamlit as st

# Function to calculate EMI
def calculate_emi(principal, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly and in decimal
    tenure_months = tenure_years * 12
    if monthly_rate == 0:  # Prevent division by zero in edge cases
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return emi

# Function to determine ROI based on loan type, credit score, category, and LTV ratio
def determine_roi(loan_type, credit_score, customer_category, ltv_ratio=0, house_count=1, vehicle_type="Standard"):
    # Adjusted ROI data to ensure rates for females are equal to or less than males
    roi_data = {
        "Home Loan": {
            "Salaried": {
                "Male": {800: 8.35, 750: 8.50, 700: 9.15, 650: 9.45, 600: 10.25},
                "Female": {800: 8.30, 750: 8.45, 700: 9.10, 650: 9.40, 600: 10.20}
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
                           "Electric": {800: 7.75, 750: 7.95, 700: 8.40, 650: 9.20, 600: 9.65}}
            },
            "Non-Salaried": {
                "Male": {"Standard": {800: 8.85, 750: 9.05, 700: 9.50, 650: 10.30, 600: 10.75},
                         "Electric": {800: 7.85, 750: 8.05, 700: 8.50, 650: 9.30, 600: 9.75}},
                "Female": {"Standard": {800: 8.80, 750: 9.00, 700: 9.45, 650: 10.25, 600: 10.70},
                           "Electric": {800: 7.80, 750: 8.00, 700: 8.45, 650: 9.25, 600: 9.70}}
            },
        }
    }

    # Adjust ROI for third or more houses (CRE RH rates)
    if loan_type == "Home Loan" and house_count >= 3:
        cre_rh_roi_adjustment = 1.5  # Example adjustment for third house CRE RH rate
        base_roi = roi_data[loan_type][customer_category["type"]][customer_category["gender"]].get(credit_score, 9.25)
        return base_roi + cre_rh_roi_adjustment

    # Adjust ROI based on LTV ratio if house value is provided
    if loan_type == "Home Loan" and ltv_ratio > 0:
        if ltv_ratio <= 0.8:  # LTV 80% or less
            ltv_adjustment = 0
        elif ltv_ratio <= 0.9:  # LTV between 80% and 90%
            ltv_adjustment = 0.5
        else:  # LTV above 90%
            ltv_adjustment = 1.0
        base_roi = roi_data[loan_type][customer_category["type"]][customer_category["gender"]].get(credit_score, 9.25)
        return base_roi + ltv_adjustment

    # Adjust ROI for Electric Vehicles
    if loan_type == "Vehicle Loan":
        return roi_data[loan_type][customer_category["type"]][customer_category["gender"]][vehicle_type].get(credit_score, 9.25)

    # Default ROI determination
    return roi_data.get(loan_type, {}).get(customer_category["type"], {}).get(customer_category["gender"], {}).get(credit_score, 9.25)

# Streamlit UI
st.title("Enhanced EMI and ROI Calculator")

# User inputs
loan_type = st.selectbox("Select Loan Type", ["Home Loan", "Vehicle Loan"])
loan_amount = st.number_input("Loan Amount", min_value=1000, step=1000)
tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, max_value=30, step=1)
credit_score = st.number_input("Credit Score", min_value=300, max_value=900, step=50)
customer_type = st.selectbox("Customer Category", ["Salaried", "Non-Salaried"])
gender = st.selectbox("Gender", ["Male", "Female"])

# House-specific inputs
house_count = 1
ltv_ratio = 0
if loan_type == "Home Loan":
    house_count = st.number_input("Number of Houses Owned (including this one)", min_value=1, step=1)
    house_value = st.number_input("Value of the House", min_value=10000, step=10000)
    if house_value > 0:
        ltv_ratio = loan_amount / house_value

# Vehicle-specific input
vehicle_type = "Standard"
if loan_type == "Vehicle Loan":
    vehicle_type = st.selectbox("Vehicle Type", ["Standard", "Electric"])

# Combine category information
customer_category = {"type": customer_type, "gender": gender}

# Calculate ROI and EMI
roi = determine_roi(loan_type, credit_score, customer_category, ltv_ratio, house_count, vehicle_type)
emi = calculate_emi(loan_amount, roi, tenure_years)

# Display results
st.write(f"**Applicable ROI:** {roi:.2f}%")
st.write(f"**EMI:** ₹{emi:.2f}")
