import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI-Based College Asset Prediction", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("assets.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS asset_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_name TEXT,
    year INTEGER,
    quantity_used INTEGER
)
""")
conn.commit()

# ---------------- TITLE ----------------
st.title("🥇 AI-Based College Asset Prediction System")
st.caption("Predict future asset requirements using Artificial Intelligence")

# ---------------- ADD DATA ----------------
st.subheader("➕ Add Asset Usage Data")

asset = st.text_input("Asset Name (Eg: Computer, Printer)")
year = st.number_input("Year", min_value=2015, max_value=2035, step=1)
qty = st.number_input("Quantity Used", min_value=0, step=1)

if st.button("Add Data"):
    c.execute(
        "INSERT INTO asset_usage(asset_name, year, quantity_used) VALUES (?,?,?)",
        (asset, year, qty)
    )
    conn.commit()
    st.success("Data added successfully")

# ---------------- VIEW DATA ----------------
st.subheader("📊 Asset Usage History")

df = pd.read_sql("SELECT * FROM asset_usage", conn)
st.dataframe(df, use_container_width=True)

# ---------------- PREDICTION ----------------
st.subheader("🤖 AI Prediction")

if not df.empty:
    asset_list = df["asset_name"].unique()
    selected_asset = st.selectbox("Select Asset", asset_list)

    asset_df = df[df.asset_name == selected_asset]

    X = asset_df[["year"]]
    y = asset_df["quantity_used"]

    if len(asset_df) >= 2:
        model = LinearRegression()
        model.fit(X, y)

        future_year = st.number_input("Predict for Year", min_value=2024, max_value=2040, step=1)
        prediction = model.predict([[future_year]])[0]

        st.success(f"📈 Predicted requirement for {selected_asset} in {future_year}: {int(prediction)} units")

        # ---------------- GRAPH ----------------
        fig, ax = plt.subplots()
        ax.scatter(X, y)
        ax.plot(X, model.predict(X))
        ax.set_xlabel("Year")
        ax.set_ylabel("Quantity Used")
        ax.set_title(f"{selected_asset} Usage Prediction")
        st.pyplot(fig)
    else:
        st.warning("Add at least 2 years of data for prediction")
else:
    st.info("No data available")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Final Year AI Project | College Asset Management")
