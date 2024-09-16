import streamlit as st

# Function to calculate EMI
def calculate_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / (12 * 100)
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return emi

# Function to round down credit score to nearest 50
def round_down_credit_score(score):
    return (score // 50) * 50

# Updated function to determine ROI based on loan type, credit score, category, and other factors
def determine_roi(loan_type, credit_score, customer_category, ltv_ratio=0, house_count=1, vehicle_type="Standard", credit_life_insurance=False):
    EBLR = 9.25  # Assuming EBLR (External Benchmark Lending Rate) is 9.25%
    
    roi_data = {
        "Home Loan": {
            "Salaried": {
                "Male": {800: EBLR-0.90, 750: EBLR-0.75, 700: EBLR-0.10, 650: EBLR+0.20, 600: EBLR+1.00},
                "Female": {800: EBLR-0.90, 750: EBLR-0.75, 700: EBLR-0.15, 650: EBLR+0.15, 600: EBLR+0.95},
                "PSU/Govt": {800: EBLR-0.90, 750: EBLR-0.90, 700: EBLR-0.20, 650: EBLR+0.10, 600: EBLR+0.90}
            },
            "Non-Salaried": {
                "Male": {800: EBLR-0.90, 750: EBLR-0.75, 700: EBLR, 650: EBLR+0.25, 600: EBLR+1.50},
                "Female": {800: EBLR-0.90, 750: EBLR-0.75, 700: EBLR-0.05, 650: EBLR+0.20, 600: EBLR+1.45}
            },
        },
        "Vehicle Loan": {
            "Salaried": {
                "Male": {
                    "Standard": {800: EBLR-0.45, 750: EBLR-0.25, 700: EBLR+0.20, 650: EBLR+1.00, 600: EBLR+1.45},
                    "Electric": {800: EBLR-1.45, 750: EBLR-1.25, 700: EBLR-0.80, 650: EBLR, 600: EBLR+0.45}
                },
                "Female": {
                    "Standard": {800: EBLR-0.50, 750: EBLR-0.30, 700: EBLR+0.15, 650: EBLR+0.95, 600: EBLR+1.40},
                    "Electric": {800: EBLR-1.50, 750: EBLR-1.30, 700: EBLR-0.85, 650: EBLR-0.05, 600: EBLR+0.40}
                },
                "PSU/Govt": {
                    "Standard": {800: EBLR-0.55, 750: EBLR-0.35, 700: EBLR+0.10, 650: EBLR+0.90, 600: EBLR+1.35},
                    "Electric": {800: EBLR-1.55, 750: EBLR-1.35, 700: EBLR-0.90, 650: EBLR-0.10, 600: EBLR+0.35}
                }
            },
            "Non-Salaried": {
                "Male": {
                    "Standard": {800: EBLR-0.40, 750: EBLR-0.20, 700: EBLR+0.25, 650: EBLR+1.05, 600: EBLR+1.50},
                    "Electric": {800: EBLR-1.40, 750: EBLR-1.20, 700: EBLR-0.75, 650: EBLR+0.05, 600: EBLR+0.50}
                },
                "Female": {
                    "Standard": {800: EBLR-0.45, 750: EBLR-0.25, 700: EBLR+0.20, 650: EBLR+1.00, 600: EBLR+1.45},
                    "Electric": {800: EBLR-1.45, 750: EBLR-1.25, 700: EBLR-0.80, 650: EBLR, 600: EBLR+0.45}
                }
            },
        },
        "CRE-RH 3rd House": {
            "PSU/Govt": {750: EBLR-0.65},
            "Salaried": {
                "Male": {800: EBLR-0.65, 750: EBLR-0.50, 700: EBLR+0.15, 650: EBLR+0.45, 600: EBLR+1.25},
                "Female": {800: EBLR-0.65, 750: EBLR-0.50, 700: EBLR+0.10, 650: EBLR+0.40, 600: EBLR+1.25}
            },
            "Non-Salaried": {
                "Male": {800: EBLR-0.65, 750: EBLR-0.50, 700: EBLR+0.25, 650: EBLR+0.50, 600: EBLR+1.25},
                "Female": {800: EBLR-0.65, 750: EBLR-0.50, 700: EBLR+0.20, 650: EBLR+0.45, 600: EBLR+1.25}
            }
        },
        "CRE-RH 4th House onwards": {
            "PSU/Govt": {750: EBLR-0.15},
            "Salaried": {
                "Male": {800: EBLR-0.15, 750: EBLR, 700: EBLR+0.65, 650: EBLR+0.95, 600: EBLR+1.75},
                "Female": {800: EBLR-0.15, 750: EBLR, 700: EBLR+0.60, 650: EBLR+0.90, 600: EBLR+1.75}
            },
            "Non-Salaried": {
                "Male": {800: EBLR-0.15, 750: EBLR, 700: EBLR+0.75, 650: EBLR+1.00, 600: EBLR+1.75},
                "Female": {800: EBLR-0.15, 750: EBLR, 700: EBLR+0.70, 650: EBLR+0.95, 600: EBLR+1.75}
            }
        }
    }

    min_credit_scores = {"Home Loan": 600, "Vehicle Loan": 600, "CRE-RH 3rd House": 600, "CRE-RH 4th House onwards": 600}

    rounded_credit_score = round_down_credit_score(credit_score)
    
    if rounded_credit_score < min_credit_scores.get(loan_type, 600):
        return "Not Eligible"

    employment = customer_category["employment"]
    gender = customer_category["gender"]

    if loan_type == "Home Loan":
        if house_count == 3:
            loan_type = "CRE-RH 3rd House"
        elif house_count >= 4:
            loan_type = "CRE-RH 4th House onwards"
        
        if loan_type == "Home Loan":
            base_roi = roi_data[loan_type][customer_category["type"]][employment if employment == "PSU/Govt" else gender].get(rounded_credit_score, EBLR+1.00)
        else:  # CRE-RH 3rd House or CRE-RH 4th House onwards
            if employment == "PSU/Govt" and rounded_credit_score >= 750:
                base_roi = roi_data[loan_type]["PSU/Govt"][750]
            else:
                base_roi = roi_data[loan_type][customer_category["type"]][gender].get(rounded_credit_score, EBLR+2.25)
        
        if ltv_ratio > 0.8:
            base_roi += 0.5
        
        # Credit Life Insurance concession (only for Home Loans)
        if credit_life_insurance:
            base_roi -= 0.05
    elif loan_type == "Vehicle Loan":
        base_roi = roi_data[loan_type][customer_category["type"]][employment if employment == "PSU/Govt" else gender][vehicle_type].get(rounded_credit_score, EBLR+1.50)

    return base_roi

# Streamlit UI
st.set_page_config(page_title="UBI EMI and ROI Calculator", page_icon="🏦", layout="centered")

# Add creator information
st.sidebar.text("Created by:")
st.sidebar.text("Pushpender Sharma")
st.sidebar.text("CM UMFB Panchkula")
st.sidebar.text("M : +919920802159")

st.title("🏦 UBI EMI and ROI Calculator")

# User inputs
loan_type = st.selectbox("Select Loan Type", ["Home Loan", "Vehicle Loan"])
loan_amount = st.number_input("Loan Amount (in Lakhs)", min_value=0.01, step=0.01, value=10.00, format="%.2f")

# Convert loan amount from lakhs to rupees for internal calculations
loan_amount_rupees = loan_amount * 100000

# Move "Value of the House" input here for Home Loans
house_value = 0
if loan_type == "Home Loan":
    house_value = st.number_input("Value of the House (in Lakhs)", min_value=0.01, step=0.01, value=20.00, format="%.2f")

# Loan tenure input
st.subheader("Loan Tenure")
col1, col2 = st.columns(2)

if loan_type == "Home Loan":
    max_years = 30
    default_years = 10
else:  # Vehicle Loan
    max_years = 7
    default_years = 5

with col1:
    tenure_years = st.number_input("Years", min_value=0, max_value=max_years, value=default_years, step=1)
with col2:
    max_months = min(11, (360 if loan_type == "Home Loan" else 84) - tenure_years * 12)
    tenure_months = st.number_input("Months", min_value=0, max_value=max_months, value=0, step=1)

total_tenure_months = tenure_years * 12 + tenure_months

# Validate total tenure for Vehicle Loan
if loan_type == "Vehicle Loan" and total_tenure_months > 84:
    st.error("Total tenure for Vehicle Loan cannot exceed 84 months.")
    st.stop()

credit_score = st.number_input("Credit Score", min_value=300, max_value=900, step=1, value=750)
customer_type = st.selectbox("Customer Category", ["Salaried", "Non-Salaried"])

# Only show employment type for Salaried customers
employment_type = "General"
if customer_type == "Salaried":
    employment_type = st.selectbox("Employment Type", ["General", "PSU/Govt"])

gender = st.selectbox("Gender", ["Male", "Female"])

# Loan-specific inputs
house_count = 1
ltv_ratio = 0
vehicle_type = "Standard"
credit_life_insurance = False

if loan_type == "Home Loan":
    house_count = st.number_input("Number of Houses Owned (including this one)", min_value=1, step=1, value=1)
    if house_value > 0:
        ltv_ratio = loan_amount / house_value
    credit_life_insurance = st.checkbox("Credit Life Insurance Proposed")
elif loan_type == "Vehicle Loan":
    vehicle_type = st.selectbox("Vehicle Type", ["Standard", "Electric"])

# Combine category information
customer_category = {"type": customer_type, "employment": employment_type, "gender": gender}

# Calculate ROI and EMI
roi = determine_roi(loan_type, credit_score, customer_category, ltv_ratio, house_count, vehicle_type, credit_life_insurance)

# Display results
if roi == "Not Eligible":
    st.error("You are not eligible for this loan due to a low credit score.")
else:
    emi = calculate_emi(loan_amount_rupees, roi, total_tenure_months)
    st.success(f"Applicable ROI: {roi:.2f}%")
    st.success(f"EMI: ₹{emi:.2f}")

# Display the rounded credit score used for calculation
st.info(f"Credit Score used for calculation: {round_down_credit_score(credit_score)}")
st.info(f"Loan to Value Ratio considered: {ltv_ratio:.2f}")

# Display total tenure
st.info(f"Total Loan Tenure: {tenure_years} years and {tenure_months} months ({total_tenure_months} months)")

# Display credit life insurance concession note (only for Home Loans)
if loan_type == "Home Loan" and credit_life_insurance:
    st.info("Note: A 0.05% concession has been applied to the ROI due to Credit Life Insurance.")

# Display house count information for Home Loans
if loan_type == "Home Loan":
    if house_count == 1 or house_count == 2:
        st.info(f"Regular Home Loan rates applied for house number {house_count}")
    elif house_count == 3:
        st.info("CRE-RH 3rd House rates applied")
    elif house_count >= 4:
        st.info("CRE-RH 4th House onwards rates applied")

st.markdown("For feedback, Please reach through whats app to Pushpender Sharma on +91 9920802159")