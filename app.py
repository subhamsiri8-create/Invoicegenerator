import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clean Professional Invoice", layout="wide")

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
st.sidebar.header("🎨 Style Selector")
style_id = st.sidebar.number_input("Enter Template ID (1-1000)", min_value=1, max_value=1000, value=1)

st.sidebar.markdown("---")
st.sidebar.header("📝 Business Details")
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")

st.sidebar.header("👤 Client Details")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.header("📊 Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Service Details")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- PROCEDURAL ENGINE ---
s = style_id
hues = [210, 160, 25, 340, 280, 200, 10, 120, 45, 190]
primary = f"hsl({hues[s % len(hues)]}, 75%, {25 + (s % 20)}%)"
bg_light = f"hsl({hues[s % len(hues)]}, 15%, 98%)"

font_options = [
    "'Poppins', sans-serif", "'Playfair Display', serif", "'Inter', sans-serif", 
    "'Montserrat', sans-serif", "'JetBrains Mono', monospace", "'Roboto Condensed', sans-serif"
]
selected_font = font_options[s % len(font_options)]

aligns = ["space-between", "center", "flex-start"]
h_align = aligns[s % 3]

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=JetBrains+Mono&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: A4; margin: 0; }}
        body {{ background: #f0f2f5; margin: 0; padding: 15px; font-family: {selected_font}; }}
        
        .invoice-card {{
            background: white; width: 210mm; min-height: 285mm;
            margin: auto; padding: 10mm; display: flex; flex-direction: column;
            border-top: 6px solid {primary};
        }}

        .header {{ 
            display: flex; justify-content: {h_align}; 
            align-items: center; margin-bottom: 25px; padding-bottom: 15px;
            border-bottom: 1px solid #eee;
            {f"text-align: center; flex-direction: column;" if h_align == 'center' else ""}
        }}
        
        .co-title {{ color: {primary}; font-size: 32px; font-weight: bold; text-transform: uppercase; margin: 0; }}
        .label {{ color: {primary}; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 2px; }}
        
        .table {{ width: 100%; border-collapse: collapse; }}
        .table th {{ background: {bg_light}; color: {primary}; text-align: left; padding: 12px; border-bottom: 2px solid {primary}; font-size: 11px; }}
        .table td {{ padding: 15px 12px; border-bottom: 1px solid #eee; font-size: 15px; }}
        
        .amt-words {{ background: {bg_light}; padding: 12px; border-left: 4px solid {primary}; font-style: italic; font-size: 12px; margin: 20px 0; }}
        
        .footer-aligned {{ display: flex; justify-content: flex-end; margin-top: 10px; }}
        .total-container {{ text-align: right; width: 240px; }}
        .grand-total {{ font-size: 34px; font-weight: bold; color: {primary}; margin: 0; }}
        .sig-line {{ border-top: 2px solid #000; width: 100%; margin-top: 40px; }}

        @media print {{
            header, footer, .stAppHeader, .stToolbar {{ display: none !important; }}
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
                <div style="color: #555; font-size: 12px; margin-top: 4px;">##PADDR##</div>
            </div>
            <div style="text-align: right; { 'margin-top: 20px;' if h_align == 'center' else '' }">
                <strong style="font-size: 18px; color: {primary};"># ##INVNO##</strong><br>
                <span style="font-size: 13px; font-weight: bold; color: #444;">##DATE##</span>
            </div>
        </div>

        <div style="margin-bottom: 25px;">
            <div class="label">Billed To</div>
            <div style="font-size: 20px; font-weight: bold; margin-top: 4px;">##CNAME##</div>
            <div style="white-space: pre-wrap; color: #444; line-height: 1.4; font-size: 14px;">##CADDR##</div>
        </div>

        <table class="table">
            <thead><tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="amt-words">
            <strong>Amount in Words:</strong> ##WORDS##
        </div>

        <div class="footer-aligned">
            <div class="total-container">
                <div class="label">Amount Payable</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; font-size: 12px; margin-top: 6px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {primary}; color: white; padding: 15px 60px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; letter-spacing: 1px;">
            PRINT CLEAN INVOICE
        </button>
    </div>
</body>
</html>
"""

# Replacement
final_html = html_template.replace("##PNAME##", p_name) \
                          .replace("##PADDR##", p_addr) \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##DESC##", desc) \
                          .replace("##AMT##", f"{amt:,.2f}") \
                          .replace("##WORDS##", number_to_words(amt))

components.html(final_html, height=1200, scrolling=True)
