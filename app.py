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

# --- SIDEBAR: DIMENSION ENGINE ---
st.sidebar.header("1. Paper Dimensions")
size_options = {
    "A4 (Standard)": {"w": "210mm", "h": "297mm", "pg": "A4"},
    "Letter (US/Canada)": {"w": "216mm", "h": "279mm", "pg": "letter"},
    "Half Sheet (Invoice Book)": {"w": "216mm", "h": "140mm", "pg": "landscape"},
    "Legal (Detailed)": {"w": "216mm", "h": "356mm", "pg": "legal"},
    "A5 (Compact/Receipt)": {"w": "148mm", "h": "210mm", "pg": "A5"},
    "DL (Envelope Friendly)": {"w": "99mm", "h": "210mm", "pg": "DL"}
}
selected_size = st.sidebar.selectbox("Select Invoice Size", list(size_options.keys()))
dims = size_options[selected_size]

st.sidebar.header("2. Company Info")
p_name = st.sidebar.text_input("Your Company Name", "").upper()
p_addr = st.sidebar.text_area("Your Address", "")

st.sidebar.subheader("3. Client Details")
# Defaulting to Vasavi Silks
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.subheader("4. Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- PROCEDURAL DESIGN ENGINE ---
seed_val = p_name if p_name else "BASE"
s = int(hashlib.md5(seed_val.encode()).hexdigest(), 16)
hue = s % 360
prime = f"hsl({hue}, 75%, 20%)"
font_choice = ["'Poppins'", "'Inter'", "'Montserrat'"][s % 3]

# --- HTML TEMPLATE (Safe Placeholder Method) ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: {dims['pg']}; margin: 0; }}
        body {{ background: #f0f2f5; margin: 0; padding: 20px; font-family: {font_choice}, sans-serif; }}
        
        .invoice-card {{
            background: white; width: {dims['w']}; min-height: {dims['h']};
            margin: auto; padding: 12mm; position: relative;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            overflow: hidden; display: flex; flex-direction: column;
        }}

        .top-accent {{ height: 6px; background: {prime}; margin: -12mm -12mm 20px -12mm; }}
        .header {{ display: flex; justify-content: space-between; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
        .co-title {{ color: {prime}; font-size: 24px; font-weight: bold; text-transform: uppercase; }}
        
        .label {{ color: {prime}; font-size: 10px; font-weight: bold; text-transform: uppercase; margin-bottom: 3px; }}
        .info-grid {{ display: flex; justify-content: space-between; margin-bottom: 30px; font-size: 13px; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-top: 10px; flex-grow: 1; }}
        .table th {{ background: #f8f9fa; color: {prime}; text-align: left; padding: 10px; border-bottom: 2px solid {prime}; font-size: 12px; }}
        .table td {{ padding: 12px 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
        
        .amt-words {{ background: #fafafa; padding: 12px; border-left: 4px solid {prime}; font-style: italic; font-size: 12px; margin: 20px 0; }}
        
        .footer-section {{ margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; padding-top: 20px; }}
        .total-box {{ text-align: right; }}
        .grand-total {{ font-size: 28px; font-weight: bold; color: {prime}; }}
        .sig-line {{ border-top: 1.5px solid #000; width: 180px; margin-top: 40px; margin-left: auto; }}

        @media print {{
            body {{ background: none; padding: 0; }}
            .invoice-card {{ box-shadow: none; margin: 0; width: 100%; border: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="top-accent"></div>
        <div class="header">
            <div>
                <div class="co-title">##PNAME##</div>
                <div style="color: #666; font-size: 12px;">##PADDR##</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Summary</div>
                <strong># ##INVNO##</strong><br>
                <span style="font-size: 12px;">##DATE##</span>
            </div>
        </div>

        <div class="info-grid">
            <div>
                <div class="label">Billed To</div>
                <div style="font-size: 16px; font-weight: bold;">##CNAME##</div>
                <div style="white-space: pre-wrap; color: #444; line-height: 1.4;">##CADDR##</div>
            </div>
        </div>

        <table class="table">
            <thead><tr><th>Description</th><th style="text-align: right;">Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="amt-words">
            <strong>In Words:</strong> ##WORDS##
        </div>

        <div class="footer-section">
            <div style="font-size: 10px; color: #999;"></div>
            <div class="total-box">
                <div class="label">Total Amount Payable</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; font-size: 12px; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 10px; color: #777;">For ##PNAME##</div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 12px 40px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">
            PRINT {selected_size.upper()}
        </button>
    </div>
</body>
</html>
"""

# Dynamic Replacement
final_html = html_template.replace("##PNAME##", p_name if p_name else "COMPANY NAME") \
                          .replace("##PADDR##", p_addr if p_addr else "Company Address") \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##DESC##", desc if desc else "Service Details") \
                          .replace("##AMT##", f"{amt:,.2f}") \
                          .replace("##WORDS##", number_to_words(amt))

components.html(final_html, height=1200, scrolling=True)
