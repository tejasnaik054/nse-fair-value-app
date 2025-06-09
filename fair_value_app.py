import streamlit as st
import yfinance as yf

st.title("📈 NSE Stock Fair Value Analyzer")

nse_code_input = st.text_input("Enter NSE Code (e.g., TCS, INFY, RELIANCE):")

GROWTH = 0.10
AVG_AAA_YIELD = 0.0736
CURRENT_AAA_YIELD = 0.06263

def calculate_fair_value(eps, growth, avg_aaa_yield, current_aaa_yield):
    return (eps * (8.5 + 2 * growth) * avg_aaa_yield) / current_aaa_yield

if st.button("Analyze"):
    if nse_code_input:
        nse_code = f"{nse_code_input.strip().upper()}.NS"
        try:
            ticker = yf.Ticker(nse_code)
            info = ticker.info

            eps = info.get('trailingEps')
            current_price = info.get('currentPrice')
            company_name = info.get('shortName', nse_code_input.upper())

            if eps is None or current_price is None:
                st.error("❌ Insufficient data to calculate fair value.")
            else:
                fair_value = calculate_fair_value(eps, GROWTH, AVG_AAA_YIELD, CURRENT_AAA_YIELD)

                if current_price < 0.9 * fair_value:
                    value_face = "🟢 Undervalued"
                elif current_price > 1.1 * fair_value:
                    value_face = "🔴 Overvalued"
                else:
                    value_face = "🟡 Well Valued"

                st.success(f"""
                **Company Name:** {company_name}  
                **EPS:** ₹{round(eps, 2)}  
                **Current Price:** ₹{round(current_price, 2)}  
                **Fair Value:** ₹{round(fair_value, 2)}  
                **Valuation Status:** {value_face}
                """)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.warning("⚠ Please enter an NSE stock code.")
