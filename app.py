import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Energy Optimization",
    page_icon="⚡",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("⚡ Smart Energy Consumption Optimization")

st.subheader(
    "Numerical Optimization-Based Smart Energy Consumption "
    "Prediction Framework for Residential Environments"
)

st.markdown("---")

# ============================================================
# FILE PATHS
# ============================================================

DATA_PATH = "data/homec_processed.csv"

PREDICTION_GRAPH = "graphs/predicted_vs_actual.png"
PEAK_GRAPH = "graphs/hourly_peak_load_homec.png"
OPTIMIZATION_GRAPH = "graphs/before_after_optimization.png"
COMPARISON_GRAPH = "graphs/before_after_comparison.png"

HOURLY_RESULT = "results/hourly_power_profile.csv"
OPTIMIZATION_RESULT = "results/optimization_results.csv"
COMPARISON_RESULT = "results/before_after_comparison.csv"

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


try:
    df = load_data()
except Exception as e:
    st.error("Unable to load the processed dataset.")
    st.write(e)
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Dataset",
        "ML Prediction",
        "Peak Load Analysis",
        "Optimization",
        "Before vs After"
    ]
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Project Dashboard")

    st.write(
        "This dashboard presents the results of machine learning-based "
        "energy prediction, peak-load analysis and numerical optimization."
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("ML R²", "0.6109")

    with col2:
        st.metric("Peak Hour", "07:00")

    with col3:
        st.metric("Peak Reduction", "15.00%")

    with col4:
        st.metric("Daily Energy", "68.8273 kWh")

    st.markdown("---")

    st.subheader("Project Workflow")

    st.info(
        """
        Data Collection → Data Preprocessing → Feature Extraction →
        ML Prediction → Peak Load Identification →
        Numerical Optimization → Performance Evaluation
        """
    )

    st.markdown("---")

    st.subheader("Key Results")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Machine Learning")
        st.write("MAE: **0.302053 kW**")
        st.write("RMSE: **0.425657 kW**")
        st.write("R²: **0.610869**")

    with col2:
        st.write("### Optimization")
        st.write("Before peak load: **5.4532 kW**")
        st.write("After peak load: **4.6354 kW**")
        st.write("Peak reduction: **15.00%**")

# ============================================================
# DATASET
# ============================================================

elif page == "Dataset":

    st.header("📁 Dataset")

    st.write(
        "Processed smart-home energy dataset used for the project."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", f"{len(df):,}")

    with col2:
        st.metric("Columns", f"{len(df.columns)}")

    with col3:
        st.metric(
            "Missing Values",
            f"{df.isnull().sum().sum():,}"
        )

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Monitored Appliances")

    appliance_columns = [
        "Car charger [kW]",
        "Water heater [kW]",
        "Air conditioning [kW]",
        "Home Theater [kW]",
        "Outdoor lights [kW]",
        "microwave [kW]",
        "Laundry [kW]",
        "Pool Pump [kW]"
    ]

    available_appliances = [
        col for col in appliance_columns
        if col in df.columns
    ]

    st.dataframe(
        df[available_appliances].head(20),
        use_container_width=True
    )

# ============================================================
# ML PREDICTION
# ============================================================

elif page == "ML Prediction":

    st.header("🤖 Machine Learning Prediction")

    st.write(
        "Random Forest Regression is used to predict future "
        "monitored appliance power."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("MAE", "0.302053 kW")

    with col2:
        st.metric("RMSE", "0.425657 kW")

    with col3:
        st.metric("R²", "0.610869")

    st.markdown("---")

    if os.path.exists(PREDICTION_GRAPH):

        st.subheader("Predicted vs Actual Power")

        # FIXED: removed use_container_width
        st.image(
            PREDICTION_GRAPH,
            width=900
        )

    else:
        st.warning("Prediction graph was not found.")

# ============================================================
# PEAK LOAD ANALYSIS
# ============================================================

elif page == "Peak Load Analysis":

    st.header("📈 Peak Load Analysis")

    st.write(
        "Hourly average monitored appliance power is analyzed "
        "to identify high and low demand periods."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Peak Demand Hour", "07:00")

    with col2:
        st.metric("Lowest Demand Hour", "15:00")

    st.markdown("---")

    if os.path.exists(PEAK_GRAPH):

        st.subheader("Hourly Power Profile")

        # FIXED: removed use_container_width
        st.image(
            PEAK_GRAPH,
            width=900
        )

    else:
        st.warning("Peak-load graph was not found.")

    st.markdown("---")

    if os.path.exists(HOURLY_RESULT):

        hourly_data = pd.read_csv(HOURLY_RESULT)

        st.subheader("Hourly Results")

        st.dataframe(
            hourly_data,
            use_container_width=True
        )

# ============================================================
# OPTIMIZATION
# ============================================================

elif page == "Optimization":

    st.header("⚙️ Numerical Optimization")

    st.write(
        "Numerical optimization is used to shift a portion of "
        "flexible appliance loads while preserving the calculated "
        "daily energy."
    )

    st.info(
        """
        Optimization assumptions:

        • 30% of selected flexible appliance load is treated as shiftable.

        • 70% remains fixed.

        • Appliance operating windows are constrained.

        • Shiftable energy is preserved.

        • The optimization attempts to reduce the maximum monitored load.
        """
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Before Peak", "5.4532 kW")

    with col2:
        st.metric("After Peak", "4.6354 kW")

    with col3:
        st.metric("Peak Reduction", "15.00%")

    st.markdown("---")

    if os.path.exists(OPTIMIZATION_GRAPH):

        st.subheader("Optimization Result")

        # FIXED: removed use_container_width
        st.image(
            OPTIMIZATION_GRAPH,
            width=900
        )

    else:
        st.warning("Optimization graph was not found.")

    st.markdown("---")

    if os.path.exists(OPTIMIZATION_RESULT):

        optimization_data = pd.read_csv(
            OPTIMIZATION_RESULT
        )

        st.subheader("Optimization Data")

        st.dataframe(
            optimization_data,
            use_container_width=True
        )

# ============================================================
# BEFORE VS AFTER
# ============================================================

elif page == "Before vs After":

    st.header("🔄 Before vs After Optimization")

    st.write(
        "Comparison of the monitored load before and after "
        "the numerical optimization."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Before", "5.4532 kW")

    with col2:
        st.metric("After", "4.6354 kW")

    with col3:
        st.metric("Reduction", "15.00%")

    st.markdown("---")

    st.subheader("Energy Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Energy Before", "68.8273 kWh")

    with col2:
        st.metric("Energy After", "68.8273 kWh")

    st.markdown("---")

    if os.path.exists(COMPARISON_GRAPH):

        st.subheader("Before vs After Graph")

        # FIXED: removed use_container_width
        st.image(
            COMPARISON_GRAPH,
            width=900
        )

    else:
        st.warning("Comparison graph was not found.")

    st.markdown("---")

    if os.path.exists(COMPARISON_RESULT):

        comparison_data = pd.read_csv(
            COMPARISON_RESULT
        )

        st.subheader("Comparison Data")

        st.dataframe(
            comparison_data,
            use_container_width=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Numerical Optimization-Based Smart Energy Consumption "
    "Prediction Framework for Residential Environments"
)