import streamlit as st
import requests
import os


BACKEND_URL = "http://backend:8000"  # ⚠️ pas localhost !



st.set_page_config(page_title="Credit Scoring Prediction App", layout="centered")

st.title("📊 Credit Scoring Prediction App")

# --- Group 1: General Info ---
with st.expander("🪪 General Information"):
    id = st.number_input("ID", min_value=0, step=1)
    rn = st.number_input("RN", min_value=0, step=1)
    pre_since_opened = st.number_input("Months Since Opened", min_value=0, step=1)
    pre_since_confirmed = st.number_input("Months Since Confirmed", min_value=0, step=1)
    pre_pterm = st.number_input("Pre Pterm", min_value=0, step=1)
    pre_fterm = st.number_input("Pre Fterm", min_value=0, step=1)
    pre_till_pclose = st.number_input("Pre Till Pclose", min_value=0, step=1)
    pre_till_fclose = st.number_input("Pre Till Fclose", min_value=0, step=1)

# --- Group 2: Loans Info ---
with st.expander("💳 Loans Summary"):
    pre_loans_credit_limit = st.number_input("Loans Credit Limit", min_value=0, step=1)
    pre_loans_next_pay_summ = st.number_input("Next Payment Summary", min_value=0, step=1)
    pre_loans_outstanding = st.number_input("Outstanding Loans", min_value=0, step=1)
    pre_loans_total_overdue = st.number_input("Total Overdue", min_value=0, step=1)
    pre_loans_max_overdue_sum = st.number_input("Max Overdue Sum", min_value=0, step=1)
    pre_loans_credit_cost_rate = st.number_input("Credit Cost Rate", min_value=0, step=1)
    pre_loans5 = st.number_input("Loans 5", min_value=0, step=1)
    pre_loans530 = st.number_input("Loans 5–30", min_value=0, step=1)
    pre_loans3060 = st.number_input("Loans 30–60", min_value=0, step=1)
    pre_loans6090 = st.number_input("Loans 60–90", min_value=0, step=1)
    pre_loans90 = st.number_input("Loans >90", min_value=0, step=1)

# --- Group 3: Zero Loan Flags ---
with st.expander("🚩 Zero Loan Flags"):
    is_zero_loans5 = st.selectbox("Zero Loans 5", [0, 1])
    is_zero_loans530 = st.selectbox("Zero Loans 5–30", [0, 1])
    is_zero_loans3060 = st.selectbox("Zero Loans 30–60", [0, 1])
    is_zero_loans6090 = st.selectbox("Zero Loans 60–90", [0, 1])
    is_zero_loans90 = st.selectbox("Zero Loans >90", [0, 1])

# --- Group 4: Utilization ---
with st.expander("📈 Utilization Metrics"):
    pre_util = st.number_input("Utilization", min_value=0, step=1)
    pre_over2limit = st.number_input("Over 2x Limit", min_value=0, step=1)
    pre_maxover2limit = st.number_input("Max Over 2x Limit", min_value=0, step=1)
    is_zero_util = st.selectbox("Zero Utilization", [0, 1])
    is_zero_over2limit = st.selectbox("Zero Over 2x Limit", [0, 1])
    is_zero_maxover2limit = st.selectbox("Zero Max Over 2x Limit", [0, 1])

# --- Group 5: Encoded Payments ---
with st.expander("💰 Encoded Payments (enc_paym_0 → enc_paym_24)"):
    enc_paym = {}
    for i in range(25):
        enc_paym[f"enc_paym_{i}"] = st.number_input(f"enc_paym_{i}", min_value=0, step=1)

# --- Group 6: Encoded Loan Info ---
with st.expander("🏦 Encoded Loan Info"):
    enc_loans_account_holder_type = st.number_input("Account Holder Type", min_value=0, step=1)
    enc_loans_credit_status = st.number_input("Credit Status", min_value=0, step=1)
    enc_loans_credit_type = st.number_input("Credit Type", min_value=0, step=1)
    enc_loans_account_cur = st.number_input("Account Currency", min_value=0, step=1)

# --- Group 7: Flags ---
with st.expander("⚙️ Flags"):
    pclose_flag = st.selectbox("Pclose Flag", [0, 1])
    fclose_flag = st.selectbox("Fclose Flag", [0, 1])

# --- Build Payload ---
payload = {
    "id": id,
    "rn": rn,
    "pre_since_opened": pre_since_opened,
    "pre_since_confirmed": pre_since_confirmed,
    "pre_pterm": pre_pterm,
    "pre_fterm": pre_fterm,
    "pre_till_pclose": pre_till_pclose,
    "pre_till_fclose": pre_till_fclose,
    "pre_loans_credit_limit": pre_loans_credit_limit,
    "pre_loans_next_pay_summ": pre_loans_next_pay_summ,
    "pre_loans_outstanding": pre_loans_outstanding,
    "pre_loans_total_overdue": pre_loans_total_overdue,
    "pre_loans_max_overdue_sum": pre_loans_max_overdue_sum,
    "pre_loans_credit_cost_rate": pre_loans_credit_cost_rate,
    "pre_loans5": pre_loans5,
    "pre_loans530": pre_loans530,
    "pre_loans3060": pre_loans3060,
    "pre_loans6090": pre_loans6090,
    "pre_loans90": pre_loans90,
    "is_zero_loans5": is_zero_loans5,
    "is_zero_loans530": is_zero_loans530,
    "is_zero_loans3060": is_zero_loans3060,
    "is_zero_loans6090": is_zero_loans6090,
    "is_zero_loans90": is_zero_loans90,
    "pre_util": pre_util,
    "pre_over2limit": pre_over2limit,
    "pre_maxover2limit": pre_maxover2limit,
    "is_zero_util": is_zero_util,
    "is_zero_over2limit": is_zero_over2limit,
    "is_zero_maxover2limit": is_zero_maxover2limit,
    **enc_paym,
    "enc_loans_account_holder_type": enc_loans_account_holder_type,
    "enc_loans_credit_status": enc_loans_credit_status,
    "enc_loans_credit_type": enc_loans_credit_type,
    "enc_loans_account_cur": enc_loans_account_cur,
    "pclose_flag": pclose_flag,
    "fclose_flag": fclose_flag
}

# --- Prediction Button ---
if st.button("🔮 Predict Credit Status"):
    try:
        
        response = requests.post(f"{BACKEND_URL}/api/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            credit_status = result.get('credit_status', 'Unknown')
            probability = result.get('probability', 0.0)
            st.success(f"🎯 Prediction: {credit_status}")
            st.info(f"📊 Probability: {probability:.4f} ({probability*100:.2f}%)")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"⚠️ Connection error: {e}")
