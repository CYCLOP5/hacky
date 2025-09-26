import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(
    page_title="Cosmic Weather Insurance Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

def map_kp_to_anomaly_prob(kp_index):

    prob = 1 / (1 + np.exp(-1.5 * (kp_index - 5.5)))
    return prob

def calculate_premium_for_satellite(daily_forecasts, satellite_value, shielding_factor):
  

    PROFIT_MARGIN = 0.20
    BASE_RATE_FEE = 1000

    if daily_forecasts.empty:
        return None

    worst_case = daily_forecasts.loc[daily_forecasts['y_pred'].idxmax()]

    max_kp_pred = worst_case['y_pred']
    kp_upper_bound = worst_case['ub']

    prob_of_anomaly_raw = map_kp_to_anomaly_prob(kp_upper_bound)

    prob_of_anomaly_mitigated = prob_of_anomaly_raw * (1 - shielding_factor)

    expected_loss = prob_of_anomaly_mitigated * satellite_value

    final_premium = (expected_loss * (1 + PROFIT_MARGIN)) + BASE_RATE_FEE

    return {
        "selected_date": str(worst_case['date'].date()),
        "worst_case_forecast": {
            "predicted_kp": round(max_kp_pred, 2),
            "kp_95_confidence_upper": round(kp_upper_bound, 2),
            "observed_kp_actual": round(worst_case['y_obs'], 2)
        },
        "risk_assessment": {
            "satellite_value": f"${satellite_value:,.2f}",
            "shielding_factor": f"{shielding_factor:.0%}",
            "probability_of_anomaly": f"{prob_of_anomaly_mitigated:.2%}",
            "expected_loss": f"${expected_loss:,.2f}"
        },
        "insurance_premium": {
            "premium_quote_usd": f"${final_premium:,.2f}"
        },
        "assumptions": {
            "profit_margin": f"{PROFIT_MARGIN:.0%}",
            "base_rate_fee": f"${BASE_RATE_FEE:,.2f}"
        }
    }

@st.cache_data
def load_data():
    """Loads and prepares the pre-computed forecast data."""
    try:
        df = pd.read_csv('data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['ub'] = df['kp_pred'] + 1.96 * df['std']
        df['lb'] = df['kp_pred'] - 1.96 * df['std']
        df.rename(columns={'kp_pred': 'y_pred', 'kp': 'y_obs'}, inplace=True)
        return df
    except FileNotFoundError:
        st.error("Fatal Error: `data.csv` not found.")
        st.error("Please create a `data` folder and place the CSV file inside.")
        return None

forecast_df = load_data()

st.title(" Cosmic Weather Insurance Platform")
st.markdown("A prototype system to price insurance for space weather events using probabilistic forecasting.")

if forecast_df is not None:

    st.sidebar.header("Asset & Event Details")

    available_dates = sorted(forecast_df['date'].dt.date.unique())
    selected_date_str = st.sidebar.selectbox(
        "Select a historical storm date:",
        options=[d.strftime('%Y-%m-%d') for d in available_dates],
        index=25, # Default to the 25th available date
        help="Choose a date from a known historical storm to see how the platform would have assessed the risk."
    )
    selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()


    st.sidebar.markdown("---")
    st.sidebar.subheader("Satellite Details")
    satellite_value = st.sidebar.number_input(
        "Satellite Value (USD)",
        min_value=1_000_000,
        max_value=1_000_000_000,
        value=150_000_000,
        step=1_000_000,
        format="%d"
    )

    shielding_percentage = st.sidebar.slider(
        "Satellite Shielding Effectiveness",
        min_value=0,
        max_value=100,
        value=25,
        format="%d%%",
        help="How much the satellite's shielding can mitigate the effects of a storm. 100% means perfect shielding."
    )
    shielding_factor = shielding_percentage / 100.0


    st.sidebar.markdown("---")
    get_quote_button = st.sidebar.button("Generate Insurance Quote", type="primary")

    st.subheader(f"Risk Analysis for: {selected_date.strftime('%B %d, %Y')}")

    daily_data = forecast_df[forecast_df['date'].dt.date == selected_date]

    if get_quote_button and not daily_data.empty:
        premium_details = calculate_premium_for_satellite(daily_data, satellite_value, shielding_factor)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Predicted Kp (Worst Case)",
                value=f"{premium_details['worst_case_forecast']['predicted_kp']}",
                help="The highest predicted Kp index for the selected 24-hour period."
            )
        with col2:
            st.metric(
                label="Probability of Anomaly",
                value=f"{premium_details['risk_assessment']['probability_of_anomaly']}",
                help="The calculated probability of a significant satellite anomaly based on the forecast and asset shielding."
            )
        with col3:
            st.metric(
                label="Insurance Premium (24h)",
                value=f"{premium_details['insurance_premium']['premium_quote_usd']}",
                help="The recommended premium to insure the asset for the 24-hour period."
            )

        st.markdown("---")

        st.subheader("Geomagnetic Forecast & Actuals")

        chart_data = daily_data.rename(columns={
            'y_pred': 'Predicted Kp',
            'y_obs': 'Observed Kp',
            'lb': 'Lower Bound (95%)',
            'ub': 'Upper Bound (95%)'
        }).set_index('date')

        st.line_chart(chart_data[['Predicted Kp', 'Observed Kp', 'Lower Bound (95%)', 'Upper Bound (95%)']])
        st.caption("This chart shows the model's 3-hourly probabilistic predictions (with 95% confidence interval) against the actual observed Kp index for the selected day.")

        st.subheader("Premium Calculation Breakdown")
        with st.expander("See the detailed risk and pricing model", expanded=True):
            st.json(premium_details)

    elif daily_data.empty:
        st.warning("No historical forecast data is available for the selected date. Please choose another date.")
    else:
        st.info("Enter asset details and select a date on the left, then click 'Generate Insurance Quote'.")

else:
    st.balloons()
