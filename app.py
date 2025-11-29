import streamlit as st
import asyncio
from agenttools2 import (
    enhanced_currency_agent,
    InMemoryRunner,
    show_python_code_and_response
)

# Set page config
st.set_page_config(
    page_title="💱 Currency Converter",
    page_icon="💱",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .result-box {
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("💱 AI-Powered Currency Converter")
st.markdown("""
Convert between currencies with automatic fee calculations and exchange rate lookups.
""")

# Create a form for user input
with st.form("conversion_form"):
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=100.0, step=1.0)
        from_currency = st.selectbox(
            "From Currency",
            ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR"],
            index=0
        )
    
    with col2:
        to_currency = st.selectbox(
            "To Currency",
            ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR"],
            index=1
        )
        payment_method = st.selectbox(
            "Payment Method",
            ["Bank Transfer", "Platinum Credit Card", "Gold Debit Card"],
            index=0
        )
    
    # Convert payment method to the format expected by the API
    payment_method_map = {
        "Bank Transfer": "bank transfer",
        "Platinum Credit Card": "platinum credit card",
        "Gold Debit Card": "gold debit card"
    }
    
    # Submit button
    submitted = st.form_submit_button("Convert", type="primary")

# Process the conversion when form is submitted
if submitted:
    # Prepare the query
    query = f"Convert {amount} {from_currency} to {to_currency} using {payment_method}. Show me the precise calculation."
    
    # Show loading spinner
    with st.spinner("🧠 Processing your request with AI..."):
        # Run the conversion
        async def run_conversion():
            runner = InMemoryRunner(agent=enhanced_currency_agent)
            response = await runner.run_debug(query)
            return response
        
        try:
            # Run the async function
            response = asyncio.run(run_conversion())
            
            # Display the result
            st.markdown("### 📊 Conversion Result")
            
            # Get the formatted response
            detailed_response = show_python_code_and_response(response)
            
            # Create an expander for detailed calculation
            with st.expander("View Detailed Calculation", expanded=True):
                if detailed_response:
                    st.markdown("```\n" + detailed_response + "\n```")
                else:
                    st.warning("No detailed calculation available.")
                    if response and len(response) > 0:
                        st.json(response[0].__dict__ if hasattr(response[0], '__dict__') else str(response))
            
            # Show success message
            st.success("✅ Conversion completed successfully!")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check your API key and try again.")
            if 'response' in locals():
                st.json(response[0].__dict__ if hasattr(response[0], '__dict__') else str(response))

# Add some helpful information
st.markdown("""
---
### ℹ️ How It Works
1. Enter the amount and select currencies
2. Choose your payment method
3. Click "Convert" to see the result
4. View the detailed calculation breakdown

The system automatically:
- Looks up the latest exchange rates
- Applies the correct transaction fee
- Shows a complete breakdown of the calculation
""")