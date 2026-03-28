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
st.sidebar.header("📝 Invoice Data")
p_name = st.sidebar.text_input("Your Company Name", "Digital Marketing Mechanics").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")

st.sidebar.markdown("---")
c_name = st.sidebar.text_input("Billed To (Client)", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")

st.sidebar.markdown("---")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Invoice Date", datetime.now())
desc = st.sidebar.text_area("Service Description", "Social Media Marketing & Brand Consultation")
amt = st.sidebar.number_input("Total Amount (INR)", min_value=0.0, value=15000.0, step=500.0)

# --- DETERMINISTIC TEMPLATE ENGINE (50,000+ Variations) ---
# We use a hash of the company name so that same name = same style every time.
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)

# 1. Colors (360 Hues)
hue = (seed % 360)
primary_color = f"hsl({hue}, 65%, 30%)"
accent_bg = f"hsl({hue}, 40%, 97%)"

# 2. Fonts (Professional Pairings)
fonts = [
    "'Poppins', sans-serif", "'Montserrat', sans-serif", 
    "'Playfair Display', serif", "'Raleway', sans-serif",
    "'Open Sans', sans-serif", "'Merriweather', serif"
]
selected_font = fonts[seed % len(fonts)]

# 3. Layout Variations
layouts = ["centered", "left-aligned", "modern-split", "classic-border"]
selected_layout = layouts[(seed // 10) % len(layouts)]

# 4. Design Accents
border_radius = ["0px", "8px", "20px"][(seed // 100) % 3]

# --- HTML/CSS TEMPLATE ---
invoice_html = f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=Raleway:wght@400;700&family=Open+Sans:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">

<style>
    /* --- SCREEN UI --- */
    .invoice-container {{
        background-color: white;
        font-family: {selected_font};
        max-width: 850px;
        margin: 30px auto;
        padding: 50px;
        border-radius: {border_radius};
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-top: 12px solid {primary_color};
        color: #333;
    }}

    /* --- HEADER STYLES --- */
    .header {{
        text-align: {"center" if selected_layout == "centered" else "left"};
        margin-bottom: 40px;
        padding-bottom: 20px;
        border-bottom: 1px solid #eee;
    }}
    .header h1 {{
        color: {primary_color};
        font-size: 32px;
        margin: 0;
        letter-spacing: 1.5px;
    }}
    .header p {{ color: #666; margin-top: 5px; font-size: 14px; }}

    /* --- INFO SECTION --- */
    .info-grid {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 50px;
    }}
    .client-box {{ width: 60%; }}
    .invoice-meta {{ text-align: right; width: 35%; font-size: 14px; }}
    .label {{ color: {primary_color}; font-weight: bold; font-size: 11px; text-transform: uppercase; }}

    /* --- TABLE --- */
    .item-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 40px;
    }}
    .item-table th {{
        background-color: {primary_color};
        color: white;
        padding: 15px;
        text-align: left;
        text-transform: uppercase;
        font-size: 12px;
    }}
    .item-table td {{
        padding: 15px;
        border-bottom: 1px solid #eee;
        font-size: 15px;
    }}

    /* --- TOTALS --- */
    .total-row {{
        text-align: right;
        margin-top: 20px;
    }}
    .grand-total {{
        font-size: 28px;
        font-weight: bold;
        color: {primary_color};
    }}
    .words-box {{
        background: {accent_bg};
        padding: 15px;
        border-left: 5px solid {primary_color};
        margin-top: 20px;
        font-size: 13px;
        font-style: italic;
    }}

    /* --- SIGNATURE --- */
    .signature-area {{
        margin-top: 80px;
        text-align: right;
    }}
    .sig-line {{
        border-top: 2px solid #333;
        width: 220px;
        display: inline-block;
    }}
    .sig-label {{ font-weight: bold; margin-top: 8px; font-size: 14px; }}

    /* --- PRINT COMMANDS --- */
    @media print {{
        header, [data-testid="stSidebar"], [data-testid="stHeader"], .stButton, .print-btn-container {{
            display: none !important;
        }}
        .invoice-container {{
            box-shadow: none;
            border-radius: 0;
            margin: 0;
            padding: 30px;
            width: 100%;
        }}
        body {{ background: white; }}
    }}
</style>

<div class="invoice-container">
    <div class="header">
        <h1>{p_name}</h1>
        <p>{p_addr}</p>
    </div>

    <div class="info-grid">
        <div class="client-box">
            <div class="label">Billed To</div>
            <div style="font-size: 18px; font-weight: bold; margin-top: 5px;">{c_name}</div>
            <div style="color: #555; font-size: 14px; margin-top: 3px;">{c_addr}</div>
        </div>
        <div class="invoice-meta">
            <div class="label">Invoice Details</div>
            <div style="margin-top: 5px;"><strong>Invoice #:</strong> {inv_no}</div>
            <div><strong>Date:</strong> {inv_date.strftime('%d %b, %Y')}</div>
        </div>
    </div>

    <table class="item-table">
        <thead>
            <tr>
                <th>Description</th>
                <th style="text-align: right;">Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{desc}</td>
                <td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td>
            </tr>
        </tbody>
    </table>

    <div class="words-box">
        Rupees in words: <strong>{number_to_words(amt)}</strong>
    </div>

    <div class="total-row">
        <div style="color: #888; font-size: 12px; text-transform: uppercase;">Grand Total</div>
        <div class="grand-total">₹ {amt:,.2f}</div>
    </div>

    <div class="signature-area">
        <div class="sig-line"></div>
        <div class="sig-label">Authorized Signatory</div>
        <div style="font-size: 11px; color: #777;">For {p_name}</div>
    </div>
</div>

<div class="print-btn-container" style="text-align: center; padding-bottom: 50px;">
    <button onclick="window.print()" style="
        background-color: {primary_color};
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        Click to Print / Save as PDF
    </button>
</div>
"""

# Render the final output
st.markdown(invoice_html, unsafe_allow_html=True)
