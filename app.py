import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Invoice Studio Pro", layout="wide")

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

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
inv_size = st.sidebar.selectbox("Page Size", ["Standard A4", "Compact Receipt"])

# Blank defaults for your agency
p_name = st.sidebar.text_input("Your Company Name", "").upper()
p_addr = st.sidebar.text_area("Your Address", "")

st.sidebar.subheader("Billing To")
# Persistent default for Vasavi Silks
c_name = st.sidebar.text_input("Client Name", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.subheader("Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Service", "Digital Marketing Services")
amt = st.sidebar.number_input("Total Amount (INR)", value=0.0, step=500.0)

# --- DESIGN ENGINE ---
seed_text = p_name if p_name else "GENERIC"
s = int(hashlib.md5(seed_text.encode()).hexdigest(), 16)

# Procedural Styles
hues = [210, 145, 0, 330, 260] # Blue, Green, Orange, Pink, Purple
color_base = hues[s % len(hues)]
prime = f"hsl({color_base}, 80%, 20%)"
font_f = ["'Poppins'", "'Inter'", "'Montserrat'"][s % 3]

# Dimensions
w_val = "210mm" if inv_size == "Standard A4" else "140mm"
h_val = "297mm" if inv_size == "Standard A4" else "200mm"

# --- HTML TEMPLATE (Brace-Free Placeholder Logic) ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        @page {{ size: A4; margin: 0mm; }}
        body {{ background: #eee; margin: 0; padding: 20px; font-family: {font_f}, sans-serif; }}
        .sheet {{
            background: white; width: {w_val}; min-height: {h_val};
            margin: auto; padding: 20mm; position: relative;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .top-stripe {{ height: 8px; background: {prime}; margin: -20mm -20mm 30px -20mm; }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding-bottom: 20px; }}
        .co-name {{ color: {prime}; font-size: 28px; font-weight: bold; text-transform: uppercase; }}
        .grid {{ display: flex; justify-content: space-between; margin: 40px 0; }}
        .tag {{ color: {prime}; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .table th {{ background: #f9f9f9; text-align: left; padding: 12px; color: {prime}; border-bottom: 2px solid {prime}; }}
        .table td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        .total-box {{ text-align: right; margin-top: 40px; }}
        .grand-total {{ font-size: 32px; font-weight: bold; color: {prime}; }}
        .words {{ font-style: italic; color: #666; font-size: 13px; margin-top: 20px; padding: 10px; border-left: 3px solid {prime}; background: #fafafa; }}
        .footer {{ position: absolute; bottom: 20mm; left: 20mm; right: 20mm; display: flex; justify-content: space-between; align-items: flex-end; }}
        .sig-line {{ border-top: 2px solid #000; width: 200px; margin-bottom: 5px; }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .sheet {{ box-shadow: none; margin: 0; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="sheet">
        <div class="top-stripe"></div>
        <div class="header">
            <div>
                <div class="co-name">##PNAME##</div>
                <div style="color: #666;">##PADDR##</div>
            </div>
            <div style="text-align: right;">
                <div class="tag">Invoice Details</div>
                <strong># ##INVNO##</strong><br>
                ##DATE##
            </div>
        </div>

        <div class="grid">
            <div>
                <div class="tag">Billed To</div>
                <div style="font-size: 18px; font-weight: bold;">##CNAME##</div>
                <div style="white-space: pre-wrap; color: #444;">##CADDR##</div>
            </div>
        </div>

        <table class="table">
            <thead><tr><th>Description</th><th style="text-align: right;">Amount</th></tr></thead>
            <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
        </table>

        <div class="words"><strong>Amount in Words:</strong><br>##WORDS##</div>

        <div class="footer">
            <div style="font-size: 10px; color: #aaa;">Authorized Digital Document</div>
            <div class="total-box">
                <div class="tag">Total Amount Due</div>
                <div class="grand-total">₹ ##AMT##</div>
                <div style="margin-top: 40px;">
                    <div class="sig-line"></div>
                    <div style="font-weight: bold;">Authorized Signatory</div>
                    <div style="font-size: 11px; color: #888;">For ##PNAME##</div>
                </div>
            </div>
        </div>
    </div>
    <div class="no-print" style="text-align: center; margin-top: 30px;">
        <button onclick="window.print()" style="background: {prime}; color: white; padding: 15px 60px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 16px;">PRINT INVOICE</button>
    </div>
</body>
</html>
"""

# Replace placeholders with actual data
final_html = html_template.replace("##PNAME##", p_name if p_name else "YOUR COMPANY NAME") \
                          .replace("##PADDR##", p_addr if p_addr else "Company Address Line") \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##DESC##", desc) \
                          .replace("##AMT##", f"{amt:,.2f}") \
                          .replace("##WORDS##", number_to_words(amt))

components.html(final_html, height=1300, scrolling=True)
