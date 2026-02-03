import streamlit as st

st.set_page_config(page_title="Stock Management", layout="centered")

st.title("📦 Stock Management System")

item = st.text_input("Item Name")
quantity = st.number_input("Quantity", min_value=0, step=1)
price = st.number_input("Price", min_value=0.0, step=0.5)

if st.button("Add Stock"):
    st.success(f"Added {quantity} units of {item} at ₹{price}")
