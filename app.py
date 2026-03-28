import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Professional Invoice Studio", layout="wide")

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
st.sidebar.header("1. Document Size")
inv_size = st.sidebar.radio("Select Print Size", ["Standard A4", "Compact Receipt"])

st.sidebar.header("2. Company Info")
p_name = st.sidebar.text_input("Your Company Name", "").upper()
p_addr = st.sidebar.text_area("Your Address", "")

st.sidebar.subheader("3. Client Details")
# Defaulting to Vasavi Silks as requested
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.subheader("4. Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service Description", "")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- PROCEDURAL DESIGN ENGINE ---
seed_input = p_name if p_name else "DEFAULT"
s = int(hashlib.md5(seed_input.encode()).hexdigest(), 16)

# Design Tokens
hue = s % 360 
prime = f"hsl({hue}, 70%, 25%)"
bg_soft = f"hsl({hue}, 20%, 97%)"
font = ["'Poppins'", "'Inter'", "'Montserrat'", "'Playfair Display'"][s % 4]
layout_mode = s % 3 # 0: Modern, 1: Classic, 2: Minimalist

# Physical Dimensions
width = "210mm" if inv_size == "Standard A4" else "120mm"
min_height = "297mm" if inv_size == "Standard A4" else "180mm"

# Procedural Layout Logic
header_style = "display: flex; justify-content: space-between;" if layout_mode == 0 else "text-align: center;"
table_style = "border: 1px solid #eee;" if layout_mode == 1 else "border: none;"

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: {inv_size.split()[-1]}; margin: 0mm; }}
        body {{ background: #f4f7f6; margin: 0; padding: 20px; font-family: {font}, sans-serif; }}
        
        .invoice-box {{
            width: {width};
            min-height: {min_height};
            padding: 15mm;
            margin: auto;
            background: white;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            position: relative;
        }}

        .header-bar {{ {header_style} border-bottom: 4px solid {prime}; padding-bottom: 20px; margin-bottom: 30px; }}
        .header-bar h1 {{ color: {prime}; margin: 0; text-transform: uppercase; font-size: 28px; }}
        
        .meta-grid {{ display: flex; justify-content: space-between; margin-bottom: 40px; font-size: 14px; }}
        .label {{ color: {prime}; font-weight: bold; font-size: 10px; text-transform: uppercase; margin-bottom: 4px; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; {table_style} }}
        .main-table th {{ background: {prime}; color: white; padding: 12px; text-align: left; }}
        .main-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        
        .words-section {{ background: {bg_soft}; padding: 15px; border-radius: 4px; border-left: 4px solid {prime}; margin: 20px 0; font-style: italic; font-size: 13px; }}
        
        .footer-area {{ margin-top: 60px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .total-display {{ color: {prime}; font-size: 32px; font-weight: bold; }}
        .signature-line {{ border-top: 2px solid #333; width: 180px; margin-top: 50px; margin-left: auto; }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .invoice-box {{ box-shadow: none; margin: 0; width: 100%; border: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-box">
        <div class="header-bar">
            <div>
                <h1>{{p_name}}</h1>
                <div style="color: #666;">{{p_addr}}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice #</div>
                <strong>{{inv_no}}</strong><br>
                {{inv_date}}
            </div>
        </div>

        <div class="meta-grid">
            <div>
                <div class="label">Client Information</div>
                <div style="font-size: 16px; font-weight: bold;">{{c_name}}</div>
                <div style="white-space: pre-wrap;">{{c_addr}}</div>
            </div>
        </div>

        <table class="main-table">
            <thead>
                <tr><th>Description of Service</th><th style="text-align: right;">Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{{desc}}</td><td style="text-align: right; font-weight: bold;">₹ {{amt}}</td></tr>
            </tbody>
        </table>

        <div class="words-section">
            <strong>Amount in words:</strong><br>{{words}}
        </div>

        <div class="footer-area">
            <div style="font-size: 11px; color: #999;">System Generated Official Record.</div>
            <div style="text-align: right;">
                <div class="label">Total Amount Due</div>
                <div class="total-display">₹ {{amt}}</div>
                <div class="signature-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #777;">For {{p_name}}</div>
            </div>
        </div>
    </div>

    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 14px 40px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
            🖨️ Print {inv_size} Invoice
        </button>
    </div>
</body>
</html>
"""

# Manual placeholder replacement for safety
final_html = html_template.replace("{{p_name}}", p_name if p_name else "YOUR COMPANY") \
                          .replace("{{p_addr}}", p_addr if p_addr else "Address Line") \
                          .replace("{{c_name}}", c_name if c_name else "Client Name") \
                          .replace("{{c_addr}}", c_addr if c_addr else "Client Details") \
                          .replace("{{inv_no}}", inv_no if inv_no else "---") \
                          .replace("{{inv_date}}", inv_date.strftime("%d %b, %Y")) \
                          .replace("{{desc}}", desc if desc else "Service Description") \
                          .replace("{{amt}}", f"{amt:,.2f}") \
                          .replace("{{words}}", number_to_words(amt))

components.html(final_html, height=1400, scrolling=True)
