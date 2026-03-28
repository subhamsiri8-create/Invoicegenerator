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
st.sidebar.header("Invoice Details")
p_name = st.sidebar.text_input("Your Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")

st.sidebar.subheader("Client Details")
# Defaulting to Vasavi Silks details as requested
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service Description", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- GENERATIVE DESIGN ENGINE ---
seed_raw = hashlib.md5(p_name.encode()).hexdigest()
s = int(seed_raw, 16)

# Procedural properties
hue = s % 360 
border_radius = (s % 25)
font_choice = ["'Poppins'", "'Montserrat'", "'Raleway'", "'Inter'", "'Playfair Display'"][s % 5]
header_align = ["left", "center", "right"][s % 3]
prime = f"hsl({hue}, 75%, 20%)"
bg_tint = f"hsl({hue}, 30%, 98%)"

# NEW: DYNAMIC FOOTER TEXT VARIATIONS
footer_variants = [
    "🛡️ Authorized Digital Document",
    "✅ Verified Electronic Invoice",
    "✨ System Generated Official Record",
    "📜 Authenticated Billing Statement",
    "💎 Premium Service Receipt",
    "🔒 Secure Digital Transaction"
]
selected_footer = footer_variants[s % len(footer_variants)]

# --- THE GENERATIVE HTML ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@400;700&family=Raleway:wght@400;700&family=Inter:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{ size: auto; margin: 0mm; }}
        body {{ background: #fdfdfd; margin: 0; padding: 40px; font-family: {font_choice}, sans-serif; }}
        .invoice-card {{
            max-width: 850px; margin: auto; background: white; padding: 50px;
            border-top: 12px solid {prime};
            border-radius: {border_radius}px;
            box-shadow: 0 15px 50px rgba(0,0,0,0.1);
        }}
        .header {{ text-align: {header_align}; margin-bottom: 50px; border-bottom: 1px solid #eee; padding-bottom: 25px; }}
        .header h1 {{ color: {prime}; font-size: 32px; text-transform: uppercase; margin: 0; letter-spacing: 1px; }}
        .grid {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .label {{ color: {prime}; font-weight: bold; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }}
        .table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        .table th {{ background: {prime}; color: white; padding: 15px; text-align: left; }}
        .table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .words-box {{ background: {bg_tint}; padding: 20 :px; border-left: 6px solid {prime}; border-radius: 4px; margin: 20px 0; font-style: italic; }}
        .footer {{ margin-top: 70px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-line {{ border-top: 2px solid #333; width: 220px; margin-top: 50px; }}
        
        /* Styled Dynamic Footer Text */
        .dynamic-footer-text {{ 
            font-size: 12px; 
            color: {prime}; 
            opacity: 0.7; 
            font-weight: 600;
            letter-spacing: 0.5px;
        }}

        @media print {{
            body {{ background: white; padding: 15mm; }}
            .invoice-card {{ box-shadow: none; border: 1px solid #eee; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <h1>{p_name}</h1>
            <div style="color: #666; font-size: 14px; margin-top: 5px;">{p_addr}</div>
        </div>
        <div class="grid">
            <div>
                <div class="label">Billed To</div>
                <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
                <div style="white-space: pre-wrap; color: #444;">{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Details</div>
                <strong># {inv_no}</strong><br>
                {inv_date.strftime("%d %b, %Y")}
            </div>
        </div>
        <table class="table">
            <thead><tr><th>Description of Service</th><th style="text-align: right;">Amount</th></tr></thead>
            <tbody><tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr></tbody>
        </table>
        <div class="words-box"><strong>Rupees in Words:</strong><br>{number_to_words(amt)}</div>
        <div class="footer">
            <div class="dynamic-footer-text">{selected_footer}</div>
            <div style="text-align: right;">
                <div class="label">Grand Total</div>
                <div style="font-size: 32px; font-weight: bold; color: {prime};">₹ {amt:,.2f}</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #888;">For {p_name}</div>
            </div>
        </div>
    </div>
    <div style="text-align: center; margin-top: 40px;" class="no-print">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 15px 45px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">Print Invoice</button>
    </div>
</body>
</html>
"""

components.html(html_template, height=1200, scrolling=True)
