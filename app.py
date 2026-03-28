import streamlit as st
from datetime import datetime
import hashlib

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
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- STYLING ENGINE ---
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)
hue = (seed % 360)
primary_color = f"hsl({hue}, 65%, 30%)"
accent_bg = f"hsl({hue}, 40%, 97%)"

# --- THE TEMPLATE (Using .format() for safety) ---
invoice_template = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
<style>
    .invoice-container {{
        background-color: white;
        font-family: 'Poppins', sans-serif;
        max-width: 800px;
        margin: 20px auto;
        padding: 40px;
        border-top: 10px solid {color};
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }}
    .header {{ text-align: center; border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
    .header h1 {{ color: {color}; margin: 0; text-transform: uppercase; font-size: 28px; }}
    .info-grid {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
    .item-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
    .item-table th {{ background: {color}; color: white; padding: 12px; text-align: left; }}
    .item-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
    .grand-total {{ font-size: 26px; font-weight: bold; color: {color}; text-align: right; }}
    .words-box {{ background: {bg}; padding: 10px; border-left: 4px solid {color}; margin-top: 10px; font-size: 12px; }}
    .signature-area {{ margin-top: 60px; text-align: right; }}
    .sig-line {{ border-top: 1px solid #333; width: 200px; display: inline-block; margin-top: 40px; }}

    @media print {{
        [data-testid="stSidebar"], [data-testid="stHeader"], .stButton {{ display: none !important; }}
        .invoice-container {{ box-shadow: none; margin: 0; width: 100%; }}
    }}
</style>

<div class="invoice-container">
    <div class="header">
        <h1>{p_name}</h1>
        <div style="color: #666;">{p_addr}</div>
    </div>
    
    <div class="info-grid">
        <div>
            <strong style="color: {color}; font-size: 12px;">BILLED TO</strong><br>
            <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
            <div style="color: #555;">{c_addr}</div>
        </div>
        <div style="text-align: right;">
            <strong style="color: {color}; font-size: 12px;">INVOICE DETAILS</strong><br>
            <strong># {inv_no}</strong><br>
            {date}
        </div>
    </div>

    <table class="item-table">
        <thead>
            <tr><th>Description</th><th style="text-align: right;">Amount</th></tr>
        </thead>
        <tbody>
            <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
        </tbody>
    </table>

    <div class="words-box">Rupees in words: <strong>{words}</strong></div>
    
    <div class="grand-total">
        <div style="font-size: 12px; color: #888; text-transform: uppercase;">Total Due</div>
        ₹ {amt:,.2f}
    </div>

    <div class="signature-area">
        <div class="sig-line"></div>
        <div style="font-weight: bold;">Authorized Signatory</div>
        <div style="font-size: 10px; color: #888;">For {p_name}</div>
    </div>
</div>

<div style="text-align: center; margin-top: 20px;">
    <button onclick="window.print()" style="padding: 10px 20px; background: {color}; color: white; border: none; border-radius: 5px; cursor: pointer;">Print Invoice</button>
</div>
"""

# APPLY DATA TO TEMPLATE
st.markdown(
    invoice_template.format(
        color=primary_color,
        bg=accent_bg,
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
