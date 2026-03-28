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
st.sidebar.title("Invoice Settings")
p_name = st.sidebar.text_input("Your Company", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- DETERMINISTIC DESIGN ENGINE (50,000+ Variations) ---
# This creates a unique ID based on the company name
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)

# 1. Colors (360 degrees of the HSL wheel)
hue = (seed % 360)
primary = f"hsl({hue}, 75%, 25%)"
secondary = f"hsl({hue}, 40%, 97%)"

# 2. Layouts (Different structural styles)
layouts = ["modern-left", "classic-center", "bold-sidebar", "minimal"]
selected_layout = layouts[(seed // 7) % len(layouts)]

# 3. Fonts (Professional sets)
fonts = ["'Poppins', sans-serif", "'Montserrat', sans-serif", "'Playfair Display', serif", "'Raleway', sans-serif"]
selected_font = fonts[(seed // 13) % len(fonts)]

# --- THE HTML & CSS ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=Raleway:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{ size: auto; margin: 0mm; }}
        body {{ background: #f0f2f6; margin: 0; padding: 40px; font-family: {font}; }}
        .invoice-box {{
            max-width: 800px; margin: auto; background: white; padding: 60px;
            border-top: 20px solid {color}; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .header {{ 
            text-align: {align}; 
            border-bottom: 2px solid #eee; 
            padding-bottom: 25px; 
            margin-bottom: 40px; 
        }}
        .header h1 {{ color: {color}; margin: 0; font-size: 32px; text-transform: uppercase; }}
        .info-grid {{ display: flex; justify-content: space-between; margin-bottom: 50px; }}
        .label {{ color: {color}; font-weight: bold; font-size: 11px; text-transform: uppercase; }}
        .item-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .item-table th {{ background: {color}; color: white; padding: 15px; text-align: left; }}
        .item-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .total-area {{ text-align: right; margin-top: 30px; }}
        .grand-total {{ font-size: 32px; font-weight: bold; color: {color}; }}
        .words-box {{ background: {bg}; padding: 15px; border-left: 5px solid {color}; margin-top: 30px; font-style: italic; font-size: 13px; }}
        .footer {{ margin-top: 80px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-line {{ border-top: 2px solid #333; width: 220px; display: inline-block; margin-top: 60px; }}
        @media print {{
            body {{ background: white; padding: 15mm; }}
            .invoice-box {{ box-shadow: none; border: 1px solid #eee; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-box">
        <div class="header">
            <h1>{p_name}</h1>
            <div style="color: #666;">{p_addr}</div>
        </div>
        <div class="info-grid">
            <div>
                <div class="label">Customer</div>
                <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
                <div>{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Details</div>
                <strong># {inv_no}</strong><br>{date}
            </div>
        </div>
        <table class="item-table">
            <thead><tr><th>Description</th><th style="text-align: right;">Amount</th></tr></thead>
            <tbody><tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr></tbody>
        </table>
        <div class="words-box">Rupees in words: <strong>{words}</strong></div>
        <div class="footer">
            <div style="font-size: 11px; color: #888;">Unique Template Generated for {p_name}</div>
            <div style="text-align: right;">
                <div class="total-area">
                    <div class="label">Amount Due</div>
                    <div class="grand-total">₹ {amt:,.2f}</div>
                </div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #999;">For {p_name}</div>
            </div>
        </div>
    </div>
    <div style="text-align: center; margin-top: 30px;" class="no-print">
        <button onclick="window.print()" style="background: {color}; color: white; padding: 15px 40px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">Print Invoice</button>
    </div>
</body>
</html>
"""

# --- INJECT DATA AND RENDER ---
final_render = html_template.format(
    color=primary, bg=secondary, font=selected_font,
    align="center" if selected_layout == "classic-center" else "left",
    p_name=p_name, p_addr=p_addr, c_name=c_name, c_addr=c_addr,
    inv_no=inv_no, date=inv_date.strftime("%d %b, %Y"),
    desc=desc, amt=amt, words=number_to_words(amt)
)

components.html(final_render, height=1200, scrolling=True)
