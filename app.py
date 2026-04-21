import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Clean Professional Invoice", layout="wide")

# --- SESSION STATE FOR LINE ITEMS ---
if "line_items" not in st.session_state:
    st.session_state.line_items = [{"desc": "Service Details", "amt": 0.0}]

def add_item():
    st.session_state.line_items.append({"desc": "", "amt": 0.0})

def remove_item(idx):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(idx)

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

st.sidebar.markdown("---")
st.sidebar.header("📄 Paper Size")
sheet_size = st.sidebar.radio(
    " ", ["A4", "A5", "Letter"], index=0,
    label_visibility="collapsed", horizontal=True,
    format_func=lambda x: {"A4": " A4 ", "A5": " A5 ", "Letter": " Letter "}[x]
)
orientation = st.sidebar.radio("Orientation", ["Portrait", "Landscape"], index=0, horizontal=True)

st.sidebar.markdown("---")
st.sidebar.header("📝 Business Details")
p_name = st.sidebar.text_input("Company Name", "DIGITAL MARKETING MECHANICS").upper()
p_addr = st.sidebar.text_area("Address", "Eluru, Andhra Pradesh")

st.sidebar.header("👤 Client Details")
c_name = st.sidebar.text_input("Billed To", "VASAVI SILKS PRIVATE LIMITED")
c_addr = st.sidebar.text_area("Client Address", "Edaravari Street\nEluru-534002\n9246663443\naccounts@vasavisilks.com")

st.sidebar.markdown("---")
st.sidebar.header("📊 Invoice Data")
inv_no = st.sidebar.text_input("Invoice #", "INV-2026-001")
inv_date = st.sidebar.date_input("Date", datetime.now())

# --- DISCOUNT & TAX (optional) ---
col_disc, col_tax = st.sidebar.columns(2)
with col_disc:
    discount_type = st.selectbox("Discount", ["None", "Flat ₹", "%"], index=0)
    discount_val = st.number_input("Discount Value", min_value=0.0, value=0.0, step=0.01,
                                    disabled=(discount_type == "None"), key="disc_val")
with col_tax:
    tax_type = st.selectbox("Tax", ["None", "Flat ₹", "%"], index=0)
    tax_val = st.number_input("Tax Value", min_value=0.0, value=0.0, step=0.01,
                               disabled=(tax_type == "None"), key="tax_val")

st.sidebar.markdown("---")
st.sidebar.header("📦 Line Items")

# Render line items
for i, item in enumerate(st.session_state.line_items):
    cols = st.sidebar.columns([5, 1, 3, 1])
    with cols[0]:
        item["desc"] = st.text_input("Desc", value=item["desc"], key=f"desc_{i}", label_visibility="collapsed",
                                      placeholder="Description...")
    with cols[1]:
        st.markdown(f"<div style='text-align:center;padding-top:22px;font-size:10px;color:#888;'>#{i+1}</div>",
                     unsafe_allow_html=True)
    with cols[2]:
        item["amt"] = st.number_input("₹", value=item["amt"], min_value=0.0, step=0.01,
                                       key=f"amt_{i}", label_visibility="collapsed", format="%.2f")
    with cols[3]:
        st.markdown("<div style='padding-top:18px;'></div>", unsafe_allow_html=True)
        if st.button("✕", key=f"del_{i}", help="Remove item",
                     use_container_width=True,
                     disabled=(len(st.session_state.line_items) <= 1)):
            remove_item(i)
            st.rerun()

st.sidebar.button("➕ Add Line Item", on_click=add_item, use_container_width=True, type="secondary")

# --- CALCULATIONS ---
subtotal = sum(item["amt"] for item in st.session_state.line_items)

discount_amount = 0.0
if discount_type == "Flat ₹":
    discount_amount = discount_val
elif discount_type == "%":
    discount_amount = subtotal * (discount_val / 100)

tax_amount = 0.0
if tax_type == "Flat ₹":
    tax_amount = tax_val
elif tax_type == "%":
    tax_amount = (subtotal - discount_amount) * (tax_val / 100)

grand_total = subtotal - discount_amount + tax_amount

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Subtotal:** ₹ {subtotal:,.2f}")
if discount_amount > 0:
    st.sidebar.markdown(f"~~Discount~~: -₹ {discount_amount:,.2f}")
if tax_amount > 0:
    st.sidebar.markdown(f"**Tax:** +₹ {tax_amount:,.2f}")
st.sidebar.markdown(f"### Grand Total: ₹ {grand_total:,.2f}")

# --- SHEET DIMENSIONS ---
sheet_dims = {"A4": {"w": 210, "h": 297}, "A5": {"w": 148, "h": 210}, "Letter": {"w": 216, "h": 279}}
dim = sheet_dims[sheet_size]
if orientation == "Landscape":
    dim = {"w": dim["h"], "h": dim["w"]}
page_w_mm, page_h_mm = dim["w"], dim["h"]

scale = page_w_mm / 210.0
is_small = sheet_size == "A5"

