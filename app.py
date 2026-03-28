import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Professional Invoice Generator", layout="wide")

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
        if n > 0: res += convert_less_than_thousand(n)
        return res.strip()
    num_int = int(num); num_dec = int(round((num - num_int) * 100))
    words = convert(num_int) + " Rupees"
    if num_dec > 0: words += " and " + convert(num_dec) + " Paise"
    return words + " Only"

# --- SIDEBAR ---
st.sidebar.header("Invoice Configuration")
p_name = st.sidebar.text_input("Your Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")

st.sidebar.subheader("Default Client Info")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- PROCEDURAL DESIGN ENGINE ---
seed_raw = hashlib.md5(p_name.encode()).hexdigest()
s = int(seed_raw, 16)

# Generate unique design tokens
hue = s % 360 
prime = f"hsl({hue}, 75%, 20%)"
bg_light = f"hsl({hue}, 30%, 98%)"
font_stack = ["'Poppins'", "'Montserrat'", "'Inter'", "'Raleway'"][s % 4]
radius = (s % 20)
align = ["left", "center", "right"][s % 3]

# Generate unique footer text
adjs = ["Official", "Certified", "Authorized", "Verified"]
objs = ["Digital Document", "Electronic Invoice", "Service Record"]
footer_txt = f"{adjs[s % 4]} {objs[(s//2) % 3]}"

# --- THE HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@400;700&family=Inter:wght@400;700&family=Raleway:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* --- GLOBAL & PRINT RESET --- */
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: A4; margin: 0mm; }}
        html, body {{ margin: 0; padding: 0; width: 100%; background: #f0f2f5; }}
        
        /* --- MAIN WRAPPER (Prevents cutting) --- */
        .page-container {{ 
            width: 210mm; 
            min-height: 297mm; 
            padding: 20mm; 
            margin: 20px auto; 
            background: white; 
            font-family: {font_stack}, sans-serif;
            position: relative;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .invoice-header {{ 
            text-align: {align}; 
            border-bottom: 2px solid {prime}; 
            padding-bottom: 30px; 
            margin-bottom: 40px; 
        }}
        .invoice-header h1 {{ color: {prime}; font-size: 32px; margin: 0; text-transform: uppercase; }}
        
        .info-section {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .label {{ color: {prime}; font-weight: bold; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }}
        
        .item-table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        .item-table th {{ background: {prime}; color: white; padding: 15px; text-align: left; }}
        .item-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        
        .amt-words {{ background: {bg_light}; padding: 20px; border-left: 5px solid {prime}; margin: 25px 0; border-radius: 4px; font-style: italic; font-size: 14px; }}
        
        .invoice-footer {{ margin-top: 100px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-box {{ text-align: right; }}
        .sig-line {{ border-top: 2px solid #000; width: 200px; margin-top: 60px; margin-left: auto; }}
        
        .doc-verify {{ font-size: 11px; color: #999; font-style: italic; }}

        /* --- PRINT OVERRIDES --- */
        @media print {{
            body {{ background: none; }}
            .page-container {{ margin: 0; box-shadow: none; width: 100%; height: 100%; border: none; }}
            .no-print {{ display: none !important; }}
            /* Prevents browser from cutting the bottom */
            footer, header {{ display: none !important; }} 
        }}
    </style>
</head>
<body>
    <div class="page-container">
        <div class="invoice-header">
            <h1>{p_name}</h1>
            <div style="color: #666; margin-top: 5px;">{p_addr}</div>
        </div>

        <div class="info-section">
            <div>
                <div class="label">Billed To</div>
                <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
                <div style="white-space: pre-wrap; color: #444;">{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Summary</div>
                <strong>No: {inv_no}</strong><br>
                Date: {inv_date.strftime("%d %b, %Y")}
            </div>
        </div>

        <table class="item-table">
            <thead>
                <tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
            </tbody>
        </table>

        <div class="amt-words">
            <strong>Amount in words:</strong><br>{number_to_words(amt)}
        </div>

        <div class="invoice-footer">
            <div class="doc-verify">{footer_txt}.</div>
            <div class="sig-box">
                <div class="label">Total Due</div>
                <div style="font-size: 32px; font-weight: bold; color: {prime};">₹ {amt:,.2f}</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #777;">For {p_name}</div>
            </div>
        </div>
    </div>

    <div class="no-print" style="text-align: center; margin: 40px 0;">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 15px 50px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px;">
            🖨️ Print Full Page Invoice
        </button>
    </div>
</body>
</html>
"""

components.html(html_template, height=1300, scrolling=True)
