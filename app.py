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
st.sidebar.title("Invoice Designer")
# The template changes based on this input
p_name = st.sidebar.text_input("Company Name (Triggers Template Change)", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Digital Marketing Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- DETERMINISTIC DESIGN ENGINE ---
# This ensures "Entry A" always looks like "Template A"
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)

# 1. Dynamic Colors (360 Hues)
hue = (seed % 360)
primary_color = f"hsl({hue}, 70%, 25%)"
accent_bg = f"hsl({hue}, 40%, 98%)"

# 2. Professional Font Pairings
fonts = [
    "'Poppins', sans-serif", 
    "'Montserrat', sans-serif", 
    "'Playfair Display', serif", 
    "'Raleway', sans-serif",
    "'Merriweather', serif"
]
selected_font = fonts[seed % len(fonts)]

# 3. Structural Layout Styles
layouts = ["modern-left", "classic-center", "bold-border", "minimal-clean"]
selected_layout = layouts[(seed // 10) % len(layouts)]
alignment = "center" if selected_layout == "classic-center" else "left"
border_val = "15px" if selected_layout == "bold-border" else "0px"

# --- HTML TEMPLATE ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=Raleway:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{ size: auto; margin: 0mm; }}
        body {{ 
            background: #f4f7f9; 
            margin: 0; 
            padding: 40px; 
            font-family: {font}; 
        }}
        .invoice-card {{
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 60px;
            border-top: 15px solid {color};
            border-left: {border} solid {color};
            box-shadow: 0 20px 50px rgba(0,0,0,0.1);
            color: #333;
        }}
        .header {{ 
            text-align: {align}; 
            border-bottom: 1px solid #eee; 
            padding-bottom: 30px; 
            margin-bottom: 40px; 
        }}
        .header h1 {{ color: {color}; margin: 0; font-size: 34px; text-transform: uppercase; letter-spacing: 2px; }}
        
        .grid {{ display: flex; justify-content: space-between; margin-bottom: 50px; }}
        .section-label {{ color: {color}; font-weight: bold; font-size: 11px; text-transform: uppercase; margin-bottom: 8px; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-bottom: 40px; }}
        .table th {{ background: {color}; color: white; padding: 15px; text-align: left; text-transform: uppercase; font-size: 13px; }}
        .table td {{ padding: 18px; border-bottom: 1px solid #eee; font-size: 15px; }}
        
        .total-box {{ text-align: right; }}
        .grand-total {{ font-size: 32px; font-weight: bold; color: {color}; }}
        
        .words-container {{ 
            background: {bg}; 
            padding: 20px; 
            border-left: 6px solid {color}; 
            margin: 30px 0; 
            font-style: italic; 
            font-size: 13px; 
        }}

        .footer {{ 
            margin-top: 80px; 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-end; 
        }}
        .sig-box {{ text-align: right; }}
        .sig-line {{ border-top: 2px solid #333; width: 230px; display: inline-block; margin-top: 60px; }}

        @media print {{
            body {{ background: white; padding: 10mm; }}
            .invoice-card {{ box-shadow: none; border: 1px solid #eee; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <h1>{p_name}</h1>
            <div style="color: #666; font-size: 14px;">{p_addr}</div>
        </div>

        <div class="grid">
            <div>
                <div class="section-label">Billed To</div>
                <div style="font-size: 20px; font-weight: bold;">{c_name}</div>
                <div style="color: #555;">{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="section-label">Invoice Summary</div>
                <strong>Invoice ID:</strong> {inv_no}<br>
                <strong>Date:</strong> {date}
            </div>
        </div>

        <table class="table">
            <thead>
                <tr><th>Description of Service</th><th style="text-align: right;">Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
            </tbody>
        </table>

        <div class="words-container">
            <strong>Amount in Words:</strong><br>{words}
        </div>

        <div class="footer">
            <div style="font-size: 11px; color: #999;">
                System Generated Invoice | Style ID: {seed}
            </div>
            <div class="sig-box">
                <div class="total-box">
                    <div class="section-label">Total Outstanding</div>
                    <div class="grand-total">₹ {amt:,.2f}</div>
                </div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #777;">For {p_name}</div>
            </div>
        </div>
    </div>

    <div class="no-print" style="text-align: center; margin-top: 40px;">
        <button onclick="window.print()" style="
            background: {color}; 
            color: white; 
            padding: 15px 50px; 
            border: none; 
            border-radius: 8px; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        ">
            🖨️ Download Professional PDF
        </button>
    </div>
</body>
</html>
"""

# --- RENDER ---
final_html = html_template.format(
    color=primary_color,
    bg=accent_bg,
    font=selected_font,
    align=alignment,
    border=border_val,
    p_name=p_name,
    p_addr=p_addr,
    c_name=c_name,
    c_addr=c_addr,
    inv_no=inv_no,
    date=inv_date.strftime("%d %B, %Y"),
    desc=desc,
    amt=amt,
    words=number_to_words(amt),
    seed=name_hash[:8]
)

components.html(final_html, height=1200, scrolling=True)
