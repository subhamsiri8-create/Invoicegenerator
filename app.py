import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Invoice Generator", layout="wide")

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
        if n >= 100:
            res += ones[int(n // 100)] + " Hundred "
            n %= 100
        if n >= 1000:
            res += convert_less_than_thousand(n // 1000) + " Thousand "
            n %= 1000
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
st.sidebar.title("Invoice Maker")
p_name = st.sidebar.text_input("Your Company", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- STYLE SEED ---
name_hash = hashlib.md5(p_name.encode()).hexdigest()
seed = int(name_hash, 16)
primary_color = "hsl({}, 70%, 30%)".format(seed % 360)

# --- THE HTML TEMPLATE ---
# We use the {{ }} trick for CSS inside the string
html_content = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #f4f4f4; margin: 0; padding: 20px; font-family: 'Poppins', sans-serif; }}
        .invoice-box {{
            max-width: 800px;
            margin: auto;
            padding: 40px;
            background: #fff;
            border-top: 10px solid {color};
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            color: #333;
        }}
        .header {{ text-align: center; border-bottom: 1px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: {color}; margin: 0; font-size: 28px; }}
        .info {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .item-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        .item-table th {{ background: {color}; color: white; padding: 12px; text-align: left; }}
        .item-table td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .total {{ text-align: right; font-size: 24px; font-weight: bold; color: {color}; }}
        .words {{ background: #f9f9f9; padding: 10px; border-left: 4px solid {color}; font-size: 12px; margin-top: 20px; }}
        .footer {{ margin-top: 60px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-line {{ border-top: 2px solid #333; width: 200px; margin-top: 50px; }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .invoice-box {{ box-shadow: none; border: 1px solid #eee; }}
            .btn-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-box">
        <div class="header">
            <h1>{p_name}</h1>
            <p>{p_addr}</p>
        </div>
        <div class="info">
            <div>
                <strong>Billed To:</strong><br>{c_name}<br>{c_addr}
            </div>
            <div style="text-align: right;">
                <strong>Invoice #:</strong> {inv_no}<br><strong>Date:</strong> {date}
            </div>
        </div>
        <table class="item-table">
            <thead><tr><th>Description</th><th style="text-align: right;">Amount</th></tr></thead>
            <tbody><tr><td>{desc}</td><td style="text-align: right;">₹ {amt:,.2f}</td></tr></tbody>
        </table>
        <div class="words">Rupees in words: {words}</div>
        <div class="footer">
            <div style="font-size: 11px; color: #999;">Generated via Digital Marketing Mechanics</div>
            <div style="text-align: right;">
                <div class="total">Total: ₹ {amt:,.2f}</div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
            </div>
        </div>
    </div>
    <div style="text-align: center; margin-top: 20px;" class="btn-print">
        <button onclick="window.print()" style="padding: 10px 30px; background: {color}; color: white; border: none; cursor: pointer; border-radius: 5px;">Print / Save PDF</button>
    </div>
</body>
</html>
"""

# --- RENDER WITH IFRAME ---
# This forces the browser to treat it as HTML, not text.
final_html = html_content.format(
    color=primary_color,
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

components.html(final_html, height=1100, scrolling=True)
