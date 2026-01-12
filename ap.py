import streamlit as st
import pandas as pd
import pickle
import base64
import calendar  # for month names

# ---------- BACKGROUND IMAGE ----------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* BACKGROUND IMAGE */
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* CENTER CONTENT */
        .block-container {{
            padding-top: 6rem;
            text-align: center;
        }}

        h1, p {{
            color: white !important;
            text-align: center;
        }}

        /* BUTTON */
        .stButton>button {{
            background-color: #0b3c5d;
            color: white;
            border-radius: 18px;
            padding: 0.75rem 1.7rem;
            font-size: 16px;
            display: block;
            margin: 1.8rem auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("bg.jpg")

# ---------- LOAD MODEL & DATA ----------
with open("v_on_spot_model.pkl", "rb") as file:
    model = pickle.load(file)

f_df = pd.read_csv("f_df.csv")

# ---------- TITLE ----------
st.title("V-On-Spot 🌍✈️")

st.write(
    "Choose the month you want to travel and discover the best destinations. "
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------- MONTH SELECT ----------
months = list(calendar.month_name)[1:]  # ['January', 'February', ..., 'December']

# Add placeholder at the start
options = ["📅 Select Month"] + months

# Normal (non-searchable) selectbox
month = st.selectbox(
    "Select Month:",
    options=options,
    index=0
)

# ---------- BUTTON ----------
if st.button("✨ Show Recommendations"):
    if month == "📅 Select Month":  # placeholder selected
        st.warning("Please select a month 🌍")
    else:
        # Convert month name to number
        month_number = months.index(month) + 1  # January = 1
        recommendations = f_df[f_df['Month'] == month_number].copy()

        if recommendations.empty:
            st.warning("No destinations found.")
        else:
            X_input = recommendations[['Month', 'AvgTemp']]
            recommendations['Suitable'] = model.predict(X_input)

            recommendations['Suitable'] = recommendations['Suitable'].map(
                {1: "✅ Suitable", 0: "❌ Not Suitable"}
            )

            st.success(f"Recommended destinations for {month}")

            st.dataframe(
                recommendations[['City', 'Country', 'AvgTemp', 'Budget', 'Suitable']],
                use_container_width=True
            )
