import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Professional Invoice Generator", layout="wide")

# --- SESSION STATE ---
if "line_items" not in st.session_state:
    st.session_state.line_items = [{"desc": "Service Details", "amt": 0.0}]

def add_item():
    st.session_state.line_items.append({"desc": "", "amt": 0.0})

def remove_item(idx):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(idx)

# --- INDIAN NUMBER SYSTEM ---
def number_to_words(num):
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    def clt(n):
        if n == 0: return ''
        if n < 20: return ones[int(n)]
        t, r = divmod(n, 10)
        return tens[int(t)] + (' ' + ones[int(r)] if r else '')
    def cv(n):
        if n == 0: return 'Zero'
        res = ""
        if n >= 10000000: res += clt(n // 10000000) + " Crore "; n %= 10000000
        if n >= 100000: res += clt(n // 100000) + " Lakh "; n %= 100000
        if n >= 1000: res += clt(n // 1000) + " Thousand "; n %= 1000
        if n >= 100: res += ones[int(n // 100)] + " Hundred "; n %= 100
        if n > 0: res += clt(n)
        return res.strip()
    ni = int(num); nd = int(round((num - ni) * 100))
    w = cv(ni) + " Rupees"
    if nd > 0: w += " and " + cv(nd) + " Paise"
    return w + " Only"

# --- FIXED LAYOUT STYLE ENGINE ---
def get_style(sid):
    i = sid - 1

    # 20 Font Pairs (heading, body)
    font_pairs = [
        ("'DM Sans', sans-serif", "'Space Grotesk', sans-serif"),
        ("'Playfair Display', serif", "'Source Sans 3', sans-serif"),
        ("'Outfit', sans-serif", "'Crimson Text', serif"),
        ("'Sora', sans-serif", "'Libre Baskerville', serif"),
        ("'Manrope', sans-serif", "'Cormorant Garamond', serif"),
        ("'Plus Jakarta Sans', sans-serif", "'Lora', serif"),
        ("'Bricolage Grotesk', sans-serif", "'EB Garamond', serif"),
        ("'Geist', sans-serif", "'Instrument Serif', serif"),
        ("'Onest', sans-serif", "'Fraunces', serif"),
        ("'Nunito Sans', sans-serif", "'Merriweather', serif"),
        ("'Figtree', sans-serif", "'Bitter', serif"),
        ("'General Sans', sans-serif", "'DM Serif Display', serif"),
        ("'Poppins', sans-serif", "'Space Mono', monospace"),
        ("'Montserrat', sans-serif", "'IBM Plex Mono', monospace"),
        ("'Inter', sans-serif", "'JetBrains Mono', monospace"),
        ("'Roboto Condensed', sans-serif", "'Roboto Slab', serif"),
        ("'Work Sans', sans-serif", "'Literata', serif"),
        ("'Lexend', sans-serif", "'Fira Code', monospace"),
        ("'Supreme', sans-serif", "'Newsreader', serif"),
        ("'Cabinet Grotesk', sans-serif", "'Garamond', serif"),
    ]
    hf, bf = font_pairs[i % 20]

    # 20 Color Palettes (header_bg, header_accent, primary, light_tint)
    palettes = [
        ("#1a1a2e", "#16213e", "#0f3460", "#e8eaf6"),   # Deep Navy
        ("#1b4332", "#2d6a4f", "#40916c", "#d8f3dc"),   # Forest
        ("#3c1642", "#5c1a6b", "#7b2d8e", "#f3e5f5"),   # Royal Purple
        ("#2b2d42", "#3d405b", "#5c6085", "#e8e8f0"),   # Slate
        ("#3d0c02", "#5c1a0a", "#8b2500", "#fce4d6"),   # Dark Red
        ("#0b3d2e", "#145a42", "#1e8564", "#d0f0e0"),   # Emerald
        ("#1a1a1a", "#333333", "#555555", "#f0f0f0"),   # Pure Black
        ("#2c1810", "#4a2c20", "#6b3a2a", "#f5e6dc"),   # Warm Brown
        ("#0d1b2a", "#1b2d45", "#2a4365", "#d6e4f0"),   # Midnight Blue
        ("#2d1b36", "#452a54", "#5e3a72", "#ede0f5"),   # Dark Violet
        ("#1a3300", "#2d5500", "#408000", "#e5f5d0"),   # Military Green
        ("#331a00", "#553300", "#775500", "#f5ecd0"),   # Dark Gold
        ("#1a0022", "#330044", "#550066", "#f0e0f5"),   # Deep Magenta
        ("#002233", "#003355", "#004477", "#d0e8f5"),   # Steel Blue
        ("#220000", "#440000", "#660000", "#f5d0d0"),   # Dark Crimson
        ("#1a2f1a", "#2d4a2d", "#406640", "#d5ecd5"),   # Pine Green
        ("#2a1a00", "#443000", "#5e4600", "#f0e5c0"),   # Dark Amber
        ("#001a2c", "#002d4a", "#004066", "#c8e0f0"),   # Ocean Blue
        ("#2c0020", "#4a0035", "#66004a", "#f0d0e5"),   # Wine
        ("#1c1c1c", "#363636", "#505050", "#ebebeb"),   # Charcoal
    ]
    hbg, hac, pri, lt = palettes[i % 20]

    # 10 Header accent styles (thin line below, gradient fade, double line, etc.)
    header_accents = [
        "none", "thin-line", "gradient-fade", "double-line",
        "dotted-line", "thick-bottom", "shadow-glow", "inner-border",
        "diagonal-cut", "subtle-gradient"
    ]
    hacc = header_accents[i % 10]

    # 8 Table border styles
    table_borders = [
        "hairline", "thin", "medium", "dotted",
        "dashed", "double-bottom", "thick-bottom", "color-accent"
    ]
    tbrd = table_borders[i % 8]

    # 6 Total highlight styles
    total_highlights = [
        "bold-text", "bg-box", "underline-accent", "side-bar",
        "top-bottom-lines", "circle-bg"
    ]
    tot = total_highlights[i % 6]

    # 6 Signature styles
    sig_styles = [
        "simple-line", "double-line", "dotted-box",
        "bracket", "stamp-circle", "minimal-text"
    ]
    sig = sig_styles[i % 6]

    # Typography variations
    title_weights = ["600", "700", "800", "900"]
    title_spacings = ["0px", "1px", "2px", "3px"]
    tw = title_weights[i % 4]
    tsp = title_spacings[i % 4]

    return {
        "hf": hf, "bf": bf,
        "hbg": hbg, "hac": hac, "pri": pri, "lt": lt,
        "hacc": hacc, "tbrd": tbrd, "tot": tot, "sig": sig,
        "tw": tw, "tsp": tsp, "id": sid
    }

# --- BUILD FIXED LAYOUT HTML ---
def build_invoice(S, data, FS, pw, ph, pad):
    c = S; hf = c["hf"]; bf = c["bf"]
    hbg = c["hbg"]; hac = c["hac"]; pri = c["pri"]; lt = c["lt"]

    # --- HEADER ACCENT CSS ---
    hacc_css = ""
    if c["hacc"] == "thin-line":
        hacc_css = f"border-bottom:1px solid {hac};"
    elif c["hacc"] == "gradient-fade":
        hacc_css = f"border-bottom:3px solid transparent;border-image:linear-gradient(90deg,{hac},transparent) 1;"
    elif c["hacc"] == "double-line":
        hacc_css = f"border-bottom:3px double {hac};"
    elif c["hacc"] == "dotted-line":
        hacc_css = f"border-bottom:2px dotted {hac};"
    elif c["hacc"] == "thick-bottom":
        hacc_css = f"border-bottom:4px solid {pri};"
    elif c["hacc"] == "shadow-glow":
        hacc_css = f"box-shadow:0 4px 15px rgba(0,0,0,0.3);"
    elif c["hacc"] == "inner-border":
        hacc_css = f"border:1px solid {hac};border-top:none;"
    elif c["hacc"] == "diagonal-cut":
        hacc_css = f"clip-path:polygon(0 0,100% 0,100% calc(100% - 6px),0 100%);"
    elif c["hacc"] == "subtle-gradient":
        hacc_css = f"background:linear-gradient(180deg,{hbg} 80%,{hac} 100%);border:none;"

    # --- TABLE BORDER CSS ---
    brd = "1px solid #e0e0e0"
    if c["tbrd"] == "hairline": brd = "0.5px solid #ddd"
    elif c["tbrd"] == "thin": brd = "1px solid #ccc"
    elif c["tbrd"] == "medium": brd = "1.5px solid #bbb"
    elif c["tbrd"] == "dotted": brd = "1px dotted #bbb"
    elif c["tbrd"] == "dashed": brd = "1px dashed #bbb"
    elif c["tbrd"] == "double-bottom": brd = "1px solid #ddd"
    elif c["tbrd"] == "thick-bottom": brd = "1px solid #e0e0e0"
    elif c["tbrd"] == "color-accent": brd = f"1px solid {lt}"

    last_row_brd = brd
    if c["tbrd"] == "double-bottom": last_row_brd = f"3px double {pri}"
    elif c["tbrd"] == "thick-bottom": last_row_brd = f"2.5px solid {pri}"
    elif c["tbrd"] == "color-accent": last_row_brd = f"2px solid {pri}"

    # --- TOTAL HIGHLIGHT ---
    tot_inner = f'<div style="font-size:{FS["label"]}px;color:{pri};font-weight:700;text-transform:uppercase;letter-spacing:2px;font-family:{hf};">Grand Total</div><div style="font-size:{FS["grand"]}px;font-weight:900;color:{pri};margin:4px 0;line-height:1.1;">₹ {data["grand"]:,.2f}</div>'
    if c["tot"] == "bold-text":
        tot_html = f'<div style="text-align:right;">{tot_inner}</div>'
    elif c["tot"] == "bg-box":
        tot_html = f'<div style="text-align:right;background:{lt};padding:15px 20px;border-radius:6px;border:1px solid {lt};">{tot_inner}</div>'
    elif c["tot"] == "underline-accent":
        tot_html = f'<div style="text-align:right;">{tot_inner}<div style="height:3px;background:linear-gradient(90deg,transparent,{pri});margin-top:4px;border-radius:2px;"></div></div>'
    elif c["tot"] == "side-bar":
        tot_html = f'<div style="text-align:right;border-left:4px solid {pri};padding-left:15px;">{tot_inner}</div>'
    elif c["tot"] == "top-bottom-lines":
        tot_html = f'<div style="text-align:right;border-top:2px solid {pri};border-bottom:2px solid {pri};padding:10px 0;">{tot_inner}</div>'
    elif c["tot"] == "circle-bg":
        tot_html = f'<div style="text-align:right;">{tot_inner}</div>'

    # --- SIGNATURE ---
    if c["sig"] == "simple-line":
        sig_html = f'<div><div style="border-top:1.5px solid #333;width:200px;"></div><div style="font-size:{FS["xs"]}px;font-weight:700;margin-top:6px;color:{pri};font-family:{hf};text-transform:uppercase;letter-spacing:1px;">Authorized Signature</div></div>'
    elif c["sig"] == "double-line":
        sig_html = f'<div><div style="border-top:2px solid #333;width:200px;margin-bottom:3px;"></div><div style="border-top:1px solid #333;width:200px;"></div><div style="font-size:{FS["xs"]}px;font-weight:700;margin-top:6px;color:{pri};font-family:{hf};text-transform:uppercase;letter-spacing:1px;">Authorized Signature</div></div>'
    elif c["sig"] == "dotted-box":
        sig_html = f'<div style="border:1.5px dotted #bbb;padding:20px 25px;border-radius:4px;width:220px;"><div style="border-bottom:1px solid #ccc;width:160px;margin-bottom:6px;height:30px;"></div><div style="font-size:{FS["xs"]}px;font-weight:700;color:{pri};font-family:{hf};text-transform:uppercase;letter-spacing:1px;">Authorized Signature</div></div>'
    elif c["sig"] == "bracket":
        sig_html = f'<div style="border-left:3px solid {pri};border-bottom:3px solid {pri};padding:10px 15px;width:190px;"><div style="border-bottom:1px dashed #ccc;width:150px;margin-bottom:6px;height:25px;"></div><div style="font-size:{FS["xs"]}px;font-weight:700;color:{pri};font-family:{hf};text-transform:uppercase;letter-spacing:1px;">Authorized Signature</div></div>'
    elif c["sig"] == "stamp-circle":
        sig_html = f'<div style="width:85px;height:85px;border:2.5px double {pri};border-radius:50%;display:flex;align-items:center;justify-content:center;opacity:0.6;"><div style="text-align:center;font-size:{FS["xs"]}px;font-weight:900;color:{pri};font-family:{hf};text-transform:uppercase;letter-spacing:0.5px;line-height:1.2;">AUTHOR<br>IZED<br>SIGN</div></div>'
    elif c["sig"] == "minimal-text":
        sig_html = f'<div style="padding-top:30px;"><div style="height:35px;border-bottom:1px solid #ddd;width:180px;margin-bottom:5px;"></div><div style="font-size:{FS["xs"]}px;color:#999;font-family:{hf};text-transform:uppercase;letter-spacing:3px;font-weight:600;">Authorized Signature</div></div>'

    # --- AMOUNT IN WORDS ---
    words_variants = [
        f'background:{lt};border-left:4px solid {pri};padding:10px 12px;font-style:italic;font-size:{FS["words"]}px;color:#555;border-radius:0;',
        f'background:linear-gradient(90deg,{lt},transparent);padding:10px 12px;font-size:{FS["words"]}px;color:#555;border-radius:4px;',
        f'border:1px solid {lt};padding:10px 12px;font-size:{FS["words"]}px;color:#666;border-radius:4px;',
        f'padding:10px 0;border-bottom:1px solid {lt};font-size:{FS["words"]}px;color:#555;',
        f'background:{pri};color:white;padding:10px 12px;font-size:{FS["words"]}px;border-radius:4px;',
    ]
    words_style = words_variants[c["id"] % 5]
    words_html = f'<div style="margin:14px 0;{words_style}font-family:{bf};"><strong>Amount in Words:</strong> {data["words"]}</div>'

    # --- TABLE ROWS ---
    rows = ""
    for idx, item in enumerate(data["items"]):
        rows += f'<tr><td style="padding:10px 12px;border-bottom:{brd};font-size:{FS["table"]}px;font-family:{bf};">{item["desc"] if item["desc"] else "&nbsp;"}</td><td style="text-align:right;padding:10px 12px;border-bottom:{brd};font-size:{FS["table"]}px;font-weight:600;font-family:{bf};">₹ {item["amt"]:,.2f}</td></tr>'
    # Last row override
    if data["items"]:
        rows = rows.rstrip()
        last_close = rows.rfind("</tr>")
        rows = rows[:rows.rfind(f'border-bottom:{brd}')] + f'border-bottom:{last_row_brd};' + rows[rows.rfind(f'border-bottom:{brd}')+len(f'border-bottom:{brd};'):]

    # --- SUMMARY ---
    sum_html = ""
    if data["disc"] > 0 or data["tax"] > 0:
        sum_html = '<div style="display:flex;justify-content:flex-end;margin:8px 0 0 0;"><div style="width:230px;">'
        sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:3px 0;"><span style="color:#666;">Subtotal</span><span style="font-weight:600;">₹ {data["sub"]:,.2f}</span></div>'
        if data["disc"] > 0:
            sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:3px 0;color:#c0392b;"><span>Discount ({data["disc_type"]})</span><span>-₹ {data["disc"]:,.2f}</span></div>'
        if data["tax"] > 0:
            sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:3px 0;color:#27ae60;"><span>Tax ({data["tax_type"]})</span><span>+₹ {data["tax"]:,.2f}</span></div>'
        sum_html += '</div></div>'

    # --- FULL INVOICE ---
    invoice = f"""
    <!-- DARK HEADER STRIP -->
    <div style="background:{hbg};color:white;padding:{int(pad*0.8)}mm {pad}mm;{hacc_css}">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-family:{hf};font-size:{FS["title"]}px;font-weight:{c["tw"]};color:white;text-transform:uppercase;letter-spacing:{c["tsp"]};line-height:1.15;">{data["pname"]}</div>
                <div style="font-family:{bf};font-size:{FS["small"]}px;color:rgba(255,255,255,0.7);margin-top:4px;">{data["paddr"]}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:{hf};font-size:{FS["label"]}px;font-weight:700;color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:2px;">Invoice</div>
                <div style="font-family:{hf};font-size:{int(FS["title"]*0.55)}px;font-weight:700;color:white;margin-top:2px;"># {data["invno"]}</div>
                <div style="font-family:{bf};font-size:{FS["small"]}px;color:rgba(255,255,255,0.7);margin-top:2px;">{data["date"]}</div>
            </div>
        </div>
    </div>

    <!-- BODY -->
    <div style="padding:{pad}mm;flex:1;display:flex;flex-direction:column;">

        <!-- BILLED TO -->
        <div style="margin-bottom:20px;">
            <div style="font-family:{hf};font-size:{FS["label"]}px;font-weight:700;color:{pri};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;">Billed To</div>
            <div style="font-family:{hf};font-size:{int(FS["title"]*0.6)}px;font-weight:700;color:#222;">{data["cname"]}</div>
            <div style="white-space:pre-wrap;color:#555;line-height:1.5;font-size:{FS["small"]}px;margin-top:2px;font-family:{bf};">{data["caddr"]}</div>
        </div>

        <!-- TABLE -->
        <div style="margin-bottom:4px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <div style="font-family:{hf};font-size:{FS["label"]}px;font-weight:700;color:{pri};text-transform:uppercase;letter-spacing:1.5px;">Item Details</div>
                <span style="background:{lt};color:{pri};font-size:{FS["xs"]}px;padding:2px 8px;border-radius:10px;font-weight:600;">{len(data["items"])} items</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead>
                    <tr>
                        <th style="text-align:left;padding:10px 12px;border-bottom:2px solid {pri};font-size:{FS["thead"]}px;font-weight:700;color:{pri};text-transform:uppercase;letter-spacing:0.5px;font-family:{hf};">Description</th>
                        <th style="text-align:right;padding:10px 12px;border-bottom:2px solid {pri};font-size:{FS["thead"]}px;font-weight:700;color:{pri};text-transform:uppercase;letter-spacing:0.5px;font-family:{hf};">Amount (₹)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        {sum_html}

        {words_html}

        <!-- BOTTOM: SIGNATURE + TOTAL -->
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;padding-top:15px;">
            <div>{sig_html}</div>
            <div style="min-width:200px;">{tot_html}</div>
        </div>
    </div>
    """

    return invoice

# ===================== SIDEBAR =====================
st.sidebar.header("🎨 Template Engine")
style_id = st.sidebar.number_input("Style ID (1–1000)", min_value=1, max_value=1000, value=1, key="sid")

st.sidebar.markdown("---")
st.sidebar.header("📄 Paper Size")
sheet_size = st.sidebar.radio(" ", ["A4", "A5", "Letter"], index=0, label_visibility="collapsed", horizontal=True,
    format_func=lambda x: {"A4":" A4 ","A5":" A5 ","Letter":" Letter "}[x])
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

col_d, col_t = st.sidebar.columns(2)
with col_d:
    disc_type = st.selectbox("Discount", ["None", "Flat ₹", "%"], index=0)
    disc_val = st.number_input("Discount Val", min_value=0.0, value=0.0, step=0.01, disabled=(disc_type=="None"), key="dv")
with col_t:
    tax_type = st.selectbox("Tax", ["None", "Flat ₹", "%"], index=0)
    tax_val = st.number_input("Tax Val", min_value=0.0, value=0.0, step=0.01, disabled=(tax_type=="None"), key="tv")

st.sidebar.markdown("---")
st.sidebar.header("📦 Line Items")
for i, item in enumerate(st.session_state.line_items):
    c1, c2, c3, c4 = st.sidebar.columns([5,1,3,1])
    with c1: item["desc"] = st.text_input("D", value=item["desc"], key=f"d_{i}", label_visibility="collapsed", placeholder="Description...")
    with c2: st.markdown(f"<div style='text-align:center;padding-top:22px;font-size:10px;color:#888;'>#{i+1}</div>", unsafe_allow_html=True)
    with c3: item["amt"] = st.number_input("₹", value=item["amt"], min_value=0.0, step=0.01, key=f"a_{i}", label_visibility="collapsed", format="%.2f")
    with c4:
        st.markdown("<div style='padding-top:18px;'></div>", unsafe_allow_html=True)
        if st.button("✕", key=f"x_{i}", use_container_width=True, disabled=(len(st.session_state.line_items)<=1)):
            remove_item(i); st.rerun()
st.sidebar.button("➕ Add Line Item", on_click=add_item, use_container_width=True, type="secondary")

# --- CALC ---
subtotal = sum(it["amt"] for it in st.session_state.line_items)
disc_amt = disc_val if disc_type=="Flat ₹" else (subtotal * disc_val/100 if disc_type=="%" else 0)
tax_amt = tax_val if tax_type=="Flat ₹" else ((subtotal-disc_amt)*tax_val/100 if tax_type=="%" else 0)
grand_total = subtotal - disc_amt + tax_amt

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Subtotal:** ₹{subtotal:,.2f}")
if disc_amt>0: st.sidebar.markdown(f"~~Discount~~: -₹{disc_amt:,.2f}")
if tax_amt>0: st.sidebar.markdown(f"**Tax:** +₹{tax_amt:,.2f}")
st.sidebar.markdown(f"### Total: ₹{grand_total:,.2f}")

# ===================== RENDER =====================
S = get_style(style_id)

sheet_dims = {"A4":{"w":210,"h":297},"A5":{"w":148,"h":210},"Letter":{"w":216,"h":279}}
dim = sheet_dims[sheet_size]
if orientation=="Landscape": dim={"w":dim["h"],"h":dim["w"]}
pw, ph = dim["w"], dim["h"]

sc = pw/210.0; small = sheet_size=="A5"
if small:
    FS={"title":17,"small":9,"xs":7,"table":10,"thead":8,"grand":20,"words":9,"label":7}
    pad=6
else:
    FS={"title":int(28*sc),"small":int(13*sc),"xs":int(9*sc),"table":int(14*sc),"thead":int(10*sc),"grand":int(30*sc),"words":int(11*sc),"label":int(9*sc)}
    pad=int(10*sc)

ps = 1.0
if small and orientation=="Portrait": ps=1.45
elif small and orientation=="Landscape": ps=1.3
elif sheet_size=="Letter" and orientation=="Landscape": ps=0.95

data = {
    "pname": p_name, "paddr": p_addr,
    "cname": c_name, "caddr": c_addr,
    "invno": inv_no, "date": inv_date.strftime("%d %b, %Y"),
    "items": st.session_state.line_items,
    "sub": subtotal, "disc": disc_amt, "disc_type": disc_type,
    "tax": tax_amt, "tax_type": tax_type,
    "grand": grand_total, "words": number_to_words(grand_total)
}

invoice_html = build_invoice(S, data, FS, pw, ph, pad)

base_css = f"""
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;margin:0;padding:0;}}
@page{{size:{pw}mm {ph}mm;margin:0;}}
body{{background:#e0e0e0;margin:0;padding:20px;font-family:{S['bf']};display:flex;flex-direction:column;align-items:center;min-height:100vh;}}
.wrap{{transform:scale({ps});transform-origin:top center;}}
.card{{background:white;width:{pw}mm;min-height:{ph}mm;display:flex;flex-direction:column;overflow:hidden;position:relative;}}
@media print{{body{{background:none;padding:0;display:block;}}.wrap{{transform:none!important;}}.card{{box-shadow:none;width:{pw}mm;min-height:{ph}mm;}}.print-btn{{display:none!important;}}}}
"""

print_html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600;700&family=Outfit:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Sora:wght@400;600;700&family=Libre+Baskerville:wght@400;700&family=Manrope:wght@400;600;700&family=Cormorant+Garamond:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700&family=Lora:wght@400;600;700&family=Bricolage+Grotesk:wght@400;700&family=EB+Garamond:wght@400;600;700&family=Geist:wght@400;700&family=Instrument+Serif:wght@400;700&family=Onest:wght@400;700&family=Fraunces:wght@400;700&family=Nunito+Sans:wght@400;600;700&family=Merriweather:wght@400;700&family=Figtree:wght@400;600;700&family=Bitter:wght@400;700&family=General+Sans:wght@400;700&family=DM+Serif+Display:wght@400;700&family=Poppins:wght@400;600;700&family=Space+Mono:wght@400;700&family=Montserrat:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Roboto+Slab:wght@400;700&family=Work+Sans:wght@400;600;700&family=Literata:wght@400;700&family=Lexend:wght@400;600;700&family=Fira+Code:wght@400;700&family=Supreme:wght@400;700&family=Newsreader:wght@400;700&family=Cabinet+Grotesk:wght@400;700&display=swap" rel="stylesheet">
<style>{base_css}</style></head><body>
<div class="wrap"><div class="card">{invoice_html}</div></div>
<script>window.onload=function(){{window.print();}}</script>
</body></html>"""

preview_html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600;700&family=Outfit:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Sora:wght@400;600;700&family=Libre+Baskerville:wght@400;700&family=Manrope:wght@400;600;700&family=Cormorant+Garamond:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700&family=Lora:wght@400;600;700&family=Bricolage+Grotesk:wght@400;700&family=EB+Garamond:wght@400;600;700&family=Geist:wght@400;700&family=Instrument+Serif:wght@400;700&family=Onest:wght@400;700&family=Fraunces:wght@400;700&family=Nunito+Sans:wght@400;600;700&family=Merriweather:wght@400;700&family=Figtree:wght@400;600;700&family=Bitter:wght@400;700&family=General+Sans:wght@400;700&family=DM+Serif+Display:wght@400;700&family=Poppins:wght@400;600;700&family=Space+Mono:wght@400;700&family=Montserrat:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Roboto+Slab:wght@400;700&family=Work+Sans:wght@400;600;700&family=Literata:wght@400;700&family=Lexend:wght@400;600;700&family=Fira+Code:wght@400;700&family=Supreme:wght@400;700&family=Newsreader:wght@400;700&family=Cabinet+Grotesk:wght@400;700&display=swap" rel="stylesheet">
<style>{base_css}.card{{box-shadow:0 4px 24px rgba(0,0,0,0.12);}}
.print-btn{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:999;background:{S['hbg']};color:white;padding:14px 50px;border:none;border-radius:6px;font-weight:700;cursor:pointer;letter-spacing:1px;font-size:13px;box-shadow:0 4px 15px rgba(0,0,0,0.25);font-family:{S['hf']};transition:transform 0.15s,box-shadow 0.15s;}}
.print-btn:hover{{transform:translateX(-50%) translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.35);}}
</style></head><body>
<div class="wrap"><div class="card">{invoice_html}</div></div>
<button class="print-btn" onclick="printClean()">🖨️ PRINT — Style #{style_id}</button>
<script>
function printClean(){{
    const h=`{print_html.replace('`','\\`').replace('</script>','<\\/script>')}`;
    const w=window.open('','_blank');w.document.write(h);w.document.close();
}}
</script>
</body></html>"""

bh = {"A4":1100,"A5":800,"Letter":1050}
dh = int(bh[sheet_size]*ps)+150+max(0,(len(st.session_state.line_items)-3)*40)
components.html(preview_html, height=dh, scrolling=True)
