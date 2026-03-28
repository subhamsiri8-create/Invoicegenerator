import streamlit as st
import json
import os
from PIL import Image, ImageDraw, ImageFont

# --- SYSTEM SETTINGS ---
REGISTRY_FILE = "customer_registry.json"
DEFAULT_NAME = "VASAVI SILKS PRIVATE LIMITED"

st.set_page_config(page_title="DMM Ultra-Template System", layout="wide")

# --- SCALABLE TEMPLATE ENGINE ---
class TemplateEngine:
    @staticmethod
    def get_layout(template_id):
        """
        Logic to handle 60,000+ variations.
        Instead of 60k files, we use math to vary the design.
        """
        # Example: Change header color based on template ID
        colors = ["#1F618D", "#239B56", "#B03A2E", "#7D3C98", "#2E4053"]
        base_color = colors[template_id % len(colors)]
        
        # Shift layout positions based on ID
        offset = (template_id % 5) * 10 
        
        return {
            "primary_color": base_color,
            "header_y": 40 + offset,
            "table_start_y": 300 + offset
        }

# --- RENDERING CORE ---
def render_ultra_invoice(name, items, inv_no, date, template_id):
    layout = TemplateEngine.get_layout(template_id)
    img = Image.new('RGB', (827, 1169), 'white')
    draw = ImageDraw.Draw(img)
    
    # Dynamic Branding based on Template ID
    draw.rectangle([0, 0, 827, 120], fill=layout['primary_color'])
    draw.text((40, layout['header_y']), "AKULA DIVYA", fill="white")
    draw.text((350, layout['header_y']), "TAX INVOICE", fill="white")

    # Customer Data
    draw.text((40, 150), f"INVOICE #: {inv_no}", fill="black")
    draw.text((40, 170), f"DATE: {date}", fill="black")
    draw.text((500, 150), name, fill="black")
    draw.text((500, 170), "Visakhapatnam - 530013", fill="black")

    # Table
    y = layout['table_start_y']
    draw.line([40, y, 787, y], fill="black", width=2)
    draw.text((50, y+10), "Description", fill="black")
    draw.text((700, y+10), "Amount (₹)", fill="black")
    
    y += 50
    total = 0
    for item in items:
        draw.text((50, y), item['desc'], fill="black")
        draw.text((700, y), f"{item['price']:,}", fill="black")
        total += item['price']
        y += 40
        draw.line([40, y, 787, y], fill="#EBEDEF")

    # Total
    draw.text((50, 1000), f"TOTAL: ₹ {total:,.2f}", fill="black")
    draw.text((50, 1050), f"Template ID: {template_id}", fill="grey")
    
    return img

# --- STREAMLIT UI ---
st.title("🚀 DMM 60K Template Portal")

with st.sidebar:
    st.header("Template Controller")
    # You can now pick any number from 1 to 60,000
    tid = st.number_input("Select Template ID", min_value=1, max_value=60000, value=1)
    st.write(f"Currently viewing design variant #{tid}")

c_name = st.text_input("Customer Name", value=DEFAULT_NAME)
inv_no = st.text_input("Invoice Number", value="SEP/10/24-25")

# Item List
if 'item_count' not in st.session_state: st.session_state.item_count = 1
items = []
for i in range(st.session_state.item_count):
    cols = st.columns([4, 2])
    d = cols[0].text_input(f"Item {i+1}", value="Service Description", key=f"d{i}")
    p = cols[1].number_input(f"Price {i+1}", value=11000, key=f"p{i}")
    items.append({"desc": d, "price": p})

if st.button("➕ Add Item"):
    st.session_state.item_count += 1
    st.rerun()

if st.button("✨ Generate & Print"):
    invoice_img = render_ultra_invoice(c_name, items, inv_no, "18/09/2024", tid)
    st.image(invoice_img, use_container_width=True)
    
    invoice_img.save("output.png")
    with open("output.png", "rb") as f:
        st.download_button("📥 Download A4 PDF-Ready Image", f, "Invoice.png")
