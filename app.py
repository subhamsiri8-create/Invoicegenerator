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

# --- SIDEBAR: DYNAMIC STYLE SELECTION ---
st.sidebar.header("🎨 Template Selection")
# User can type any number from 1 to 1000 to change the entire look
style_index = st.sidebar.number_input("Select Template ID (1-1000)", min_value=1, max_value=1000, value=1)

st.sidebar.markdown("---")
st.sidebar.header("📝 Business Details")
p_name = st.sidebar.text_input("Your Company", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")

st.sidebar.header("👤 Client Details")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.header("📊 Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Service Details")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- THE PROCEDURAL STYLE ENGINE ---
# We use the style_index to derive all design properties mathematically
s = style_index 
hues = [210, 160, 25, 340, 280, 200, 10, 120, 50, 300]
primary_color = f"hsl({hues[s % len(hues)]}, 70%, {20 + (s % 30)}%)"
bg_tint = f"hsl({hues[s % len(hues)]}, 10%, 98%)"
fonts = ["'Poppins'", "'Inter'", "'Montserrat'", "'Roboto'", "'Open Sans'", "'Lato'"]
selected_font = fonts[s % len(fonts)]

# Layout variations based on index
alignments = ["flex-start", "center", "space-between"]
header_align = alignments[s % 3]
border_styles = [f"5px solid {primary_color}", "none", "1px solid #eee", f"2px dashed {primary_color}"]
current_border = border_styles[s % 4]

# --- DYNAMIC HTML ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        body {{ background: #f4f4f4; margin: 0; padding: 20px; font-family: {selected_font}, sans-serif; }}
        
        .invoice-card {{
            background: white; width: 210mm; min-height: 297mm;
            margin: auto; padding: 12mm; position: relative;
            display: flex; flex-direction: column;
            border-top: {current_border};
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }}

        .header {{ 
            display: flex; 
            justify-content: {header_align}; 
            align-items: center;
            margin-bottom: 20px; 
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
            {f"text-align: center; flex-direction: column;" if header_align == 'center' else ""}
        }}
        
        .co-title {{ color: {primary_color}; font-size: 28px; font-weight: bold; text-transform: uppercase; margin: 0; }}
        .label {{ color: {primary_color}; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .table th {{ background: {bg_tint}; color: {primary_color}; text-align: left; padding: 10px; border-bottom: 2px solid {primary_color}; }}
        .table td {{ padding: 12px 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
        
        .amt-words {{ background: {bg_tint}; padding: 10px; border-left: 4px solid {primary_color}; font-style: italic; font-size: 12px; margin: 15px 0; }}
        
        .footer-wrap {{ display: flex; justify-content: flex-end; margin-top: 10px; }}
        .total-box {{ text-align: right; width: 250px; }}
        .grand-total {{ font-size: 30px; font-weight: bold; color: {primary_color}; margin: 5px 0; }}
        .sig-line {{ border-top: 1.5px solid #000; width: 100%; margin-top: 40px; }}

        @media print {{
            header, footer, .stAppHeader, .stToolbar {{ display: none !important; }}
            body {{ background: none; padding: 0; }}
            .invoice-card {{ box-shadow: none; margin: 0; width: 100%; border-left: none; border-right: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <div>
                <div class="co-title">##PNAME##</div>
                <div style="color: #666; font-size: 12px;">##PADDR##</div>
            </div>
            <div style="text-align: right; { 'margin-top: 15px;' if header_align == 'center' else '' }">
                <div class="label">Invoice Details</div>
                <strong># ##INVNO##</strong><br>
                <span>##DATE##</span>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <div class="label">Billed To</div>
            <div style="font-size: 18px; font-weight: bold; margin-top: 5px;">##CNAME##</div>
            <div style="white-space: pre-wrap; color: #444; line-height: 1.4;">##CADDR##</div>
        </div>

        <table class="table">
            <thead><tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="amt-words">
            <strong>In Words:</strong> ##WORDS##
        </div>

        <div class="footer-wrap">
            <div class="total-box">
                <div class="label">Amount Payable</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; font-size: 12px; margin-top: 5px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {primary_color}; color: white; padding: 15px 50px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">
            PRINT TEMPLATE #{s}
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

components.html(final_html, height=1200, scrolling=True)
