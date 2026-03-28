import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

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
st.sidebar.title("Invoice Details")
p_name = st.sidebar.text_input("Your Company", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Your Address", "Eluru, Andhra Pradesh")
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS")
c_addr = st.sidebar.text_area("Client Address", "Mumbai, Maharashtra")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Social Media Management")
amt = st.sidebar.number_input("Amount (INR)", value=15000.0)

# --- THE SINGLE FIXED TEMPLATE ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* CRITICAL: Removes browser headers/footers */
        @page {{
            size: auto;
            margin: 0mm; 
        }}

        body {{ 
            background-color: #f7f7f7; 
            margin: 0; 
            padding: 40px; 
            font-family: 'Poppins', sans-serif; 
        }}

        .invoice-card {{
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 50px;
            border-top: 15px solid #4F7942; /* Fixed Green Theme */
            box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        }}

        .header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #4F7942; margin: 0; font-size: 30px; }}
        
        .grid {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
        .label {{ color: #4F7942; font-weight: bold; font-size: 12px; text-transform: uppercase; }}
        
        .table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .table th {{ background: #4F7942; color: white; padding: 12px; text-align: left; }}
        .table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        
        .total-box {{ text-align: right; margin-top: 30px; }}
        .total-amt {{ font-size: 28px; font-weight: bold; color: #4F7942; }}
        
        .words-box {{ background: #f0f4ef; padding: 12px; border-left: 5px solid #4F7942; margin-top: 20px; font-style: italic; font-size: 13px; }}

        .footer-sign {{ margin-top: 60px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-line {{ border-top: 2px solid #333; width: 220px; display: inline-block; margin-top: 50px; }}

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
            <p style="color: #666;">{p_addr}</p>
        </div>

        <div class="grid">
            <div>
                <div class="label">Customer</div>
                <div style="font-size: 17px; font-weight: bold;">{c_name}</div>
                <div style="color: #555;">{c_addr}</div>
            </div>
            <div style="text-align: right;">
                <div class="label">Invoice Details</div>
                <strong># {inv_no}</strong><br>
                {date}
            </div>
        </div>

        <table class="table">
            <thead>
                <tr><th>Description</th><th style="text-align: right;">Amount</th></tr>
            </thead>
            <tbody>
                <tr><td>{desc}</td><td style="text-align: right; font-weight: bold;">₹ {amt:,.2f}</td></tr>
            </tbody>
        </table>

        <div class="words-box">Rupees in words: <strong>{words}</strong></div>

        <div class="footer-sign">
            <div style="font-size: 11px; color: #888;">Thank you for your business!</div>
            <div style="text-align: right;">
                <div class="total-box">
                    <div class="label">Amount Due</div>
                    <div class="total-amt">₹ {amt:,.2f}</div>
                </div>
                <div class="sig-line"></div>
                <div style="font-weight: bold; margin-top: 5px;">Authorized Signatory</div>
                <div style="font-size: 11px; color: #777;">For {p_name}</div>
            </div>
        </div>
    </div>

    <div style="text-align: center; margin-top: 30px;" class="no-print">
        <button onclick="window.print()" style="
            background: #4F7942; color: white; padding: 12px 35px; 
            border: none; border-radius: 5px; font-weight: bold; cursor: pointer;
        ">
            🖨️ Print Invoice
        </button>
    </div>
</body>
</html>
"""

# --- RENDER ---
final_html = html_code.format(
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
