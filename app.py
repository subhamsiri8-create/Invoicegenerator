import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clean Professional Invoice", layout="wide")

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
st.sidebar.header("🎨 Style Selector")
style_id = st.sidebar.number_input("Enter Template ID (1-1000)", min_value=1, max_value=1000, value=1)

# --- SHEET SIZE SELECTOR (inline CSS + radio buttons) ---
st.sidebar.markdown("---")
st.sidebar.header("📄 Paper Size")

# Visual sheet selector using custom HTML
sheet_html = """
<style>
    .sheet-option {
        display: inline-block; cursor: pointer; text-align: center;
        border: 2px solid #ddd; border-radius: 8px; padding: 10px 14px;
        margin-right: 6px; transition: all 0.2s; vertical-align: top;
        background: white; user-select: none;
    }
    .sheet-option:hover { border-color: #999; }
    .sheet-option.selected { border-color: #2563eb; background: #eff6ff; }
    .sheet-icon {
        border: 1.5px solid #888; background: #fafafa; margin: 0 auto 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 9px; color: #888; font-weight: bold;
    }
    .a4-icon { width: 38px; height: 54px; }
    .a5-icon { width: 30px; height: 42px; }
    .letter-icon { width: 40px; height: 52px; }
    .sheet-label { font-size: 11px; font-weight: 600; color: #333; }
    .sheet-dim { font-size: 9px; color: #999; }
</style>
"""

st.sidebar.markdown(sheet_html, unsafe_allow_html=True)

sheet_size = st.sidebar.radio(
    " ",
    ["A4", "A5", "Letter"],
    index=0,
    label_visibility="collapsed",
    horizontal=True,
    format_func=lambda x: {
        "A4": " A4 ",
        "A5": " A5 ",
        "Letter": " Letter "
    }[x]
)

# Orientation
orientation = st.sidebar.radio(
    "Orientation",
    ["Portrait", "Landscape"],
    index=0,
    horizontal=True
)

st.sidebar.markdown("---")
st.sidebar.header("📝 Business Details")
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")

