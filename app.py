import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import date

# --- UI BRANDING & ANIMATIONS ---
def inject_ui():
    st.markdown("""
        <style>
        .stApp {
            background: radial-gradient(circle at top left, #0d1117, #161b22);
            color: #c9d1d9;
        }
        @keyframes slideUp {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .main .block-container { animation: slideUp 0.6s ease-out; }
        
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #1f618d, #2874a6);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 15px;
            font-weight: bold;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# --- THE 50,000 TEMPLATE GENERATOR ---
class InvoiceGenerator:
    @staticmethod
    def get_template_config(tid):
        """Generates unique styles for 50,000 variants mathematically"""
        colors = ["#1f618d", "#239b56", "#b03a2e", "#7d3c98", "#2e4053", "#d35400"]
        return {
            "main_color": colors[tid % len(colors)],
            "header_height": 100 + (tid % 50),
            "font_size": 20 + (tid % 5),
            "border_width": 1 + (tid % 3)
        }

    @staticmethod
    def create_pdf_ready_image(data, tid):
        conf = InvoiceGenerator.get_template_config(tid)
        img = Image.new('RGB', (827, 1169), 'white')
        draw = ImageDraw.Draw(img)
        
        # Header - Parametric Design
        draw.rectangle([0, 0, 827, conf['header_height']], fill=conf['main_color'])
        draw.text((40, 40), "AJAY SENI", fill="white")
        draw.text((650, 40), "INVOICE", fill="white")

        # Client Info (Default: Vasavi Silks)
        draw.text((50, 200), f"BILL TO: {data['name']}", fill="black")
        draw.text((50, 230), data['addr'], fill="black")
        
        # Meta Info
        draw.text((550, 200), f"INVOICE #: {data['inv_no']}", fill="black")
        draw.text((550, 230), f"DATE: {data['date']}", fill="black")

        # Table Grid
        y_start = 350
        draw.line([50, y_start, 777, y_start], fill="black", width=conf['border_width'])
        draw.text((60, y_start+10), "DESCRIPTION", fill="black")
        draw.text((650, y_start+10), "AMOUNT (₹)", fill="black")
        
        y = y_start + 50
        total = 0
        for item in data['items']:
            draw.text((60, y), item['desc'], fill="black")
            draw.text((650, y), f"{item['amt']:,}", fill="black")
            total += item['amt']
            y += 45
            draw.line([50, y, 777, y], fill="#dddddd")

        # Final Total
        draw.rectangle([50, 1000, 777, 1060], outline="black", width=2)
        draw.text((70, 1015), "TOTAL PAYABLE", fill="black")
        draw.text((630, 1015), f"₹ {total:,.2f}", fill="black")

        return img

# --- DASHBOARD UI ---
inject_ui()
st.title("🚀 AJAY SENI: 50K Template Portal")

with st.sidebar:
    st.header("Template Selector")
    tid = st.number_input("Select Template ID (1 - 50,000)", min_value=1, max_value=50000, value=1)
    st.info(f"Using Layout Configuration #{tid}")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Customer", value="VASAVI SILKS PRIVATE LIMITED")
    addr = st.text_area("Address", value="Edaravari Street, Eluru – 534002")
with col2:
    inv_no = st.text_input("Invoice #", value="SEP/10/24-25")
    inv_date = st.text_input("Date", value="18/09/2024")

st.subheader("🛒 Line Items")
if 'rows' not in st.session_state: st.session_state.rows = 1
items = []
for i in range(st.session_state.rows):
    r = st.columns([3, 1])
    d = r[0].text_input(f"Service {i+1}", key=f"d{i}", value="Influencer Store Explore")
    a = r[1].number_input(f"Amount", key=f"a{i}", value=11000)
    items.append({"desc": d, "amt": a})

if st.button("＋ Add Row"):
    st.session_state.rows += 1
    st.rerun()

if st.button("✨ GENERATE & PRINT"):
    payload = {"name": name, "addr": addr, "inv_no": inv_no, "date": inv_date, "items": items}
    final_img = InvoiceGenerator.create_pdf_ready_image(payload, tid)
    
    st.image(final_img, caption=f"Template #{tid} Preview", use_container_width=True)
    
    final_img.save("invoice_out.png")
    with open("invoice_out.png", "rb") as f:
        st.download_button("📥 Download Print File", f, file_name=f"{inv_no}_T{tid}.png")
