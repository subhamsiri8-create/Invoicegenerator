import streamlit as st
from datetime import datetime
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Tax Invoice Generator", layout="wide")

# --- INDIAN NUMBER SYSTEM LOGIC ---
def number_to_words(num):
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

    def convert_less_than_thousand(n):
        if n == 0: return ''
        if n < 20: return ones[int(n)]
        t, rem = divmod(n, 10)
        return tens[int(t)] + (' ' + ones[int(rem)] if rem != 0 else '')

    def convert(n):
        if n == 0: return 'Zero'
        res = ""
        if n >= 10000000:
            res += convert_less_than_thousand(n // 10000000) + " Crore "
            n %= 10000000
        if n >= 100000:
            res += convert_less_than_thousand(n // 100000) + " Lakh "
            n %= 100000
        if n >= 1000:
            res += convert_less_than_thousand(n // 1000) + " Thousand "
            n %= 1000
        if n >= 100:
            res += ones[int(n // 100)] + " Hundred "
            n %= 100
        if n > 0:
            res += convert_less_than_thousand(n)
        return res.strip()

    num_int = int(num)
    num_dec = int(round((num - num_int) * 100))
    words = convert(num_int) + " Rupees"
    if num_dec > 0:
        words += " and " + convert(num_dec) + " Paise"
    return words + " Only"

# --- UI INPUTS ---
st.sidebar.header("Bill Details")
p_name = st.sidebar.text_input("Your Company Name", "Digital Marketing Mechanics")
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Social Media Management Services")
amt = st.sidebar.number_input("Amount (INR)", min_value=0.0, value=15000.0)

# --- PROCEDURAL STYLING ENGINE ---
# Seed based on company name for brand consistency
style_seed = sum(ord(c) for c in p_name)
hue = (style_seed * 137.5) % 360
primary_color = f"hsl({hue}, 60%, 35%)"
fonts = ["Poppins", "Montserrat", "Raleway", "Playfair Display"]
selected_font = fonts[style_seed % len(fonts)]

# --- INVOICE HTML TEMPLATE ---
invoice_html = f"""
<link href="https://fonts.googleapis.com/css2?family={selected_font.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
<style>
    .invoice-box {{
        font-family: '{selected_font}', sans-serif;
        max-width: 800px;
        margin: auto;
        padding: 40px;
        border: 1px solid #eee;
        background: white;
        color: #333;
    }}
    .header {{ border-bottom: 3px solid {primary_color}; padding-bottom: 20px; text-align: center; margin-bottom: 30px; }}
    .header h1 {{ color: {primary_color}; text-transform: uppercase; margin: 0; }}
    .meta {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
    .table-container {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
    .table-container th {{ background: {primary_color}; color: white; padding: 12px; text-align: left; }}
    .table-container td {{ padding: 12px; border-bottom: 1px solid #eee; }}
    .total-section {{ text-align: right; margin-top: 30px; }}
    .total-amount {{ font-size: 24px; font-weight: bold; color: {primary_color}; }}
    .words-box {{ background: #f9f9f9; padding: 10px; border-left: 4px solid {primary_color}; font-size: 13px; font-style: italic; }}
</style>

<div class="invoice-box">
    <div class="header">
        <h1>{p_name}</h1>
        <p>{p_addr}</p>
    </div>
    
    <div class="meta">
        <div>
            <strong>Billed To:</strong><br>
            {c_name}<br>{c_addr}
        </div>
        <div style="text-align: right;">
            <strong>Invoice #:</strong> {inv_no}<br>
            <strong>Date:</strong> {inv_date.strftime('%d %b, %Y')}
        </div>
    </div>

    <table class="table-container">
        <thead>
            <tr><th>Description</th><th style="text-align: right;">Amount</th></tr>
        </thead>
        <tbody>
            <tr><td>{desc}</td><td style="text-align: right;">₹ {amt:,.2f}</td></tr>
        </tbody>
    </table>

    <div class="words-box">Rupees in words: {number_to_words(amt)}</div>
    
    <div class="total-section">
        <span>Grand Total:</span><br>
        <span class="total-amount">₹ {amt:,.2f}</span>
    </div>
</div>
"""

st.markdown(invoice_html, unsafe_allow_html=True)

# Add a Print Button
st.sidebar.markdown("---")
if st.sidebar.button("Prepare for Printing"):
    st.info("Press Ctrl+P (Cmd+P on Mac) to save the invoice as a PDF.")
