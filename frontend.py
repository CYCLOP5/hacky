import streamlit as st

def main():
    """
    Main function to run the Streamlit user interface for the
    Cosmic Weather Insurance Platform.
    """
    st.set_page_config(
        page_title="Borealis Insurance - GEO Satellite Pricing",
        layout="wide",
        page_icon="🛰️"
    )

    # --- Main Panel: Introduction ---
    st.title("🛰️ Project Borealis: Cosmic Weather Insurance")
    st.markdown("This is the user interface for pricing a 24-hour insurance policy for a Geostationary (GEO) Satellite.")
    st.markdown("---")


    # --- Sidebar: User Inputs ---
    st.sidebar.header("Policy Configuration")

    # Input 1: Asset Value (Core Requirement)
    st.sidebar.subheader("1. Asset Details")
    asset_value_millions = st.sidebar.number_input(
        "Asset Value ($ Millions)",
        min_value=1.0,
        value=250.0,
        step=10.0,
        help="Enter the total insured value of the satellite, including replacement and revenue."
    )

    # Input 2: Satellite Shielding Level (Optional Enhancement)
    shielding_level = st.sidebar.selectbox(
        "Asset Shielding Level",
        options=['Standard', 'Hardened', 'Light/Legacy'],
        index=0,
        help="Select the qualitative level of the satellite's physical protection against radiation."
    )

    # Input 3: Satellite Age (Optional Enhancement)
    years_in_orbit = st.sidebar.slider(
        "Years in Orbit",
        min_value=0,
        max_value=15,
        value=5,
        step=1,
        help="Specify the satellite's age. Older assets may have a higher risk profile."
    )

    # Input 4: Underwriter's Adjustment Factor (Human-in-the-Loop)
    st.sidebar.subheader("2. Underwriter Adjustment")
    adjustment_factor = st.sidebar.slider(
        "Risk Adjustment Factor",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.05,
        help="Adjust the AI-calculated risk based on proprietary knowledge. 1.0 means no change."
    )

    # --- Action Button ---
    st.sidebar.markdown("---")
    if st.sidebar.button("Run Agentic Workflow", type="primary"):
        # This is the trigger for your agentic AI workflow.
        # The logic will be added here in the next step.
        st.success("Workflow initiated! (Placeholder for agentic process)")
        
        # We can display the captured inputs for confirmation
        st.write("### Captured Inputs:")
        st.json({
            "Asset Type": "GEO Satellite",
            "Asset Value ($USD)": asset_value_millions * 1_000_000,
            "Shielding Level": shielding_level,
            "Years in Orbit": years_in_orbit,
            "Underwriter Adjustment Factor": adjustment_factor
        })
    
    # --- Main Panel: Placeholders for Agent Outputs ---
    st.header("Results Dashboard")
    st.markdown("*Awaiting calculation... Please configure the asset in the sidebar and run the workflow.*")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Worst-Case Kp (24h)", "...")
    col2.metric("Incident Probability", "...")
    col3.metric("Expected Loss (24h)", "...")
    col4.metric("Recommended 24h Premium", "...")

    st.markdown("### Agentic Process Log")
    st.info("The thought process and tool execution of the AI agents will appear here once the workflow is run.")


if __name__ == "__main__":
    main()
