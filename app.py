import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Invoice Studio", layout="wide")

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
st.sidebar.header("🎨 Professional Presets")
template_id = st.sidebar.slider("Select Design Variant", 1, 1000, 101)

st.sidebar.markdown("---")
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS").upper() #
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh") #

st.sidebar.header("👤 Client")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED") #
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com") #

st.sidebar.header("📊 Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-88")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Digital Marketing Services")
amt = st.sidebar.number_input("Total Amount (INR)", value=15000.0)

# --- REALISM ENGINE ---
s = template_id
hues = [215, 140, 30, 0, 260, 200]
primary = f"hsl({hues[s % len(hues)]}, 85%, 20%)"
accent = f"hsl({hues[s % len(hues)]}, 85%, 96%)"

# Professional Font Pairings (Heading | Body)
font_pairs = [
    ("'Inter'", "'Inter'"), 
    ("'Playfair Display'", "'Montserrat'"),
    ("'Roboto'", "'Open Sans'"),
    ("'Montserrat'", "'Lato'")
]
h_font, b_font = font_pairs[s % len(font_pairs)]

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&family=Roboto:wght@400;700&family=Open+Sans&family=Lato&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        body {{ background: #eef0f3; margin: 0; padding: 20px; font-family: {b_font}, sans-serif; color: #333; }}
        
        .invoice-card {{
            background: white; width: 210mm; min-height: 297mm;
            margin: auto; padding: 15mm; position: relative;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }}

        /* Subtle Background Watermark for Realism */
        .invoice-card::after {{
            content: "ORIGINAL INVOICE"; position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 80px; font-weight: bold; color: rgba(0,0,0,0.02);
            pointer-events: none; z-index: 0;
        }}

        .top-header {{ display: flex; justify-content: space-between; border-bottom: 2px solid {primary}; padding-bottom: 15px; margin-bottom: 20px; }}
        .co-info h1 {{ font-family: {h_font}; color: {primary}; margin: 0; font-size: 26px; text-transform: uppercase; }}
        
        .status-badge {{
            background: {accent}; color: {primary}; padding: 5px 15px;
            border-radius: 4px; font-weight: bold; font-size: 12px; border: 1px solid {primary};
        }}

        .info-grid {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
        .label {{ font-size: 10px; font-weight: bold; color: #888; text-transform: uppercase; margin-bottom: 5px; }}

        .main-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; z-index: 1; position: relative; }}
        .main-table th {{ background: {primary}; color: white; text-align: left; padding: 12px; font-size: 12px; text-transform: uppercase; }}
        .main-table td {{ padding: 15px 12px; border-bottom: 1px solid #eee; font-size: 14px; }}
        
        .words-section {{ margin-top: 20px; font-size: 12px; color: #555; font-style: italic; border-left: 3px solid {primary}; padding-left: 10px; }}

        /* TIGHT BOTTOM ALIGNMENT */
        .summary-block {{ display: flex; justify-content: flex-end; margin-top: 15px; }}
        .total-box {{ width: 240px; text-align: right; }}
        .total-row {{ display: flex; justify-content: space-between; padding: 5px 0; border-top: 1px solid #eee; }}
        .grand-total {{ font-size: 28px; font-weight: bold; color: {primary}; margin: 5px 0; }}
        
        .signature-area {{ margin-top: 30px; border-top: 1.5px solid #000; padding-top: 5px; }}

        @media print {{
            header, .stAppHeader, .stToolbar, .no-print {{ display: none !important; }}
            body {{ background: none; padding: 0; }}
            .invoice-card {{ box-shadow: none; margin: 0; width: 100%; border: none; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="top-header">
            <div class="co-info">
                <h1>##PNAME##</h1>
                <div style="font-size: 12px; color: #666;">##PADDR##</div>
            </div>
            <div style="text-align: right;">
                <div class="status-badge">TAX INVOICE</div>
                <div style="margin-top: 10px; font-size: 13px;">
                    <strong>Invoice:</strong> ##INVNO##<br>
                    <strong>Date:</strong> ##DATE##
                </div>
            </div>
        </div>

        <div class="info-grid">
            <div>
                <div class="label">Bill To</div>
                <div style="font-size: 16px; font-weight: bold;">##CNAME##</div>
                <div style="white-space: pre-wrap; font-size: 13px; color: #444; line-height: 1.4;">##CADDR##</div>
            </div>
        </div>

        <table class="main-table">
            <thead><tr><th>Description of Services</th><th style="text-align: right;">Amount (INR)</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="words-section">
            <strong>Amount in Words:</strong> ##WORDS##
        </div>

        <div class="summary-block">
            <div class="total-box">
                <div class="total-row"><span>Sub-Total:</span><span>₹ ##AMT##</span></div>
                <div class="grand-total">₹ ##AMT##</div>
                <div class="signature-area">
                    <div style="font-size: 11px; font-weight: bold;">Authorized Signatory</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {primary}; color: white; padding: 12px 40px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; transition: 0.3s;">
            GENERATE PROFESSIONAL PDF
        </button>
    </div>
</body>
</html>
"""

# Rendering Logic
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
