import streamlit as st
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Invoice Generator", layout="wide")

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

# --- SIDEBAR INPUTS ---
st.sidebar.header("Invoice Settings")
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS")
p_addr = st.sidebar.text_input("Location", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS")
c_addr = st.sidebar.text_input("Client City", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice No", "INV-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_input("Description", "Social Media Management Services")
amt = st.sidebar.number_input("Amount", value=15000.0)

# --- DYNAMIC STYLING ---
style_seed = sum(ord(c) for c in p_name)
hue = (style_seed * 137.5) % 360
primary_color = f"hsl({hue}, 60%, 35%)"

# --- RENDER INVOICE ---
# We use a triple-quoted string and .format() to avoid f-string curly brace conflicts with CSS
invoice_template = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
<style>
    .invoice-box {{
        font-family: 'Poppins', sans-serif;
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
        background-color: white;
    }}
    .header {{ text-align: center; border-bottom: 3px solid {color}; padding-bottom: 10px; margin-bottom: 20px; }}
    .header h1 {{ color: {color}; margin-bottom: 5px; text-transform: uppercase; }}
    .meta {{ display: flex; justify-content: space-between; margin-top: 20px; margin-bottom: 30px; font-size: 14px; }}
    .table-container {{ width: 100%; border-collapse: collapse; }}
    .table-container th {{ background: {color}; color: white; padding: 10px; text-align: left; }}
    .table-container td {{ padding: 10px; border-bottom: 1px solid #eee; }}
    .total-area {{ text-align: right; margin-top: 20px; }}
    .grand-total {{ font-size: 20px; font-weight: bold; color: {color}; }}
    .words {{ font-style: italic; color: #666; font-size: 12px; margin-top: 10px; }}
</style>

<div class="invoice-box">
    <div class="header">
        <h1>{p_name}</h1>
        <div>{p_addr}</div>
    </div>
    <div class="meta">
        <div>
            <strong>Billed To:</strong><br>
            {c_name}<br>{c_addr}
        </div>
        <div style="text-align: right;">
            <strong>Invoice #:</strong> {inv_no}<br>
            <strong>Date:</strong> {date}
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
    <div class="total-area">
        <div class="words">Rupees in words: {words}</div>
        <div style="margin-top:10px;">Grand Total:</div>
        <div class="grand-total">₹ {amt:,.2f}</div>
    </div>
</div>
"""

# Injecting the data into the template
st.markdown(
    invoice_template.format(
        color=primary_color,
        p_name=p_name,
        p_addr=p_addr,
        c_name=c_name,
        c_addr=c_addr,
        inv_no=inv_no,
        date=inv_date.strftime("%d %b, %Y"),
        desc=desc,
        amt=amt,
        words=number_to_words(amt)
    ),
    unsafe_allow_html=True
)
