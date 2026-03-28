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

# --- DYNAMIC STYLE GENERATOR ---
# Hash ensures "Company A" always gets the same unique template
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)
hue = (seed % 360)
primary_color = "hsl({}, 70%, 25%)".format(hue)
bg_color = "hsl({}, 30%, 98%)".format(hue)

# --- THE HTML & CSS ---
# We use doubled braces {{ }} for CSS to avoid Python conflict
html_code = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ 
            background-color: #f0f2f6; 
            margin: 0; 
            padding: 40px; 
            font-family: 'Poppins', sans-serif; 
        }}
        .invoice-card {{
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 60px;
            border-top: 20px solid {color};
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            position: relative;
        }}
        .header {{ text-align: center; border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 40px; }}
        .header h1 {{ color: {color}; margin: 0; font-size: 30px; letter-spacing: 2px; }}
        
        .info-section {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .label {{ color: {color}; font-weight: bold; font-size: 11px; text-transform: uppercase; }}
        
        .main-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .main-table th {{ background: {color}; color: white; padding: 15px; text-align: left; }}
        .main-table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        
        .total-wrapper {{ text-align: right; margin-top: 30px; }}
        .grand-total {{ font-size: 32px; font-weight: bold; color: {color}; }}
        
        .words-section {{ background: {bg}; padding: 15px; border-left: 5px solid {color}; margin-top: 30px; font-style: italic; font-size: 13px; }}
        
        .signature-footer {{ margin-top: 80px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-box {{ text-align: right; }}
        .sig-line {{ border-top: 2px solid #333; width: 220px; display: inline-block; margin-top: 60px; }}
        .sig-label {{ font-weight: bold; margin-top: 5px; }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .invoice-card {{ box-shadow: none; border: 1px solid #eee; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <h1>{p_name}</h1>
            <p style="color: #666;">{p_addr}</p>
        </div>

        <div class="info-section">
            <div>
                <div class="label">Customer</div>
                <div style="font-size: 18px; font-weight: bold;">{c_name}</div>
                <div>{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Info</div>
                <strong># {inv_no}</strong><br>
                {date}
            </div>
        </div>

        <table class="main-table">
            <thead>
                <tr><th>Description</th><th style="text-align: right;">Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
            </tbody>
        </table>

        <div class="words-section">Rupees in words: <strong>{words}</strong></div>

        <div class="signature-footer">
            <div style="font-size: 12px; color: #888;">Thank you for choosing {p_name}!</div>
            <div class="sig-box">
                <div class="total-wrapper">
                    <div class="label">Amount Due</div>
                    <div class="grand-total">₹ {amt:,.2f}</div>
                </div>
                <div class="sig-line"></div>
                <div class="sig-label">Authorized Signatory</div>
                <div style="font-size: 11px; color: #999;">For {p_name}</div>
            </div>
        </div>
    </div>

    <div style="text-align: center; margin-top: 30px;" class="no-print">
        <button onclick="window.print()" style="
            background: {color}; color: white; padding: 15px 40px; 
            border: none; border-radius: 8px; font-weight: bold; cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            🖨️ Print Invoice / Save as PDF
        </button>
    </div>
</body>
</html>
"""

# --- INJECT AND RENDER ---
final_output = html_code.format(
    color=primary_color,
    bg=bg_color,
    p_name=p_name,
    p_addr=p_addr,
    c_name=c_name,
    c_addr=c_addr,
    inv_no=inv_no,
    date=inv_date.strftime("%d %b, %Y"),
    desc=desc,
    amt=amt,
    words=number_to_words(amt)
)

# Height set to 1200 to accommodate the signature area
components.html(final_output, height=1200, scrolling=True)
