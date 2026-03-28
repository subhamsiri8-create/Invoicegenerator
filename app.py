import streamlit as st
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
        if n > 0:
            res += convert_less_than_thousand(n)
        return res.strip()

    num_int = int(num)
    num_dec = int(round((num - num_int) * 100))
    words = convert(num_int) + " Rupees"
    if num_dec > 0:
        words += " and " + convert(num_dec) + " Paise"
    return words + " Only"

# --- SIDEBAR INPUTS ---
st.sidebar.header("📋 Invoice Details")
p_name = st.sidebar.text_input("Your Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")

st.sidebar.markdown("---")
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")

st.sidebar.markdown("---")
inv_no = st.sidebar.text_input("Invoice Number", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service Description", "Digital Marketing & Branding")
amt = st.sidebar.number_input("Amount (INR)", min_value=0.0, value=15000.0)

# --- DYNAMIC STYLING ENGINE ---
# This creates one of 50,000+ styles based on the company name
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)
hue = (seed % 360)
primary_color = "hsl({}, 65%, 30%)".format(hue)
light_bg = "hsl({}, 40%, 98%)".format(hue)

# --- HTML TEMPLATE ---
# Note: CSS uses doubled braces {{ }} to prevent Python errors
invoice_template = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
<style>
    .invoice-wrapper {{
        background-color: white;
        font-family: 'Poppins', sans-serif;
        max-width: 800px;
        margin: 30px auto;
        padding: 50px;
        border-top: 15px solid {color};
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        color: #333;
    }}
    .header-section {{ text-align: center; border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 40px; }}
    .header-section h1 {{ color: {color}; margin: 0; font-size: 32px; letter-spacing: 1px; }}
    
    .meta-grid {{ display: flex; justify-content: space-between; margin-bottom: 50px; }}
    .meta-label {{ color: {color}; font-weight: bold; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }}
    
    .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
    .data-table th {{ background: {color}; color: white; padding: 12px; text-align: left; text-transform: uppercase; font-size: 13px; }}
    .data-table td {{ padding: 15px; border-bottom: 1px solid #eee; font-size: 15px; }}
    
    .amount-box {{ text-align: right; margin-top: 20px; }}
    .total-text {{ font-size: 30px; font-weight: bold; color: {color}; }}
    
    .words-section {{ background: {bg}; padding: 15px; border-left: 5px solid {color}; margin-top: 20px; font-style: italic; font-size: 13px; }}

    .footer-area {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 70px; }}
    .sig-section {{ text-align: right; }}
    .sig-line {{ border-top: 2px solid #333; width: 220px; display: inline-block; margin-top: 50px; }}
    .sig-title {{ font-weight: bold; font-size: 14px; margin-top: 5px; }}

    @media print {{
        header, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .no-print {{
            display: none !important;
        }}
        .invoice-wrapper {{
            box-shadow: none;
            border: 1px solid #eee;
            margin: 0;
            padding: 20px;
            width: 100%;
        }}
        body {{ background: white; }}
    }}
</style>

<div class="invoice-wrapper">
    <div class="header-section">
        <h1>{p_name}</h1>
        <div style="color: #666;">{p_addr}</div>
    </div>
    
    <div class="meta-grid">
        <div>
            <div class="meta-label">Billed To</div>
            <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
            <div style="color: #555;">{c_addr}</div>
        </div>
        <div style="text-align: right;">
            <div class="meta-label">Invoice Details</div>
            <strong>No: {inv_no}</strong><br>
            Date: {date}
        </div>
    </div>

    <table class="data-table">
        <thead>
            <tr><th>Description</th><th style="text-align: right;">Amount</th></tr>
        </thead>
        <tbody>
            <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
        </tbody>
    </table>

    <div class="words-section">Rupees in words: <strong>{words}</strong></div>
    
    <div class="footer-area">
        <div style="color: #888; font-size: 12px;">Payment is due within 15 days.</div>
        <div class="sig-section">
            <div class="amount-box">
                <div class="meta-label">Grand Total Due</div>
                <div class="total-text">₹ {amt:,.2f}</div>
            </div>
            <div class="sig-line"></div>
            <div class="sig-title">Authorized Signatory</div>
            <div style="font-size: 11px; color: #777;">For {p_name}</div>
        </div>
    </div>
</div>

<div class="no-print" style="text-align: center; margin: 40px;">
    <button onclick="window.print()" style="
        background: {color}; 
        color: white; 
        padding: 12px 40px; 
        border: none; 
        border-radius: 6px; 
        font-weight: bold; 
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    ">
        🖨️ Print Invoice / Save as PDF
    </button>
</div>
"""

# --- INJECT DATA AND RENDER ---
st.markdown(
    invoice_template.format(
        color=primary_color,
        bg=light_bg,
        p_name=p_name,
        p_addr=p_addr,
        c_name=c_name,
        c_addr=c_addr,
        inv_no=inv_no,
        date=inv_date.strftime("%d %b, %Y"),
        desc=desc,
        amt=amt,
        words=number_to_words(amt)
    ),
    unsafe_allow_html=True
)
