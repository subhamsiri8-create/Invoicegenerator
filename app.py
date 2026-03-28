import streamlit as st
from PIL import Image, ImageDraw
import os

# --- UI BRANDING ---
def apply_branding():
    st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top left, #0d1117, #161b22); color: #c9d1d9; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .main .block-container { animation: fadeIn 1s; }
        
        /* Custom Card for Customer Entry */
        .customer-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #30363d;
            margin-bottom: 20px;
        }
        
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: white; border: none; padding: 12px; border-radius: 8px; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CUSTOMER DATABASE ---
# You can add more customers to this list easily
CUSTOMERS = {
    "VASAVI SILKS PRIVATE LIMITED": {
        "address": "Edaravari Street, Eluru – 534002",
        "contact": "Phone 9246663443 | accounts@vasavisilks.com",
        "location": "Visakhapatnam - 530013"
    },
    "SUBHAM GRAND": {
        "address": "GNT Road, Near Karra Vantena, Eluru",
        "contact": "Phone 9550538336",
        "location": "Eluru"
    },
    "SIRI DRESS DIVINE": {
        "address": "Main Road, Kakinada",
        "contact": "Manager: 9988776655",
        "location": "Kakinada"
    }
}

def render_invoice(cust_data, inv_meta, items):
    img = Image.new('RGB', (827, 1169), 'white')
    draw = ImageDraw.Draw(img)
    
    # AJAY SENI BRANDING
    draw.text((600, 50), "AJAY SENI", fill="black")
    draw.text((350, 50), "INVOICE", fill="black")

    # Dynamic "Bill To" Section
    draw.text((50, 120), f"INVOICE NO : {inv_meta['no']}", fill="black")
    draw.text((320, 120), f"DATE : {inv_meta['date']}", fill="black")
    draw.text((550, 120), cust_data['name'], fill="black")
    draw.text((550, 140), cust_data['location'], fill="black")

    draw.text((50, 160), cust_data['address'], fill="black")
    draw.text((50, 180), cust_data['contact'], fill="black")

    # Table Setup
    draw.rectangle([50, 250, 777, 290], fill="#f4f4f4", outline="black")
    draw.text((65, 262), "Description", fill="black")
    draw.text((680, 262), "Amount (₹)", fill="black")

    y, total = 310, 0
    for item in items:
        draw.text((65, y), item['desc'], fill="black")
        draw.text((680, y), f"{item['amt']:,}", fill="black")
        total += item['amt']
        y += 45
        draw.line([50, y-5, 777, y-5], fill="#eeeeee")

    # Grand Total
    draw.rectangle([50, 950, 777, 1000], outline="black", width=2)
    draw.text((65, 965), "TOTAL AMOUNT PAYABLE", fill="black")
    draw.text((650, 965), f"₹ {total:,.2f}", fill="black")
    
    return img

# --- APP INTERFACE ---
apply_branding()
st.title("💠 AJAY SENI | Smart Billing")

# 1. CUSTOMER SELECTION
st.subheader("👥 Select Customer")
selected_cust = st.selectbox("Choose from database", options=list(CUSTOMERS.keys()))

# Auto-fill logic
cust_info = CUSTOMERS[selected_cust]

with st.container():
    st.markdown('<div class="customer-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        final_name = st.text_input("Billing Name", value=selected_cust)
        final_addr = st.text_area("Address", value=cust_info['address'])
    with c2:
        final_loc = st.text_input("City/Location", value=cust_info['location'])
        final_contact = st.text_input("Contact Details", value=cust_info['contact'])
    st.markdown('</div>', unsafe_allow_html=True)

# 2. INVOICE META
st.subheader("📅 Invoice Details")
m1, m2 = st.columns(2)
inv_no = m1.text_input("Invoice #", value="OCT-15/24-25")
inv_date = m2.text_input("Date", value="18/09/2024")

# 3. LINE ITEMS
st.subheader("💼 Services")
if 'rows' not in st.session_state: st.session_state.rows = 1
items = []
for i in range(st.session_state.rows):
    r = st.columns([3, 1])
    d = r[0].text_input(f"Service {i+1}", key=f"d{i}", value="Influencer Store Explore")
    a = r[1].number_input(f"Price", key=f"a{i}", value=50000)
    items.append({"desc": d, "amt": a})

if st.button("➕ Add Another Service"):
    st.session_state.rows += 1
    st.rerun()

st.divider()

if st.button("🚀 GENERATE PROFESSIONAL INVOICE"):
    cust_payload = {"name": final_name, "address": final_addr, "location": final_loc, "contact": final_contact}
    meta_payload = {"no": inv_no, "date": inv_date}
    
    final_img = render_invoice(cust_payload, meta_payload, items)
    st.image(final_img, caption="Professional Preview", use_container_width=True)
    
    final_img.save("invoice.png")
    with open("invoice.png", "rb") as f:
        st.download_button("📥 Download Print File", f, file_name=f"{inv_no}.png")
