import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Dynamic Invoice Generator", layout="wide")

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

# --- MASSIVE STYLE ENGINE ---
def get_style(sid):
    """Returns a complete style dict for a given ID. 1000 unique combinations."""
    i = sid - 1

    # --- 20 FONT PAIRS ---
    font_pairs = [
        ("'DM Sans', sans-serif", "'Space Grotesk', sans-serif"),
        ("'Playfair Display', serif", "'Source Sans 3', sans-serif"),
        ("'Outfit', sans-serif", "'Crimson Text', serif"),
        ("'Sora', sans-serif", "'Libre Baskerville', serif"),
        ("'Cabinet Grotesk', sans-serif", "'Garamond', serif"),
        ("'Manrope', sans-serif", "'Cormorant Garamond', serif"),
        ("'Plus Jakarta Sans', sans-serif", "'Lora', serif"),
        ("'Bricolage Grotesque', sans-serif", "'EB Garamond', serif"),
        ("'Geist', sans-serif", "'Instrument Serif', serif"),
        ("'Onest', sans-serif", "'Fraunces', serif"),
        ("'Nunito Sans', sans-serif", "'Merriweather', serif"),
        ("'Figtree', sans-serif", "'Bitter', serif"),
        ("'Supreme', sans-serif", "'Newsreader', serif"),
        ("'General Sans', sans-serif", "'DM Serif Display', serif"),
        ("'Poppins', sans-serif", "'Space Mono', monospace"),
        ("'Montserrat', sans-serif", "'IBM Plex Mono', monospace"),
        ("'Inter', sans-serif", "'JetBrains Mono', monospace"),
        ("'Roboto Condensed', sans-serif", "'Roboto Slab', serif"),
        ("'Work Sans', sans-serif", "'Literata', serif"),
        ("'Lexend', sans-serif", "'Fira Code', monospace"),
    ]
    head_font, body_font = font_pairs[i % 20]

    # --- 20 COLOR PALETTES (primary, secondary, accent, bg_tint) ---
    palettes = [
        ("#1a365d", "#2b6cb0", "#e2e8f0", "#f7fafc"),  # Navy Blue
        ("#1c4532", "#276749", "#c6f6d5", "#f0fff4"),  # Forest Green
        ("#742a2a", "#c53030", "#fed7d7", "#fff5f5"),  # Crimson
        ("#44337a", "#6b46c1", "#e9d8fd", "#faf5ff"),  # Royal Purple
        ("#7b341e", "#c05621", "#feebc8", "#fffaf0"),  # Burnt Orange
        ("#234e52", "#319795", "#b2f5ea", "#e6fffa"),  # Teal
        ("#2d3748", "#4a5568", "#e2e8f0", "#f7fafc"),  # Slate
        ("#553c9a", "#805ad5", "#e9d8fd", "#faf5ff"),  # Violet
        ("#22543d", "#38a169", "#c6f6d5", "#f0fff4"),  # Emerald
        ("#9b2c2c", "#e53e3e", "#fed7d7", "#fff5f5"),  # Red
        ("#2a4365", "#4299e1", "#bee3f8", "#ebf8ff"),  # Sky Blue
        ("#744210", "#d69e2e", "#fefcbf", "#fffff0"),  # Gold
        ("#702459", "#b83280", "#fed7e2", "#fff5f7"),  # Pink
        ("#285e61", "#3bc4c4", "#b2f5ea", "#e6fffa"),  # Cyan
        ("#5a3e36", "#a0705e", "#fde8d8", "#fffbf5"),  # Warm Brown
        ("#1a202c", "#2d3748", "#edf2f7", "#f7fafc"),  # Charcoal
        ("#065f46", "#10b981", "#d1fae5", "#ecfdf5"),  # Mint
        ("#92400e", "#f59e0b", "#fef3c7", "#fffbeb"),  # Amber
        ("#4c1d95", "#7c3aed", "#ddd6fe", "#f5f3ff"),  # Indigo
        ("#831843", "#ec4899", "#fce7f3", "#fdf2f8"),  # Fuchsia
    ]
    c1, c2, c3, c4 = palettes[i % 20]

    # --- 10 HEADER LAYOUTS ---
    header_layouts = [
        "flex-row-space-between",          # 0: Left name, right invoice#
        "flex-row-center-col",             # 1: Centered name, # below
        "flex-row-reverse",                # 2: Right name, left invoice#
        "left-bar-name-top",               # 3: Thick left bar, name big on top
        "centered-stacked",                # 4: Everything centered stacked
        "dual-box",                        # 5: Two equal boxes side by side
        "name-across-top",                 # 6: Name full width, # below right
        "right-aligned-name",              # 7: Everything right-aligned
        "invoice-no-banner",               # 8: Invoice # as a banner strip
        "minimal-inline",                  # 9: Single line, minimal
    ]
    header_type = header_layouts[i % 10]

    # --- 8 TABLE STYLES ---
    table_styles = [
        "filled-header",                   # 0: Colored header, white text
        "underline-header",                # 1: No bg, thick bottom border
        "boxed-cells",                     # 2: Full grid borders
        "striped-rows",                    # 3: Alternating row colors
        "minimal-line",                    # 4: Hairline separators only
        "dotted-lines",                    # 5: Dotted row separators
        "rounded-modern",                  # 6: Rounded header, soft shadows
        "bold-accent-left",                # 7: Thick left border on rows
    ]
    table_type = table_styles[i % 8]

    # --- 8 DECORATIVE STYLES ---
    deco_styles = [
        "corner-shapes",                   # 0: Geometric corner shapes
        "top-gradient-bar",                # 1: Gradient top bar
        "side-stripe",                     # 2: Thick side stripe
        "double-border",                   # 3: Double border frame
        "dot-pattern",                     # 4: Subtle dot pattern bg
        "diagonal-watermark",              # 5: Diagonal watermark text
        "bottom-accent",                   # 6: Thick bottom accent bar
        "circle-badge",                    # 7: Circle badge with initial
    ]
    deco_type = deco_styles[i % 8]

    # --- 6 TOTAL BLOCK STYLES ---
    total_styles = [
        "right-aligned-bold",              # 0: Simple right aligned
        "boxed-highlight",                 # 1: Background box with border
        "underline-grow",                  # 2: Growing underline effect
        "circle-total",                    # 3: Circular highlight
        "banner-strip",                    # 4: Full width colored strip
        "minimal-spacing",                 # 5: Lots of whitespace
    ]
    total_type = total_styles[i % 6]

    # --- 6 SIGNATURE STYLES ---
    sig_styles = [
        "simple-line",                     # 0: Line + text below
        "dotted-line-box",                 # 1: Dotted line in light box
        "stamp-style",                     # 2: Circular stamp-like
        "bracket-style",                   # 3: Bracket corners
        "double-underline",                # 4: Double underline
        "minimal-text",                    # 5: Just text, no line
    ]
    sig_type = sig_styles[i % 6]

    # --- Typography variations ---
    title_cases = ["UPPERCASE", "uppercase", "Capitalize", "normal"]
    title_case = title_cases[(i // 3) % 4]
    letter_spacings = ["0px", "1px", "2px", "3px", "4px"]
    letter_sp = letter_spacings[i % 5]
    title_weights = ["700", "800", "900"]
    title_weight = title_weights[i % 3]

    # Border radius
    radii = ["0px", "4px", "8px", "12px", "20px"]
    radius = radii[i % 5]

    return {
        "head_font": head_font, "body_font": body_font,
        "c1": c1, "c2": c2, "c3": c3, "c4": c4,
        "header_type": header_type, "table_type": table_type,
        "deco_type": deco_type, "total_type": total_type,
        "sig_type": sig_type, "title_case": title_case,
        "letter_sp": letter_sp, "title_weight": title_weight,
        "radius": radius, "id": sid,
    }

# --- BUILD DECORATIVE CSS ---
def build_deco_css(s):
    d = s["deco_type"]; c = s["c1"]; c2 = s["c2"]; c3 = s["c3"]; r = s["radius"]
    css = ""
    if d == "corner-shapes":
        css = f"""
        .deco-tl, .deco-br {{ position:absolute; width:50px; height:50px; pointer-events:none; }}
        .deco-tl {{ top:0;left:0;border-top:4px solid {c};border-left:4px solid {c};border-radius:{r} 0 0 0; }}
        .deco-br {{ bottom:0;right:0;border-bottom:4px solid {c};border-right:4px solid {c};border-radius:0 0 {r} 0; }}"""
    elif d == "top-gradient-bar":
        css = f"""
        .deco-bar {{ position:absolute;top:0;left:0;right:0;height:8px;
            background:linear-gradient(90deg,{c},{c2},{c}); }}"""
    elif d == "side-stripe":
        css = f"""
        .deco-side {{ position:absolute;top:0;left:0;bottom:0;width:8px;background:{c}; }}"""
    elif d == "double-border":
        css = f"""
        .deco-frame {{ position:absolute;top:4px;left:4px;right:4px;bottom:4px;
            border:1px solid {c3};pointer-events:none;border-radius:{r}; }}"""
    elif d == "dot-pattern":
        css = f"""
        .deco-dots {{ position:absolute;top:0;left:0;right:0;bottom:0;
            background-image:radial-gradient({c3} 1px,transparent 1px);
            background-size:20px 20px;opacity:0.3;pointer-events:none;z-index:0; }}"""
    elif d == "diagonal-watermark":
        css = f"""
        .deco-watermark {{ position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-30deg);
            font-size:80px;color:{c3};opacity:0.08;font-weight:900;pointer-events:none;
            font-family:{s['head_font']};white-space:nowrap;letter-spacing:10px;text-transform:uppercase; }}"""
    elif d == "bottom-accent":
        css = f"""
        .deco-bottom {{ position:absolute;bottom:0;left:0;right:0;height:6px;
            background:linear-gradient(90deg,{c},{c2}); }}"""
    elif d == "circle-badge":
        initial = "INV"
        css = f"""
        .deco-circle {{ position:absolute;top:15px;right:15px;width:55px;height:55px;
            border:3px solid {c};border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-size:14px;font-weight:900;color:{c};font-family:{s['head_font']};letter-spacing:1px; }}"""
    return css

# --- BUILD HEADER HTML ---
def build_header_html(s, p_name, p_addr, inv_no, inv_date, fs):
    h = s["header_type"]; c = s["c1"]; c2 = s["c2"]; hf = s["head_font"]
    tc = s["title_case"]; ls = s["letter_sp"]; tw = s["title_weight"]
    tn = fs["title"]; sn = fs["small"]; xs = fs["xs"]

    name_el = f'<div style="font-family:{hf};font-size:{tn}px;font-weight:{tw};color:{c};text-transform:{tc};letter-spacing:{ls};line-height:1.1;">{p_name}</div>'
    addr_el = f'<div style="font-family:{s["body_font"]};font-size:{sn}px;color:#666;margin-top:4px;">{p_addr}</div>'
    inv_el = f'<div style="font-family:{hf};font-size:{int(tn*0.55)}px;font-weight:700;color:{c};"># {inv_no}</div>'
    date_el = f'<div style="font-family:{s["body_font"]};font-size:{sn}px;color:#555;font-weight:600;">{inv_date}</div>'

    if h == "flex-row-space-between":
        return f'<div style="display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;"><div>{name_el}{addr_el}</div><div style="text-align:right;">{inv_el}{date_el}</div></div>'
    elif h == "flex-row-center-col":
        return f'<div style="text-align:center;padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;">{name_el}{addr_el}<div style="margin-top:10px;">{inv_el}{date_el}</div></div>'
    elif h == "flex-row-reverse":
        return f'<div style="display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;"><div>{inv_el}{date_el}</div><div style="text-align:right;">{name_el}{addr_el}</div></div>'
    elif h == "left-bar-name-top":
        return f'<div style="border-left:5px solid {c};padding-left:15px;padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;">{name_el}{addr_el}<div style="margin-top:10px;text-align:right;">{inv_el}{date_el}</div></div>'
    elif h == "centered-stacked":
        return f'<div style="text-align:center;padding-bottom:20px;border-bottom:2px solid {c};margin-bottom:20px;"><div style="font-size:{xs}px;color:{c};font-weight:700;letter-spacing:3px;text-transform:uppercase;font-family:{hf};">INVOICE</div>{name_el}<div style="margin-top:4px;">{addr_el}</div><div style="margin-top:12px;">{inv_el} &nbsp;·&nbsp; {date_el}</div></div>'
    elif h == "dual-box":
        return f'<div style="display:flex;gap:15px;margin-bottom:20px;"><div style="flex:1;background:{s["c4"]};padding:15px;border-radius:{s["radius"]};border:1px solid {s["c3"]};">{name_el}{addr_el}</div><div style="flex:1;background:{s["c4"]};padding:15px;border-radius:{s["radius"]};border:1px solid {s["c3"]};text-align:right;display:flex;flex-direction:column;justify-content:center;"><div style="font-size:{xs}px;color:{c};font-weight:700;letter-spacing:2px;text-transform:uppercase;font-family:{hf};">Invoice</div>{inv_el}{date_el}</div></div>'
    elif h == "name-across-top":
        return f'<div style="padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;">{name_el}{addr_el}<div style="display:flex;justify-content:flex-end;gap:20px;margin-top:8px;">{inv_el}{date_el}</div></div>'
    elif h == "right-aligned-name":
        return f'<div style="text-align:right;padding-bottom:15px;border-bottom:1px solid {s["c3"]};margin-bottom:20px;">{name_el}{addr_el}<div style="margin-top:10px;">{inv_el}{date_el}</div></div>'
    elif h == "invoice-no-banner":
        return f'<div style="background:{c};color:white;padding:12px 15px;border-radius:{s["radius"]};margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;"><div style="font-family:{hf};font-size:{int(tn*0.8)}px;font-weight:{tw};text-transform:{tc};letter-spacing:{ls};">{p_name}</div><div style="font-family:{hf};font-size:{sn}px;font-weight:700;"># {inv_no} &nbsp;|&nbsp; {inv_date}</div></div>'
    elif h == "minimal-inline":
        return f'<div style="display:flex;align-items:baseline;gap:15px;padding-bottom:12px;border-bottom:1px solid #ddd;margin-bottom:20px;flex-wrap:wrap;">{name_el}<span style="color:#ccc;">|</span>{addr_el}<div style="margin-left:auto;display:flex;gap:15px;align-items:baseline;">{inv_el}<span style="color:#ccc;">·</span>{date_el}</div></div>'
    return f'<div>{name_el}{addr_el}{inv_el}{date_el}</div>'

# --- BUILD TABLE CSS ---
def build_table_css(s, fs):
    t = s["table_type"]; c = s["c1"]; c3 = s["c3"]; tf = fs["table"]; thf = fs["thead"]; r = s["radius"]
    css = ".items-table { width:100%; border-collapse:collapse; margin:8px 0; }\n"
    if t == "filled-header":
        css += f".items-table th {{ background:{c}; color:white; padding:10px;text-align:left;font-size:{thf}px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-family:{s['head_font']}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px;border-bottom:1px solid #eee;font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "underline-header":
        css += f".items-table th {{ padding:10px;text-align:left;font-size:{thf}px;font-weight:700;color:{c};border-bottom:3px solid {c};font-family:{s['head_font']};text-transform:uppercase; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px;border-bottom:1px solid #eee;font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "boxed-cells":
        css += f".items-table th {{ background:{s['c4']};padding:10px;text-align:left;font-size:{thf}px;font-weight:700;color:{c};border:1px solid {c3};font-family:{s['head_font']}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px;border:1px solid {c3};font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "striped-rows":
        css += f".items-table th {{ background:{c};color:white;padding:10px;text-align:left;font-size:{thf}px;font-weight:700;font-family:{s['head_font']}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table tr:nth-child(even) {{ background:{s['c4']}; }}\n"
        css += f".items-table td {{ padding:10px;border-bottom:1px solid #eee;font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "minimal-line":
        css += f".items-table th {{ padding:8px 10px;text-align:left;font-size:{thf}px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid #ddd;font-family:{s['head_font']}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px;border-bottom:1px solid #f0f0f0;font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "dotted-lines":
        css += f".items-table th {{ padding:10px;text-align:left;font-size:{thf}px;font-weight:700;color:{c};border-bottom:2px dotted {c3};font-family:{s['head_font']};text-transform:uppercase; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px;border-bottom:1px dotted {c3};font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
    elif t == "rounded-modern":
        css += f".items-table {{ border-radius:{r};overflow:hidden;border:1px solid {c3}; }}\n"
        css += f".items-table th {{ background:{c};color:white;padding:12px;text-align:left;font-size:{thf}px;font-weight:700;font-family:{s['head_font']}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px 12px;border-bottom:1px solid {c3};font-size:{tf}px;font-family:{s['body_font']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600; }}\n"
        css += f".items-table tr:last-child td {{ border-bottom:none; }}\n"
    elif t == "bold-accent-left":
        css += f".items-table th {{ padding:10px 10px 10px 15px;text-align:left;font-size:{thf}px;font-weight:700;color:{c};font-family:{s['head_font']};text-transform:uppercase;border-bottom:2px solid {c}; }}\n"
        css += f".items-table th:last-child {{ text-align:right; }}\n"
        css += f".items-table td {{ padding:10px 10px 10px 15px;border-bottom:1px solid #eee;font-size:{tf}px;font-family:{s['body_font']};border-left:3px solid transparent; }}\n"
        css += f".items-table tr:hover td {{ border-left-color:{c};background:{s['c4']}; }}\n"
        css += f".items-table td:last-child {{ text-align:right;font-weight:600;border-left:none!important; }}\n"
    return css

# --- BUILD TOTAL BLOCK HTML ---
def build_total_html(s, grand_total, fs):
    t = s["total_type"]; c = s["c1"]; c3 = s["c3"]; c4 = s["c4"]; r = s["radius"]
    gt = fs["grand"]
    if t == "right-aligned-bold":
        return f'<div style="text-align:right;margin-top:15px;"><div style="font-size:{fs["xs"]}px;color:{c};font-weight:700;text-transform:uppercase;letter-spacing:2px;font-family:{s["head_font"]};">Grand Total</div><div style="font-size:{gt}px;font-weight:900;color:{c};margin:4px 0;">₹ {grand_total:,.2f}</div></div>'
    elif t == "boxed-highlight":
        return f'<div style="background:{c4};border:2px solid {c};border-radius:{r};padding:15px;text-align:right;margin-top:15px;"><div style="font-size:{fs["xs"]}px;color:{c};font-weight:700;text-transform:uppercase;letter-spacing:2px;font-family:{s["head_font"]};">Grand Total</div><div style="font-size:{gt}px;font-weight:900;color:{c};margin:4px 0;">₹ {grand_total:,.2f}</div></div>'
    elif t == "underline-grow":
        return f'<div style="text-align:right;margin-top:15px;"><div style="font-size:{fs["xs"]}px;color:{c};font-weight:700;text-transform:uppercase;letter-spacing:2px;font-family:{s["head_font"]};">Grand Total</div><div style="font-size:{gt}px;font-weight:900;color:{c};margin:4px 0;">₹ {grand_total:,.2f}</div><div style="height:4px;background:linear-gradient(90deg,{c3},{c});border-radius:2px;margin-top:4px;"></div></div>'
    elif t == "circle-total":
        return f'<div style="display:flex;justify-content:flex-end;margin-top:15px;"><div style="width:{int(gt*2.5)}px;height:{int(gt*2.5)}px;border:4px solid {c};border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;"><div style="font-size:{fs["xs"]}px;color:{c};font-weight:700;text-transform:uppercase;letter-spacing:1px;font-family:{s["head_font"]};">Total</div><div style="font-size:{int(gt*0.6)}px;font-weight:900;color:{c};">₹ {grand_total:,.2f}</div></div></div>'
    elif t == "banner-strip":
        return f'<div style="background:{c};color:white;padding:15px 20px;border-radius:{r};margin-top:15px;display:flex;justify-content:space-between;align-items:center;"><div style="font-size:{fs["small"]}px;font-weight:700;text-transform:uppercase;letter-spacing:2px;font-family:{s["head_font"]};">Grand Total</div><div style="font-size:{gt}px;font-weight:900;">₹ {grand_total:,.2f}</div></div>'
    elif t == "minimal-spacing":
        return f'<div style="text-align:right;margin-top:30px;padding-top:15px;"><div style="font-size:{fs["xs"]}px;color:#999;font-weight:600;text-transform:uppercase;letter-spacing:3px;font-family:{s["head_font"]};">Amount Payable</div><div style="font-size:{gt}px;font-weight:300;color:{c};margin:8px 0;">₹ {grand_total:,.2f}</div></div>'
    return f'<div style="text-align:right;font-size:{gt}px;font-weight:900;color:{c};">₹ {grand_total:,.2f}</div>'

# --- BUILD SIGNATURE HTML ---
def build_sig_html(s, fs):
    t = s["sig_type"]; c = s["c1"]; c3 = s["c3"]; c4 = s["c4"]; r = s["radius"]
    if t == "simple-line":
        return f'<div style="margin-top:35px;"><div style="border-top:2px solid #000;width:180px;"></div><div style="font-size:{fs["xs"]}px;font-weight:700;margin-top:6px;font-family:{s["head_font"]};">Authorized Signatory</div></div>'
    elif t == "dotted-line-box":
        return f'<div style="margin-top:35px;background:{c4};padding:15px;border-radius:{r};border:1px solid {c3};display:inline-block;"><div style="border-top:2px dotted #000;width:160px;"></div><div style="font-size:{fs["xs"]}px;font-weight:700;margin-top:6px;color:{c};font-family:{s["head_font"]};">Authorized Signatory</div></div>'
    elif t == "stamp-style":
        return f'<div style="margin-top:30px;width:90px;height:90px;border:3px double {c};border-radius:50%;display:flex;align-items:center;justify-content:center;opacity:0.7;"><div style="text-align:center;font-size:{fs["xs"]}px;font-weight:900;color:{c};font-family:{s["head_font"]};text-transform:uppercase;letter-spacing:1px;line-height:1.2;">AUTHOR<br>IZED<br>SIGN</div></div>'
    elif t == "bracket-style":
        return f'<div style="margin-top:35px;padding:10px 15px;border-left:3px solid {c};border-bottom:3px solid {c};width:180px;"><div style="border-top:1px dashed {c3};width:100%;margin-bottom:6px;"></div><div style="font-size:{fs["xs"]}px;font-weight:700;color:{c};font-family:{s["head_font"]};">Authorized Signatory</div></div>'
    elif t == "double-underline":
        return f'<div style="margin-top:35px;"><div style="border-top:2px solid #000;width:180px;margin-bottom:3px;"></div><div style="border-top:1px solid #000;width:180px;"></div><div style="font-size:{fs["xs"]}px;font-weight:700;margin-top:6px;font-family:{s["head_font"]};color:{c};">Authorized Signatory</div></div>'
    elif t == "minimal-text":
        return f'<div style="margin-top:40px;font-size:{fs["xs"]}px;color:#999;font-family:{s["head_font"]};text-transform:uppercase;letter-spacing:3px;font-weight:600;">Authorized Signatory</div>'
    return '<div style="margin-top:35px;border-top:2px solid #000;width:180px;"></div>'

# --- BUILD AMOUNT IN WORDS HTML ---
def build_words_html(s, words, fs):
    c = s["c1"]; c3 = s["c3"]; c4 = s["c4"]; r = s["radius"]
    style_variants = [
        f'background:{c4};border-left:4px solid {c};padding:10px;font-style:italic;font-size:{fs["xs"]}px;color:#555;',
        f'background:linear-gradient(90deg,{c4},transparent);padding:10px;font-size:{fs["xs"]}px;color:#555;border-radius:{r};',
        f'border:1px dashed {c3};padding:10px;font-size:{fs["xs"]}px;color:#666;border-radius:{r};',
        f'padding:10px 0;border-bottom:1px solid {c3};font-size:{fs["xs"]}px;color:#555;',
        f'background:{c};color:white;padding:10px;font-size:{fs["xs"]}px;border-radius:{r};',
    ]
    variant = style_variants[s["id"] % 5]
    return f'<div style="margin:12px 0;{variant}font-family:{s["body_font"]};"><strong>Amount in Words:</strong> {words}</div>'

# ===================== SIDEBAR =====================
st.sidebar.header("🎨 Template Engine")
style_id = st.sidebar.number_input("Template ID (1–1000)", min_value=1, max_value=1000, value=1, key="sid")

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

# ===================== RENDER ENGINE =====================
S = get_style(style_id)

sheet_dims = {"A4":{"w":210,"h":297},"A5":{"w":148,"h":210},"Letter":{"w":216,"h":279}}
dim = sheet_dims[sheet_size]
if orientation=="Landscape": dim={"w":dim["h"],"h":dim["w"]}
pw, ph = dim["w"], dim["h"]

sc = pw/210.0; small = sheet_size=="A5"
if small:
    FS={"title":18,"small":9,"xs":7,"table":10,"thead":8,"grand":20,"words":9,"label":7}
    pad=6; bw=3
else:
    FS={"title":int(30*sc),"small":int(13*sc),"xs":int(9*sc),"table":int(14*sc),"thead":int(10*sc),"grand":int(30*sc),"words":int(11*sc),"label":int(9*sc)}
    pad=int(10*sc); bw=int(6*sc)

ps = 1.0
if small and orientation=="Portrait": ps=1.45
elif small and orientation=="Landscape": ps=1.3
elif sheet_size=="Letter" and orientation=="Landscape": ps=0.95

# Table rows
rows_html = ""
for idx, item in enumerate(st.session_state.line_items):
    rows_html += f'<tr><td>{item["desc"] if item["desc"] else "&nbsp;"}</td><td>₹ {item["amt"]:,.2f}</td></tr>'

# Summary
sum_html = ""
if disc_amt>0 or tax_amt>0:
    sum_html = f'<div style="display:flex;justify-content:flex-end;margin:10px 0 0 0;"><div style="width:220px;">'
    sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:2px 0;"><span style="color:#666;">Subtotal</span><span style="font-weight:600;">₹ {subtotal:,.2f}</span></div>'
    if disc_amt>0: sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:2px 0;color:#e74c3c;"><span>Discount ({disc_type})</span><span>-₹ {disc_amt:,.2f}</span></div>'
    if tax_amt>0: sum_html += f'<div style="display:flex;justify-content:space-between;font-size:{FS["small"]}px;padding:2px 0;color:#27ae60;"><span>Tax ({tax_type})</span><span>+₹ {tax_amt:,.2f}</span></div>'
    sum_html += '</div></div>'

words = number_to_words(grand_total)
deco_css = build_deco_css(S)
header_html = build_header_html(S, p_name, p_addr, inv_no, inv_date.strftime("%d %b, %Y"), FS)
table_css = build_table_css(S, FS)
total_html = build_total_html(S, grand_total, FS)
sig_html = build_sig_html(S, FS)
words_html = build_words_html(S, words, FS)

# Deco elements HTML
deco_elements = ""
dt = S["deco_type"]
if dt=="corner-shapes": deco_elements = '<div class="deco-tl"></div><div class="deco-br"></div>'
elif dt=="top-gradient-bar": deco_elements = '<div class="deco-bar"></div>'
elif dt=="side-stripe": deco_elements = '<div class="deco-side"></div>'
elif dt=="double-border": deco_elements = '<div class="deco-frame"></div>'
elif dt=="dot-pattern": deco_elements = '<div class="deco-dots"></div>'
elif dt=="diagonal-watermark": deco_elements = f'<div class="deco-watermark">{p_name[:15]}</div>'
elif dt=="bottom-accent": deco_elements = '<div class="deco-bottom"></div>'
elif dt=="circle-badge": deco_elements = '<div class="deco-circle">INV</div>'

full_css = f"""
* {{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; margin:0; padding:0; }}
@page {{ size:{pw}mm {ph}mm; margin:0; }}
body {{ background:#e8eaed; margin:0; padding:20px; font-family:{S['body_font']}; display:flex;flex-direction:column;align-items:center;min-height:100vh; }}
.wrap {{ transform:scale({ps}); transform-origin:top center; }}
.card {{ background:white;width:{pw}mm;min-height:{ph}mm;padding:{pad}mm;position:relative;overflow:hidden;display:flex;flex-direction:column; }}
{deco_css}
{table_css}
.billto {{ margin-bottom:18px; }}
.billto-label {{ font-family:{S['head_font']};font-size:{FS['label']}px;font-weight:700;color:{S['c1']};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:3px; }}
.billto-name {{ font-size:{int(FS['title']*0.65)}px;font-weight:700;color:#222;font-family:{S['head_font']}; }}
.billto-addr {{ white-space:pre-wrap;color:#555;line-height:1.4;font-size:{FS['small']}px;margin-top:2px; }}
.item-label {{ font-family:{S['head_font']};font-size:{FS['label']}px;font-weight:700;color:{S['c1']};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px;display:flex;align-items:center;gap:8px; }}
.item-count {{ background:{S['c4']};color:{S['c1']};font-size:{FS['xs']}px;padding:2px 8px;border-radius:10px;font-weight:600; }}
.print-btn {{ position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:999;background:{S['c1']};color:white;padding:14px 50px;border:none;border-radius:6px;font-weight:700;cursor:pointer;letter-spacing:1px;font-size:13px;box-shadow:0 4px 15px rgba(0,0,0,0.2);font-family:{S['head_font']}; }}
.print-btn:hover {{ filter:brightness(1.1); }}
@media print {{
    body {{ background:none;padding:0;display:block; }}
    .wrap {{ transform:none!important; }}
    .card {{ box-shadow:none;width:{pw}mm;min-height:{ph}mm; }}
    .print-btn {{ display:none!important; }}
}}
"""

invoice_body = f"""
{deco_elements}
{header_html}
<div class="billto">
    <div class="billto-label">Billed To</div>
    <div class="billto-name">{c_name}</div>
    <div class="billto-addr">{c_addr}</div>
</div>
<div class="item-label">Item Details <span class="item-count">{len(st.session_state.line_items)} items</span></div>
<table class="items-table">
    <thead><tr><th style="width:65%;">Description</th><th style="width:35%;">Amount (₹)</th></tr></thead>
    <tbody>{rows_html}</tbody>
</table>
{sum_html}
{words_html}
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;padding-top:10px;">
    <div>{sig_html}</div>
    <div>{total_html}</div>
</div>
"""

print_html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600;700&family=Outfit:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Sora:wght@400;600;700&family=Libre+Baskerville:wght@400;700&family=Cabinet+Grotesk:wght@400;700&family=Manrope:wght@400;600;700&family=Cormorant+Garamond:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700&family=Lora:wght@400;600;700&family=Bricolage+Grotesk:wght@400;700&family=EB+Garamond:wght@400;600;700&family=Geist:wght@400;700&family=Instrument+Serif:wght@400;700&family=Onest:wght@400;700&family=Fraunces:wght@400;700&family=Nunito+Sans:wght@400;600;700&family=Merriweather:wght@400;700&family=Figtree:wght@400;600;700&family=Bitter:wght@400;700&family=Supreme:wght@400;700&family=Newsreader:wght@400;700&family=General+Sans:wght@400;700&family=DM+Serif+Display:wght@400;700&family=Poppins:wght@400;600;700&family=Space+Mono:wght@400;700&family=Montserrat:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Roboto+Slab:wght@400;700&family=Work+Sans:wght@400;600;700&family=Literata:wght@400;700&family=Lexend:wght@400;600;700&family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
<style>{full_css}</style></head><body>
<div class="wrap"><div class="card">{invoice_body}</div></div>
<script>window.onload=function(){{window.print();}}</script>
</body></html>"""

preview_html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600;700&family=Outfit:wght@400;600;700&family=Crimson+Text:wght@400;600;700&family=Sora:wght@400;600;700&family=Libre+Baskerville:wght@400;700&family=Cabinet+Grotesk:wght@400;700&family=Manrope:wght@400;600;700&family=Cormorant+Garamond:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700&family=Lora:wght@400;600;700&family=Bricolage+Grotesk:wght@400;700&family=EB+Garamond:wght@400;600;700&family=Geist:wght@400;700&family=Instrument+Serif:wght@400;700&family=Onest:wght@400;700&family=Fraunces:wght@400;700&family=Nunito+Sans:wght@400;600;700&family=Merriweather:wght@400;700&family=Figtree:wght@400;600;700&family=Bitter:wght@400;700&family=Supreme:wght@400;700&family=Newsreader:wght@400;700&family=General+Sans:wght@400;700&family=DM+Serif+Display:wght@400;700&family=Poppins:wght@400;600;700&family=Space+Mono:wght@400;700&family=Montserrat:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&family=Roboto+Condensed:wght@400;700&family=Roboto+Slab:wght@400;700&family=Work+Sans:wght@400;600;700&family=Literata:wght@400;700&family=Lexend:wght@400;600;700&family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
<style>{full_css}.card{{box-shadow:0 4px 24px rgba(0,0,0,0.10);}}</style></head><body>
<div class="wrap"><div class="card">{invoice_body}</div></div>
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
