import streamlit as st
import pandas as pd
from openai_helper import extract_financial_data

st.set_page_config(layout="wide")

st.title("📰 News Financial Data Extractor")

col1, col2 = st.columns(2)

# -------- LEFT SIDE --------
with col1:
    st.subheader("Paste News Article")

    news_text = st.text_area(
        "News Article",
        height=400,
        placeholder="Paste full news article here..."
    )

    extract_clicked = st.button(
        "Extract Financial Data",
        use_container_width=True
    )

# -------- RIGHT SIDE --------
with col2:
    st.subheader("Extracted Financial Data")

    empty_df = pd.DataFrame({
        "Measure": [
            "Company Name",
            "Stock Symbol",
            "Revenue",
            "Net Income",
            "EPS"
        ],
        "Value": ["", "", "", "", ""]
    })

    if extract_clicked:

        # ✅ INPUT VALIDATION
        if not news_text.strip():
            st.warning("⚠️ Please enter news article before extracting.")
            st.table(empty_df)

        else:
            with st.spinner("Extracting financial data..."):
                data = extract_financial_data(news_text)

            # Replace empty with None
            for k, v in data.items():
                if not v:
                    data[k] = "None"

            df = pd.DataFrame({
                "Measure": list(data.keys()),
                "Value": list(data.values())
            })

            st.success("✅ Extraction Completed")
            st.table(df)

    else:
        st.table(empty_df)