st.sidebar.header("👤 Client Details")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.header("📊 Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())
desc = st.sidebar.text_area("Description", "Service Details")
amt = st.sidebar.number_input("Amount (INR)", value=0.0)

# --- SHEET DIMENSIONS ---
sheet_dims = {
    "A4": {"w": 210, "h": 297},
    "A5": {"w": 148, "h": 210},
    "Letter": {"w": 216, "h": 279},
}
dim = sheet_dims[sheet_size]
if orientation == "Landscape":
    dim = {"w": dim["h"], "h": dim["w"]}

page_w_mm = dim["w"]
page_h_mm = dim["h"]

# Scale factor relative to A4 for font sizing
scale = page_w_mm / 210.0
is_small = sheet_size == "A5"

# --- PROCEDURAL ENGINE ---
s = style_id
hues = [210, 160, 25, 340, 280, 200, 10, 120, 45, 190]
primary = f"hsl({hues[s % len(hues)]}, 75%, {25 + (s % 20)}%)"
bg_light = f"hsl({hues[s % len(hues)]}, 15%, 98%)"

font_options = [
    "'Poppins', sans-serif", "'Playfair Display', serif", "'Inter', sans-serif",
    "'Montserrat', sans-serif", "'JetBrains Mono', monospace", "'Roboto Condensed', sans-serif"
]
selected_font = font_options[s % len(font_options)]

aligns = ["space-between", "center", "flex-start"]
h_align = aligns[s % 3]

# --- ADAPTIVE FONT SIZES ---
if is_small:
    co_title_size = 20
    inv_num_size = 14
    billed_name_size = 14
    table_font_size = 11
    table_head_size = 9
    grand_total_size = 22
    amt_words_size = 10
    addr_size = 10
    label_size = 8
    padding_mm = 7
    border_w = 4
else:
    co_title_size = int(32 * scale)
    inv_num_size = int(18 * scale)
    billed_name_size = int(20 * scale)
    table_font_size = int(15 * scale)
    table_head_size = int(11 * scale)
    grand_total_size = int(34 * scale)
    amt_words_size = int(12 * scale)
    addr_size = int(14 * scale)
    label_size = int(10 * scale)
    padding_mm = int(10 * scale)
    border_w = int(6 * scale)

# Preview scaling for display (A5 needs to be larger on screen so it's readable)
preview_scale = 1.0
if sheet_size == "A5" and orientation == "Portrait":
    preview_scale = 1.45
elif sheet_size == "A5" and orientation == "Landscape":
    preview_scale = 1.35
elif sheet_size == "Letter" and orientation == "Landscape":
    preview_scale = 0.95

# Print page dimensions in CSS mm
print_w = page_w_mm
print_h = page_h_mm

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&family=Montserrat:wght@400;700&family=Playfair+Display:wght@400;700&family=JetBrains+Mono&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        @page {{
            size: {page_w_mm}mm {page_h_mm}mm;
            margin: 0;
        }}
        body {{
            background: #e8eaed; margin: 0; padding: 20px;
            font-family: {selected_font};
            display: flex; justify-content: center; align-items: flex-start;
            min-height: 100vh;
        }}

        .invoice-wrapper {{
            transform: scale({preview_scale});
            transform-origin: top center;
        }}

        .invoice-card {{
            background: white;
            width: {page_w_mm}mm;
            min-height: {page_h_mm}mm;
            padding: {padding_mm}mm;
            display: flex; flex-direction: column;
            border-top: {border_w}px solid {primary};
            box-shadow: 0 4px 24px rgba(0,0,0,0.10);
            position: relative;
            overflow: hidden;
        }}

        /* Subtle diagonal watermark */
        .invoice-card::after {{
            content: "{sheet_size} {orientation}";
            position: absolute; bottom: 6mm; left: 6mm;
            font-size: 8px; color: rgba(0,0,0,0.06); font-weight: 700;
            letter-spacing: 2px; text-transform: uppercase;
            pointer-events: none;
        }}

        .header {{
            display: flex; justify-content: {h_align};
            align-items: center; margin-bottom: 18px; padding-bottom: 12px;
            border-bottom: 1px solid #eee;
            {f"text-align: center; flex-direction: column;" if h_align == 'center' else ""}
        }}

        .co-title {{ color: {primary}; font-size: {co_title_size}px; font-weight: bold; text-transform: uppercase; margin: 0; line-height: 1.1; }}
        .label {{ color: {primary}; font-size: {label_size}px; font-weight: bold; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 2px; }}

        .table {{ width: 100%; border-collapse: collapse; }}
        .table th {{ background: {bg_light}; color: {primary}; text-align: left; padding: 8px 10px; border-bottom: 2px solid {primary}; font-size: {table_head_size}px; }}
        .table td {{ padding: 10px; border-bottom: 1px solid #eee; font-size: {table_font_size}px; }}

        .amt-words {{ background: {bg_light}; padding: 10px; border-left: 4px solid {primary}; font-style: italic; font-size: {amt_words_size}px; margin: 15px 0; }}

        .footer-aligned {{ display: flex; justify-content: flex-end; margin-top: 8px; }}
        .total-container {{ text-align: right; width: 200px; }}
        .grand-total {{ font-size: {grand_total_size}px; font-weight: bold; color: {primary}; margin: 0; line-height: 1.1; }}
        .sig-line {{ border-top: 2px solid #000; width: 100%; margin-top: 30px; }}

        .size-badge {{
            position: absolute; top: {padding_mm}mm; right: {padding_mm}mm;
            background: {primary}; color: white; font-size: 7px;
            padding: 2px 6px; border-radius: 3px; font-weight: 700;
            letter-spacing: 1px; text-transform: uppercase;
        }}

        @media print {{
            body {{ background: none; padding: 0; display: block; }}
            .invoice-wrapper {{ transform: none !important; }}
            .invoice-card {{ box-shadow: none; width: {print_w}mm; min-height: {print_h}mm; border: none; border-top: {border_w}px solid {primary}; }}
            .size-badge {{ display: none; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="invoice-wrapper">
        <div class="invoice-card">
            <div class="size-badge">{sheet_size} · {orientation}</div>

            <div class="header">
                <div>
                    <div class="co-title">##PNAME##</div>
                    <div style="color: #555; font-size: {addr_size}px; margin-top: 4px;">##PADDR##</div>
                </div>
                <div style="text-align: right; { 'margin-top: 15px;' if h_align == 'center' else '' }">
                    <strong style="font-size: {inv_num_size}px; color: {primary};"># ##INVNO##</strong><br>
                    <span style="font-size: {int(13*scale)}px; font-weight: bold; color: #444;">##DATE##</span>
                </div>
            </div>

            <div style="margin-bottom: 18px;">
                <div class="label">Billed To</div>
                <div style="font-size: {billed_name_size}px; font-weight: bold; margin-top: 3px;">##CNAME##</div>
                <div style="white-space: pre-wrap; color: #444; line-height: 1.4; font-size: {addr_size}px;">##CADDR##</div>
            </div>

            <table class="table">
                <thead><tr><th>Description</th><th style="text-align: right;">Total Amount</th></tr></thead>
                <tbody><tr><td>##DESC##</td><td style="text-align: right; font-weight: bold;">₹ ##AMT##</td></tr></tbody>
            </table>

            <div class="amt-words">
                <strong>Amount in Words:</strong> ##WORDS##
            </div>

            <div class="footer-aligned">
                <div class="total-container">
                    <div class="label">Amount Payable</div>
                    <div class="grand-total">₹ ##AMT##</div>
                    <div class="sig-line"></div>
                    <div style="font-weight: bold; font-size: {int(12*scale)}px; margin-top: 5px;">Authorized Signatory</div>
                </div>
            </div>
        </div>
    </div>

    <div class="no-print" style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 999;">
        <button onclick="window.print()" style="
            background: {primary}; color: white; padding: 14px 50px; border: none;
            border-radius: 6px; font-weight: bold; cursor: pointer; letter-spacing: 1px;
            font-size: 13px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-family: {selected_font};
        ">
            🖨️ PRINT INVOICE ({sheet_size} {orientation})
        </button>
    </div>
</body>
</html>
"""

# Replacement
final_html = html_template.replace("##PNAME##", p_name) \
                          .replace("##PADDR##", p_addr) \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##DESC##", desc) \
                          .replace("##AMT##", f"{amt:,.2f}") \
                          .replace("##WORDS##", number_to_words(amt))

# Dynamic height based on sheet + orientation
base_heights = {"A4": 1100, "A5": 800, "Letter": 1050}
base_h = base_heights[sheet_size]
display_height = int(base_h * preview_scale) + 120

components.html(final_html, height=display_height, scrolling=True)