if is_small:
    co_title_size = 18; inv_num_size = 12; billed_name_size = 13
    table_font_size = 10; table_head_size = 8; grand_total_size = 20
    amt_words_size = 9; addr_size = 9; label_size = 7
    padding_mm = 6; border_w = 3; summary_font = 10
else:
    co_title_size = int(30 * scale); inv_num_size = int(16 * scale)
    billed_name_size = int(18 * scale); table_font_size = int(14 * scale)
    table_head_size = int(10 * scale); grand_total_size = int(30 * scale)
    amt_words_size = int(11 * scale); addr_size = int(13 * scale)
    label_size = int(9 * scale); summary_font = int(12 * scale)
    padding_mm = int(10 * scale); border_w = int(6 * scale)

preview_scale = 1.0
if sheet_size == "A5" and orientation == "Portrait": preview_scale = 1.45
elif sheet_size == "A5" and orientation == "Landscape": preview_scale = 1.3
elif sheet_size == "Letter" and orientation == "Landscape": preview_scale = 0.95

# --- PROCEDURAL ENGINE ---
s = style_id
hues = [210, 160, 25, 340, 280, 200, 10, 120, 45, 190]
primary = f"hsl({hues[s % len(hues)]}, 75%, {25 + (s % 20)}%)"
bg_light = f"hsl({hues[s % len(hues)]}, 15%, 98%)"
font_options = ["'Poppins', sans-serif", "'Playfair Display', serif", "'Inter', sans-serif",
                "'Montserrat', sans-serif", "'JetBrains Mono', monospace", "'Roboto Condensed', sans-serif"]
selected_font = font_options[s % len(font_options)]
aligns = ["space-between", "center", "flex-start"]
h_align = aligns[s % 3]

# --- BUILD TABLE ROWS ---
table_rows_html = ""
for idx, item in enumerate(st.session_state.line_items):
    row_cls = "" if idx % 2 == 0 else ' style="background:#fafbfc;"'
    table_rows_html += f"""
        <tr{row_cls}>
            <td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:{table_font_size}px;">
                {item['desc'] if item['desc'] else '&nbsp;'}
            </td>
            <td style="text-align:right;padding:8px 10px;border-bottom:1px solid #eee;font-size:{table_font_size}px;font-weight:600;">
                ₹ {item['amt']:,.2f}
            </td>
        </tr>"""

# --- BUILD SUMMARY BLOCK ---
summary_html = ""
if discount_amount > 0 or tax_amount > 0:
    summary_html = f"""
    <div style="display:flex;justify-content:flex-end;margin:12px 0 0 0;">
        <div style="width:220px;">
            <div style="display:flex;justify-content:space-between;font-size:{summary_font}px;padding:3px 0;">
                <span style="color:#666;">Subtotal</span>
                <span style="font-weight:600;">₹ {subtotal:,.2f}</span>
            </div>"""
    if discount_amount > 0:
        summary_html += f"""
            <div style="display:flex;justify-content:space-between;font-size:{summary_font}px;padding:3px 0;color:#e74c3c;">
                <span>Discount ({discount_type})</span>
                <span>- ₹ {discount_amount:,.2f}</span>
            </div>"""
    if tax_amount > 0:
        summary_html += f"""
            <div style="display:flex;justify-content:space-between;font-size:{summary_font}px;padding:3px 0;color:#27ae60;">
                <span>Tax ({tax_type})</span>
                <span>+ ₹ {tax_amount:,.2f}</span>
            </div>"""
    summary_html += """
        </div>
    </div>"""

