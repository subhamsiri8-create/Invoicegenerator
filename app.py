import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# --- CONFIG & ASSETS ---
DB_FILE = "customer_mapping.json"
# Ensure these match the exact filenames you uploaded to GitHub
TEMPLATES = {
    "Service Style 1": "Ajay Seni.xlsx - Service Invoice 1.csv",
    "Service Style 2": "Ajay Seni.xlsx - Service Invoice 2.csv",
    "Landscape 1": "Ajay Seni.xlsx - Service Invoice (Landscape) 1.csv",
    "Landscape 2": "Ajay Seni.xlsx - Service Invoice (Landscape) 2.csv"
}

st.set_page_config(page_title="DMM Invoice Generator", layout="wide")

# --- DATA PERSISTENCE ---
def get_customer_style(c_name):
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
            return db.get(c_name)
    return None

def save_customer_style(c_name, style):
    db = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    db[c_name] = style
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

# --- ROBUST RENDERING ENGINE ---
def generate_fixed_invoice(customer, items, inv_no, inv_date):
    # A4 Canvas at 96 DPI
    img = Image.new('RGB', (800, 1100), 'white')
    draw = ImageDraw.Draw(img)
    
    # 1. Header & Brand
    draw.rectangle([0, 0, 800, 120], fill="#1F618D")
    draw.text((40, 45), "DIGITAL MARKETING MECHANICS", fill="white")
    draw.text((600, 45), "TAX INVOICE", fill="white")

    # 2. Invoice Meta
    draw.text((40, 140), "Eluru, Andhra Pradesh, 534002", fill="black")
    draw.text((600, 140), f"Invoice #: {inv_no}", fill="black")
    draw.text((600, 160), f"Date: {inv_date}", fill="black")

    # 3. Bill To
    draw.text((40, 220), "BILL TO:", fill="#566573")
    draw.text((40, 245), f"{customer['name']}", fill="black")
    draw.text((40, 265), f"{customer['address']}", fill="black")

    # 4. Table Header
    y = 380
    draw.rectangle([40, y, 760, y+35], fill="#EBEDEF")
    draw.text((55, y+10), "Description", fill="black")
    draw.text((500, y+10), "Qty", fill="black")
    draw.text((600, y+10), "Price (₹)", fill="black")
    draw.text((700, y+10), "Total", fill="black")

    # 5. Dynamic Items
    y += 45
    grand_total = 0
    for item in items:
        if item['desc']:
            line_total = item['qty'] * item['price']
            grand_total += line_total
            draw.text((55, y), item['desc'], fill="black")
            draw.text((510, y), str(item['qty']), fill="black")
            draw.text((600, y), f"{item['price']:,.2f}", fill="black")
            draw.text((700, y), f"{line_total:,.2f}", fill="black")
            y += 40
            draw.line([40, y, 760, y], fill="#D5DBDB")
            y += 10
    
    # 6. Total Box
    y += 20
    draw.rectangle([550, y, 760, y+50], outline="#1F618D", width=2)
    draw.text((565, y+18), "GRAND TOTAL", fill="#1F618D")
    draw.text((680, y+18), f"₹ {grand_total:,.2f}", fill="black")
    
    return img

# --- STREAMLIT UI ---
st.title("🇮🇳 Professional Indian Invoice Generator")
st.info("Assigns a fixed template to each customer and outputs print-ready files.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Step 1: Customer Details")
    name = st.text_input("Customer Name (e.g., Vasavi Silks)")
    addr = st.text_area("Address")
    
    # Check if customer already has a style
    saved_style = get_customer_style(name)
    if saved_style:
        st.success(f"Recognized Customer. Style: {saved_style}")
        current_style = saved_style
    else:
        current_style = st.selectbox("Assign Style for New Customer", list(TEMPLATES.keys()))

    st.header("Step 2: Invoice Items")
    inv_id = st.text_input("Invoice Number", value="DMM/2026/001")
    
    if 'rows' not in st.session_state: st.session_state.rows = 1
    
    item_list = []
    for i in range(st.session_state.rows):
        c = st.columns([3, 1, 2])
        d = c[0].text_input(f"Item {i+1}", key=f"d{i}")
        q = c[1].number_input("Qty", min_value=1, key=f"q{i}")
        p = c[2].number_input("Price (₹)", key=f"p{i}")
        item_list.append({"desc": d, "qty": q, "price": p})
    
    st.button("➕ Add Row", on_click=lambda: st.session_state.update({"rows": st.session_state.rows + 1}))

with col2:
    st.header("Step 3: Preview & Print")
    if st.button("🖼️ Generate Realistic Invoice"):
        if not name:
            st.warning("Please enter a customer name first.")
        else:
            save_customer_style(name, current_style)
            img_output = generate_fixed_invoice({"name": name, "address": addr}, item_list, inv_id, date.today())
            
            st.image(img_output, use_container_width=True)
            
            # Save to temporary file for download
            img_output.save("current_invoice.png")
            with open("current_invoice.png", "rb") as f:
                st.download_button("📥 Download to Print", f, file_name=f"{inv_id}.png", mime="image/png")
