import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Compact Invoice Studio", layout="wide")

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
st.sidebar.header("Configuration")
size_options = {
    "A4 (Standard)": {"w": "210mm", "h": "297mm", "pg": "A4"},
    "Letter": {"w": "216mm", "h": "279mm", "pg": "letter"},
    "Half Sheet": {"w": "216mm", "h": "140mm", "pg": "landscape"},
    "Legal": {"w": "216mm", "h": "356mm", "pg": "legal"},
    "A5": {"w": "148mm", "h": "210mm", "pg": "A5"},
    "DL": {"w": "99mm", "h": "210mm", "pg": "DL"}
}
selected_size = st.sidebar.selectbox("Paper Size", list(size_options.keys()))
dims = size_options[selected_size]

# Defaulting to your company details
p_name = st.sidebar.text_input("Your Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")

st.sidebar.markdown("---")
# Presetting Billed To details
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Service Details")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- THEME ENGINE ---
seed_val = p_name if p_name else "BASE"
s = int(hashlib.md5(seed_val.encode()).hexdigest(), 16)
hues = [210, 160, 25, 340, 280, 200, 10]
primary = f"hsl({hues[s % len(hues)]}, 70%, 25%)"
font_f = ["'Poppins'", "'Inter'", "'Montserrat'"][s % 3]

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: {dims['pg']}; margin: 0; }}
        body {{ background: #f0f2f5; margin: 0; padding: 10px; font-family: {font_f}, sans-serif; }}
        
        .invoice-card {{
            background: white; width: {dims['w']}; min-height: {dims['h']};
            margin: auto; padding: 10mm; position: relative;
            display: flex; flex-direction: column;
        }}

        .header {{ 
            display: flex; justify-content: space-between; 
            margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #eee; 
        }}
        .co-title {{ color: {primary}; font-size: 22px; font-weight: bold; margin: 0; line-height: 1; }}
        .label {{ color: {primary}; font-size: 9px; font-weight: bold; text-transform: uppercase; margin-bottom: 1px; }}
        
        .info-grid {{ display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 12px; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-top: 0; }}
        .table th {{ background: #f8f9fa; color: {primary}; text-align: left; padding: 4px 10px; border-bottom: 2.5px solid {primary}; font-size: 11px; }}
        .table td {{ padding: 6px 10px; border-bottom: 1px solid #eee; font-size: 14px; vertical-align: top; }}
        
        .amt-words {{ background: #fafafa; padding: 8px; border-left: 3px solid {primary}; font-style: italic; font-size: 11px; margin: 8px 0; }}
        
        /* ALIGNED FOOTER LOGIC */
        .footer {{ margin-top: auto; display: flex; justify-content: flex-end; padding-top: 5px; }}
        .total-container {{ text-align: right; width: 220px; }}
        .grand-total {{ font-size: 26px; font-weight: bold; color: {primary}; margin: 0; }}
        .sig-line {{ border-top: 1.5px solid #000; width: 100%; margin-top: 30px; }}

        @media print {{
            header, footer, .stAppHeader, .stDecoration, .stToolbar {{ display: none !important; }}
            body {{ background: none; padding: 0; }}
            .invoice-card {{ box-shadow: none; margin: 0; width: 100%; border: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <div>
                <div class="co-title">##PNAME##</div>
                <div style="color: #666; font-size: 11px;">##PADDR##</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice</div>
                <strong style="font-size: 14px;"># ##INVNO##</strong><br>
                <span style="font-size: 11px;">##DATE##</span>
            </div>
        </div>

        <div class="info-grid">
            <div>
                <div class="label">Billed To</div>
                <div style="font-size: 15px; font-weight: bold;">##CNAME##</div>
                <div style="white-space: pre-wrap; color: #444; line-height: 1.2;">##CADDR##</div>
            </div>
        </div>

        <table class="table">
            <thead><tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="amt-words">
            <strong>In Words:</strong> ##WORDS##
        </div>

        <div class="footer">
            <div class="total-container">
                <div class="label">Amount Payable</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; font-size: 11px; margin-top: 3px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 20px;">
        <button onclick="window.print()" style="background: {primary}; color: white; padding: 10px 30px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">
            PRINT CLEAN INVOICE
        </button>
    </div>
</body>
</html>
"""

# Dynamic Replacement
final_html = html_template.replace("##PNAME##", p_name) \
                          .replace("##PADDR##", p_addr) \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##DESC##", desc) \
                          .replace("##AMT##", f"{amt:,.2f}") \
                          .replace("##WORDS##", number_to_words(amt))

components.html(final_html, height=1300, scrolling=True)