# --- HTML TEMPLATE ---
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;600;700&family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@400;700&family=JetBrains+Mono&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        @page {{ size: {page_w_mm}mm {page_h_mm}mm; margin: 0; }}
        body {{
            background: #e8eaed; margin: 0; padding: 20px;
            font-family: {selected_font};
            display: flex; flex-direction: column; align-items: center;
            min-height: 100vh;
        }}
        .invoice-wrapper {{ transform: scale({preview_scale}); transform-origin: top center; }}
        .invoice-card {{
            background: white; width: {page_w_mm}mm; min-height: {page_h_mm}mm;
            padding: {padding_mm}mm; display: flex; flex-direction: column;
            border-top: {border_w}px solid {primary};
            box-shadow: 0 4px 24px rgba(0,0,0,0.10); position: relative;
        }}
        .invoice-card::after {{
            content: "{sheet_size} {orientation}"; position: absolute;
            bottom: 5mm; left: 5mm; font-size: 7px; color: rgba(0,0,0,0.05);
            font-weight: 700; letter-spacing: 2px; text-transform: uppercase; pointer-events: none;
        }}
        .header {{
            display: flex; justify-content: {h_align}; align-items: center;
            margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee;
            {f"text-align:center;flex-direction:column;" if h_align == 'center' else ""}
        }}
        .co-title {{ color: {primary}; font-size: {co_title_size}px; font-weight: 700; text-transform: uppercase; margin: 0; line-height: 1.1; }}
        .label {{ color: {primary}; font-size: {label_size}px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 2px; }}
        .table {{ width: 100%; border-collapse: collapse; margin-top: 4px; }}
        .table th {{
            background: {primary}; color: white; text-align: left;
            padding: 8px 10px; font-size: {table_head_size}px;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .table th:last-child {{ text-align: right; }}
        .table td {{ padding: 8px 10px; border-bottom: 1px solid #eee; font-size: {table_font_size}px; }}
        .table td:last-child {{ text-align: right; }}
        .table tr:last-child td {{ border-bottom: 2px solid {primary}; }}

        .amt-words {{
            background: {bg_light}; padding: 8px 10px;
            border-left: 4px solid {primary}; font-style: italic;
            font-size: {amt_words_size}px; margin: 14px 0;
        }}
        .footer-aligned {{ display: flex; justify-content: flex-end; margin-top: 8px; }}
        .total-container {{ text-align: right; width: 220px; }}
        .grand-total {{ font-size: {grand_total_size}px; font-weight: 700; color: {primary}; margin: 0; line-height: 1.1; }}
        .sig-line {{ border-top: 2px solid #000; width: 100%; margin-top: 28px; }}
        .size-badge {{
            position: absolute; top: {padding_mm}mm; right: {padding_mm}mm;
            background: {primary}; color: white; font-size: 7px;
            padding: 2px 6px; border-radius: 3px; font-weight: 700;
            letter-spacing: 1px; text-transform: uppercase;
        }}
        .items-count {{
            display: inline-block; background: {bg_light}; color: {primary};
            font-size: {table_head_size}px; padding: 2px 8px; border-radius: 10px;
            font-weight: 600; margin-left: 8px;
        }}
        @media print {{
            body {{ background: none; padding: 0; display: block; }}
            .invoice-wrapper {{ transform: none !important; }}
            .invoice-card {{ box-shadow: none; width: {page_w_mm}mm; min-height: {page_h_mm}mm; border: none; border-top: {border_w}px solid {primary}; }}
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
                    <div style="color:#555;font-size:{addr_size}px;margin-top:4px;">##PADDR##</div>
                </div>
                <div style="text-align:right;{'margin-top:12px;' if h_align == 'center' else ''}">
                    <strong style="font-size:{inv_num_size}px;color:{primary};"># ##INVNO##</strong><br>
                    <span style="font-size:{int(12*scale)}px;font-weight:600;color:#444;">##DATE##</span>
                </div>
            </div>

            <div style="margin-bottom:16px;">
                <div class="label">Billed To</div>
                <div style="font-size:{billed_name_size}px;font-weight:700;margin-top:3px;">##CNAME##</div>
                <div style="white-space:pre-wrap;color:#444;line-height:1.4;font-size:{addr_size}px;">##CADDR##</div>
            </div>

            <div style="display:flex;align-items:center;margin-bottom:6px;">
                <div class="label" style="margin-bottom:0;">Item Details</div>
                <span class="items-count">##COUNT## items</span>
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th style="width:65%;">Description</th>
                        <th style="width:35%;">Amount (₹)</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>

            {summary_html}

            <div class="amt-words">
                <strong>Amount in Words:</strong> ##WORDS##
            </div>

            <div class="footer-aligned">
                <div class="total-container">
                    <div class="label">Grand Total</div>
                    <div class="grand-total">₹ ##GRAND##</div>
                    <div class="sig-line"></div>
                    <div style="font-weight:700;font-size:{int(11*scale)}px;margin-top:5px;">Authorized Signatory</div>
                </div>
            </div>
        </div>
    </div>

    <div class="no-print" style="position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:999;">
        <button onclick="window.print()" style="
            background:{primary};color:white;padding:14px 50px;border:none;
            border-radius:6px;font-weight:700;cursor:pointer;letter-spacing:1px;
            font-size:13px;box-shadow:0 4px 15px rgba(0,0,0,0.2);
            font-family:{selected_font};
        ">🖨️ PRINT INVOICE ({sheet_size} {orientation})</button>
    </div>
</body>
</html>
"""

# --- FINAL REPLACEMENT ---
final_html = html_template.replace("##PNAME##", p_name) \
                          .replace("##PADDR##", p_addr) \
                          .replace("##CNAME##", c_name) \
                          .replace("##CADDR##", c_addr) \
                          .replace("##INVNO##", inv_no) \
                          .replace("##DATE##", inv_date.strftime("%d %b, %Y")) \
                          .replace("##COUNT##", str(len(st.session_state.line_items))) \
                          .replace("##WORDS##", number_to_words(grand_total)) \
                          .replace("##GRAND##", f"{grand_total:,.2f}")

base_heights = {"A4": 1100, "A5": 800, "Letter": 1050}
display_height = int(base_heights[sheet_size] * preview_scale) + 140
# Add extra height for many line items
display_height += max(0, (len(st.session_state.line_items) - 3) * 40)

components.html(final_html, height=display_height, scrolling=True)
