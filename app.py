import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Invoice Designer", layout="wide")

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
st.sidebar.header("Dimensions")
size_options = {
    "A4 (Standard)": {"w": "210mm", "h": "297mm", "pg": "A4"},
    "Letter": {"w": "216mm", "h": "279mm", "pg": "letter"},
    "Half Sheet": {"w": "216mm", "h": "140mm", "pg": "landscape"},
    "Legal": {"w": "216mm", "h": "356mm", "pg": "legal"},
    "A5": {"w": "148mm", "h": "210mm", "pg": "A5"},
    "DL": {"w": "99mm", "h": "210mm", "pg": "DL"}
}
selected_size = st.sidebar.selectbox("Select Size", list(size_options.keys()))
dims = size_options[selected_size]

st.sidebar.header("Company Details")
p_name = st.sidebar.text_input("Your Company Name", "").upper()
p_addr = st.sidebar.text_area("Your Address", "")

st.sidebar.subheader("Client (Default: Vasavi)")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.subheader("Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- PROCEDURAL THEME ENGINE ---
seed_val = p_name if p_name else "BASE_STYLE"
s = int(hashlib.md5(seed_val.encode()).hexdigest(), 16)

# 1. Color Selection
hues = [210, 160, 25, 340, 280, 200, 10] # Blue, Green, Orange, Crimson, Purple, Cyan, Deep Red
primary = f"hsl({hues[s % len(hues)]}, 70%, 25%)"
accent_bg = f"hsl({hues[s % len(hues)]}, 20%, 97%)"

# 2. Style Logic
style_mode = s % 4 
font_f = ["'Poppins'", "'Inter'", "'Montserrat'", "'Playfair Display'"][s % 4]

# Style definitions
styles = {
    0: {"name": "Modern", "border": f"4px solid {primary}", "header_align": "space-between"},
    1: {"name": "Executive", "border": "none", "header_align": "center", "bg": primary, "text": "white"},
    2: {"name": "Minimal", "border": "1px solid #eee", "header_align": "flex-start"},
    3: {"name": "Creative", "border": f"1px dashed {primary}", "header_align": "space-between"}
}
curr_style = styles[style_mode]

# --- THE HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: {dims['pg']}; margin: 0; }}
        body {{ background: #f4f4f4; margin: 0; padding: 20px; font-family: {font_f}, sans-serif; }}
        
        .invoice-card {{
            background: white; width: {dims['w']}; min-height: {dims['h']};
            margin: auto; padding: 15mm; position: relative;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            display: flex; flex-direction: column;
            border-top: {curr_style.get('border', 'none')};
        }}

        .header {{ 
            display: flex; 
            justify-content: {curr_style['header_align']}; 
            align-items: center;
            margin-bottom: 40px; 
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
            {f"text-align: center; flex-direction: column;" if curr_style['header_align'] == 'center' else ""}
        }}
        
        .co-title {{ color: {primary}; font-size: 30px; font-weight: bold; text-transform: uppercase; margin: 0; }}
        .label {{ color: {primary}; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; flex-grow: 1; }}
        .table th {{ background: {primary if style_mode == 1 else '#f9f9f9'}; color: {'white' if style_mode == 1 else primary}; text-align: left; padding: 12px; }}
        .table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        
        .amt-words {{ background: {accent_bg}; padding: 15px; border-left: 4px solid {primary}; font-style: italic; font-size: 13px; margin: 25px 0; }}
        
        .footer-grid {{ margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; }}
        .grand-total {{ font-size: 32px; font-weight: bold; color: {primary}; }}
        .sig-line {{ border-top: 2px solid #333; width: 200px; margin-top: 50px; margin-left: auto; }}

        @media print {{
            header, footer, .stAppHeader, .stDecoration, .stToolbar {{ display: none !important; }}
            body {{ background: none; padding: 0; }}
            .invoice-card {{ box-shadow: none; margin: 0; width: 100%; border-left: none; border-right: none; border-bottom: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <div>
                <div class="co-title">##PNAME##</div>
                <div style="color: #666; font-size: 13px; margin-top: 5px;">##PADDR##</div>
            </div>
            <div style="{ 'margin-top: 20px;' if style_mode == 1 else '' }">
                <div class="label">Invoice No</div>
                <strong># ##INVNO##</strong><br>
                <span style="font-size: 13px;">##DATE##</span>
            </div>
        </div>

        <div style="margin-bottom: 30px;">
            <div class="label">Billed To</div>
            <div style="font-size: 18px; font-weight: bold; margin-top: 5px;">##CNAME##</div>
            <div style="white-space: pre-wrap; color: #444; line-height: 1.5;">##CADDR##</div>
        </div>

        <table class="table">
            <thead><tr><th>Service Description</th><th style="text-align: right;">Total Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold; font-size: 18px;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="amt-words">
            <strong>Amount in Words:</strong> ##WORDS##
        </div>

        <div class="footer-grid">
            <div style="font-size: 11px; color: #999;">{curr_style['name']} Series Document</div>
            <div style="text-align: right;">
                <div class="label">Total Amount Payable</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; font-size: 13px; margin-top: 5px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {primary}; color: white; padding: 15px 50px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
            PRINT {selected_size} INVOICE
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

components.html(final_html, height=1300, scrolling=True)
