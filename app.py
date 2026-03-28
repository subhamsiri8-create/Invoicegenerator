import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
DB_FILE = "customer_registry.json"
# Mapping your uploaded filenames to friendly names
TEMPLATES = {
    "Classic Portrait": "Ajay Seni.xlsx - Service Invoice 1.csv",
    "Modern Portrait": "Ajay Seni.xlsx - Service Invoice 2.csv",
    "Landscape Style 1": "Ajay Seni.xlsx - Service Invoice (Landscape) 1.csv",
    "Landscape Style 2": "Ajay Seni.xlsx - Service Invoice (Landscape) 2.csv"
}

st.set_page_config(page_title="DMM Invoice System", layout="wide")

# --- DATABASE LOGIC ---
def load_registry():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_registry(registry):
    with open(DB_FILE, 'w') as f: json.dump(registry, f)

# --- REALISTIC RENDERER ---
def render_invoice(customer, items, inv_no, inv_date):
    # A4 proportions: 827x1169 at 100DPI
    img = Image.new('RGB', (827, 1169), 'white')
    draw = ImageDraw.Draw(img)
    
    # Header Branding (Digital Marketing Mechanics)
    draw.rectangle([0, 0, 827, 120], fill="#1F618D")
    draw.text((40, 40), "DIGITAL MARKETING MECHANICS", fill="white")
    draw.text((650, 45), "INVOICE", fill="white")

    # Business Details
    draw.text((40, 150), "Eluru, Andhra Pradesh - 534002", fill="black")
    draw.text((600, 150), f"Invoice #: {inv_no}", fill="black")
    draw.text((600, 175), f"Date: {inv_date}", fill="black")

    # Customer "Bill To"
    draw.text((40, 230), "BILL TO:", fill="#7B7D7D")
    draw.text((40, 255), f"{customer['name']}", fill="black")
    draw.text((40, 280), f"{customer['address']}", fill="black")

    # Table Setup
    y = 400
    draw.rectangle([40, y, 787, y+40], fill="#F4F6F7")
    draw.text((60, y+12), "Description", fill="black")
    draw.text((600, y+12), "Qty", fill="black")
    draw.text((700, y+12), "Total (₹)", fill="black")

    # Item Logic
    y += 50
    grand_total = 0
    for item in items:
        if item['desc']:
            line_total = item['qty'] * item['price']
            grand_total += line_total
            draw.text((60, y), item['desc'], fill="black")
            draw.text((610, y), str(item['qty']), fill="black")
            draw.text((700, y), f"₹{line_total:,.2f}", fill="black")
            y += 40
            draw.line([40, y, 787, y], fill="#D5DBDB")
            y += 10
    
    # Grand Total Box
    draw.rectangle([550, y+20, 787, y+70], outline="#1F618D", width=2)
    draw.text((565, y+38), "TOTAL AMOUNT", fill="#1F618D")
    draw.text((700, y+38), f"₹{grand_total:,.2f}", fill="black")
    
    return img

# --- INTERFACE ---
st.title("💼 Realistic Agency Invoice Generator")
registry = load_registry()

with st.sidebar:
    st.header("Customer Profile")
    c_name = st.text_input("Customer Name", placeholder="e.g. Vasavi Silks")
    c_address = st.text_area("Customer Address")
    
    # Template Selection (Memorable)
    if c_name in registry:
        st.success(f"Recognized Customer! Using: {registry[c_name]}")
        selected_style = registry[c_name]
    else:
        selected_style = st.selectbox("Assign Template Style", list(TEMPLATES.keys()))

st.header("Invoice Items")
if 'item_rows' not in st.session_state:
    st.session_state.item_rows = 1

def add_row(): st.session_state.item_rows += 1

items = []
for i in range(st.session_state.item_rows):
    cols = st.columns([4, 1, 2])
    desc = cols[0].text_input("Description", key=f"desc_{i}")
    qty = cols[1].number_input("Qty", min_value=1, key=f"qty_{i}")
    price = cols[2].number_input("Price (₹)", key=f"price_{i}")
    items.append({"desc": desc, "qty": qty, "price": price})

st.button("➕ Add Item", on_click=add_row)

if st.button("🚀 Generate Realistic Invoice"):
    if not c_name:
        st.error("Please enter a Customer Name.")
    else:
        # Save customer allotment
        registry[c_name] = selected_style
        save_registry(registry)
        
        # Render
        customer_data = {"name": c_name, "address": c_address}
        final_img = render_invoice(customer_data, items, "INV-2026-001", date.today())
        
        # Show and Download
        st.image(final_img, caption="Final Print Preview", use_container_width=True)
        final_img.save("invoice_out.png")
        with open("invoice_out.png", "rb") as f:
            st.download_button("📥 Download to Print", f, "Invoice.png", "image/png")
