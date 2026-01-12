import streamlit as st
import pandas as pd
import joblib

# Load model yang sudah dituning
model = joblib.load('rf_model_tuned.pkl')

# Ambil nama fitur dari model
features = model.feature_names_in_

# Judul dan deskripsi dashboard
st.title('📊 Employee Attrition Prediction Dashboard')
st.markdown('Dashboard ini hanya fokus pada 11 variabel (berdasarkan nilai Feature Importance) yang memicu terjadinya attrition')

# Set two columns for input
col1, col2 = st.columns(2)

with col1:
    
    age = st.slider("Age", 18, 60, 18)
    daily_rate = st.slider("Daily Rate", 102, 1499, 102)
    distance_from_home = st.slider("Distance from Home (km)", 1, 29, 1)
    hourly_rate = st.slider("Hourly Rate", 30, 100, 30)
    monthly_income = st.slider("Monthly Income", 1091, 16581, 1091)
    monthly_rate = st.slider("Monthly Rate", 2094, 26999, 2094)

with col2:
    
    percent_salary_hike = st.slider("Percent Salary Hike", 11, 25, 11)
    stock_option_level = st.slider("Stock Option Level", 0, 3, 0)
    total_working_years = st.slider("Total Working Years", 0, 29, 0)
    years_at_company = st.slider("Years at Company", 0, 18, 0)
    overtime = st.selectbox("Overtime?", ("Yes", "No"))
    
# Tombol Prediksi
if st.button("Cek Status Karyawan"):
    # Buat data mentah
    df = pd.DataFrame([{
        "Age": age,
        "DailyRate": daily_rate,
        "DistanceFromHome": distance_from_home,
        "HourlyRate": hourly_rate,
        "MonthlyIncome": monthly_income,
        "MonthlyRate": monthly_rate,
        "PercentSalaryHike": percent_salary_hike,
        "StockOptionLevel": stock_option_level,
        "TotalWorkingYears": total_working_years,
        "YearsAtCompany": years_at_company,
        "OverTime_Yes": 1 if overtime == "Yes" else 0,
    }])

    # Preprocessing agar sesuai dengan 'feature_names_in_'
    df_encoded = pd.get_dummies(df)
    
    # Urutkan kolom
    final_df = df_encoded[features]

    # Prediksi
    res = model.predict(final_df)[0]
    prob = model.predict_proba(final_df)[0]

    if res == 0:
        st.success(f"HASIL: TETAP BERTAHAN (Stay) - Probabilitas: {prob[0]:.2%}")
    else:
        st.error(f"HASIL: BERPOTENSI RESIGN - Probabilitas: {prob[1]:.2%}")
