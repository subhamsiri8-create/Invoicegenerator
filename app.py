import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
ST_PAGE_TITLE = "DMM Invoice System"
DB_FILE = "customer_mapping.json"
TEMPLATES = {
    "Classic Portrait": "Ajay Seni.xlsx - Service Invoice 1.csv",
    "Modern Portrait": "Ajay Seni.xlsx - Service Invoice 2.csv",
    "Landscape Style 1": "Ajay Seni.xlsx - Service Invoice (Landscape) 1.csv",
    "Landscape Style 2": "Ajay Seni.xlsx - Service Invoice (Landscape) 2.csv"
}

st.set_page_config(page_title=ST_PAGE_TITLE, layout="wide")

# --- DATABASE LOGIC ---
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

# --- INVOICE GENERATOR LOGIC ---
def generate_realistic_invoice(customer, items, inv_no, inv_date, template_path):
    # Create A4 Canvas
    img = Image.new('RGB', (800, 1100), 'white')
    draw = ImageDraw.Draw(img)
    
    # Header Branding
    draw.rectangle([0, 0, 800, 100], fill="#1A5276")
    draw.text((40, 35), "DIGITAL MARKETING MECHANICS", fill="white")
    draw.text((650, 40), "INVOICE", fill="white")

    # Details
    draw.text((40, 130), "Eluru, Andhra Pradesh, 534002", fill="black")
    draw.text((600, 130), f"Invoice #: {inv_no}", fill="black")
    draw.text((600, 150), f"Date: {inv_date}", fill="black")

    # Customer
    draw.text((40, 200), "BILL TO:", fill="grey")
    draw.text((40, 220), f"{customer['name']}", fill="black")
    draw.text((40, 240), f"{customer['address']}", fill="black")

    # Table Header
    y = 350
    draw.rectangle([40, y, 760, y+30], fill="#F2F4F4")
    draw.text((50, y+8), "Description", fill="black")
    draw.text((600, y+8), "Price (₹)", fill="black")
    draw.text((700, y+8), "Total", fill="black")

    # Logic for Items
    y += 40
    total = 0
    for item in items:
        line_total = item['qty'] * item['price']
        total += line_total
        draw.text((50, y), item['desc'], fill="black")
        draw.text((600, y), f"{item['price']}", fill="black")
        draw.text((700, y), f"{line_total}", fill="black")
        y += 35
        draw.line([40, y, 760, y], fill="#D5DBDB")
    
    # Grand Total
    y += 40
    draw.rectangle([550, y, 760, y+40], outline="black", width=2)
    draw.text((560, y+12), "GRAND TOTAL", fill="black")
    draw.text((670, y+12), f"₹ {total:,.2f}", fill="black")
    
    return img

# --- STREAMLIT UI ---
st.title("🚀 Professional Invoice Generator")
st.subheader("Realistic Output | Indian Rupee | Zero GST")

db = load_db()

with st.sidebar:
    st.header("1. Customer Details")
    c_id = st.text_input("Customer ID (Unique)", placeholder="e.g. CUST001")
    c_name = st.text_input("Name")
    c_address = st.text_area("Address")
    
    # Automatic Template Allotment
    if c_id in db:
        st.info(f"Existing Customer. Style: {db[c_id]}")
        selected_template = db[c_id]
    else:
        selected_template = st.selectbox("Assign Template Style", list(TEMPLATES.keys()))

col1, col2 = st.columns([1, 1])

with col1:
    st.header("2. Invoice Items")
    inv_no = st.text_input("Invoice #", value="DMM-2026-001")
    inv_date = st.date_input("Invoice Date", value=date.today())
    
    # Dynamic Item Entry
    if 'items' not in st.session_state:
        st.session_state.items = [{"desc": "", "qty": 1, "price": 0}]

    def add_item():
        st.session_state.items.append({"desc": "", "qty": 1, "price": 0})

    for i, item in enumerate(st.session_state.items):
        cols = st.columns([3, 1, 2])
        st.session_state.items[i]['desc'] = cols[0].text_input(f"Item {i+1}", value=item['desc'], key=f"d{i}")
        st.session_state.items[i]['qty'] = cols[1].number_input("Qty", value=item['qty'], key=f"q{i}")
        st.session_state.items[i]['price'] = cols[2].number_input("Price (₹)", value=item['price'], key=f"p{i}")

    st.button("➕ Add Another Item", on_click=add_item)

with col2:
    st.header("3. Realistic Preview")
    if st.button("✨ Generate & Save Customer Style"):
        if not c_id:
            st.error("Please enter a Customer ID")
        else:
            db[c_id] = selected_template
            save_db(db)
            
            customer_data = {"name": c_name, "address": c_address}
            img = generate_realistic_invoice(customer_data, st.session_state.items, inv_no, inv_date, TEMPLATES[selected_template])
            
            st.image(img, use_container_width=True, caption="Generated Invoice Preview")
            
            # Save and Download
            img.save("temp_invoice.png")
            with open("temp_invoice.png", "rb") as file:
                st.download_button(
                    label="📥 Download Invoice for Printing",
                    data=file,
                    file_name=f"Invoice_{inv_no}.png",
                    mime="image/png"
                )
            st.success("Invoice generated! Use the button above to download and print.")
