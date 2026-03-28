import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dynamic Invoice Generator", layout="wide")

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

# --- SIDEBAR (ALL BLANK BY DEFAULT) ---
st.sidebar.header("Invoice Configuration")
p_name = st.sidebar.text_input("Your Company Name", "").upper()
p_addr = st.sidebar.text_area("Your Address", "")

st.sidebar.subheader("Client Details")
c_name = st.sidebar.text_input("Billed To", "")
c_addr = st.sidebar.text_area("Client Address", "")

inv_no = st.sidebar.text_input("Invoice #", "")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service Description", "")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- PROCEDURAL DESIGN ENGINE ---
# Seed is based on the company name; defaults to a neutral grey if name is empty
seed_input = p_name if p_name else "DEFAULT"
seed_raw = hashlib.md5(seed_input.encode()).hexdigest()
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
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: A4; margin: 0mm; }}
        html, body {{ margin: 0; padding: 0; width: 100%; background: #f0f2f5; }}
        
        .page-container {{ 
            width: 210mm; 
            min-height: 297mm; 
            padding: 20mm; 
            margin: 20px auto; 
            background: white; 
            font-family: {font_stack}, sans-serif;
            position: relative;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
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
        .item-table td {{ padding: 15px; border-bottom: 1px solid #eee; min-height: 50px; }}
        
        .amt-words {{ background: {bg_light}; padding: 20px; border-left: 5px solid {prime}; margin: 25px 0; border-radius: 4px; font-style: italic; font-size: 14px; }}
        
        .invoice-footer {{ margin-top: 100px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-box {{ text-align: right; }}
        .sig-line {{ border-top: 2px solid #000; width: 200px; margin-top: 60px; margin-left: auto; }}
        
        .doc-verify {{ font-size: 11px; color: #999; font-style: italic; }}

        @media print {{
            body {{ background: none; }}
            .page-container {{ margin: 0; box-shadow: none; width: 100%; height: 100%; border: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="page-container">
        <div class="invoice-header">
            <h1>{{p_name if p_name else "COMPANY NAME"}}</h1>
            <div style="color: #666; margin-top: 5px;">{{p_addr if p_addr else "Company Address"}}</div>
        </div>

        <div class="info-section">
            <div>
                <div class="label">Billed To</div>
                <div style="font-size: 18px; font-weight: bold;">{{c_name if c_name else "Client Name"}}</div>
                <div style="white-space: pre-wrap; color: #444;">{{c_addr if c_addr else "Client Address"}}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Summary</div>
                <strong>No: {{inv_no if inv_no else "---"}}</strong><br>
                Date: {{inv_date.strftime("%d %b, %Y")}}
            </div>
        </div>

        <table class="item-table">
            <thead>
                <tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{{desc if desc else "Service Details"}}</td><td style="text-align: right; font-weight: bold;">₹ {{amt:,.2f}}</td></tr>
            </tbody>
        </table>

        <div class="amt-words">
            <strong>Amount in words:</strong><br>{{number_to_words(amt)}}
        </div>

        <div class="invoice-footer">
            <div class="doc-verify">{footer_txt}.</div>
            <div class="sig-box">
                <div class="label">Total Due</div>
                <div style="font-size: 32px; font-weight: bold; color: {prime};">₹ {{amt:,.2f}}</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #777;">For {{p_name if p_name else "Company"}}</div>
            </div>
        </div>
    </div>

    <div class="no-print" style="text-align: center; margin: 40px 0;">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 15px 50px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">
            🖨️ Print Invoice
        </button>
    </div>
</body>
</html>
"""

# Using Python f-string formatting for the seed-based tokens and regular string replacement for input data
# This prevents errors if braces are used in the text areas.
components.html(html_template.replace("{{p_name}}", p_name or "COMPANY NAME")
                            .replace("{{p_addr}}", p_addr or "Company Address")
                            .replace("{{c_name}}", c_name or "Client Name")
                            .replace("{{c_addr}}", c_addr or "Client Address")
                            .replace("{{inv_no}}", inv_no or "---")
                            .replace("{{desc}}", desc or "Service Details")
                            .replace("{{amt}}", f"{amt:,.2f}"), height=1300, scrolling=True)
