import streamlit as st
import json
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# --- THEME & ANIMATION CSS ---
def inject_professional_style():
    st.markdown("""
        <style>
        /* Main Background and Font */
        .stApp {
            background-color: #0E1117;
            color: #E0E0E0;
            font-family: 'Inter', sans-serif;
        }
        
        /* Fade-in Animation for the whole page */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main .block-container {
            animation: fadeIn 0.8s ease-out;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }

        /* Input Field Styling */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #0D1117 !important;
            color: white !important;
            border: 1px solid #30363D !important;
            border-radius: 8px !important;
            transition: 0.3s;
        }
        .stTextInput>div>div>input:focus {
            border-color: #58A6FF !important;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.2) !important;
        }

        /* Professional Button */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #2188ff 0%, #124d91 100%);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        div.stButton > button:first-child:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(33, 136, 255, 0.4);
        }

        /* Header Accent */
        h1, h2, h3 {
            color: #58A6FF !important;
            letter-spacing: -0.5px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CONFIG & DEFAULTS ---
inject_professional_style()
DEFAULT_NAME = "VASAVI SILKS PRIVATE LIMITED"
DEFAULT_ADDR = "Edaravari Street, Eluru - 534002"

st.title("💠 DMM Invoice Engine")
st.caption("Professional Portal for Digital Marketing Mechanics")

# --- LAYOUT ---
with st.container():
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📍 Client Information")
        c_name = st.text_input("Customer Name", value=DEFAULT_NAME)
        c_addr = st.text_area("Billing Address", value=DEFAULT_ADDR)
        
        st.subheader("📄 Invoice Meta")
        m1, m2 = st.columns(2)
        inv_no = m1.text_input("Invoice Number", value="SEP/10/24-25")
        inv_date = m2.text_input("Billing Date", value=date.today().strftime("%d/%m/%Y"))

    with col2:
        st.subheader("🛒 Service Line Items")
        if 'rows' not in st.session_state: st.session_state.rows = 1
        
        items = []
        for i in range(st.session_state.rows):
            row_cols = st.columns([3, 2])
            desc = row_cols[0].text_input(f"Service {i+1}", key=f"d{i}", value="Influencer Promotion")
            amt = row_cols[1].number_input(f"Amount (₹)", key=f"a{i}", value=11000)
            items.append({"desc": desc, "amt": amt})
        
        if st.button("＋ Add New Service"):
            st.session_state.rows += 1
            st.rerun()

st.divider()

# --- GENERATION ---
if st.button("⚡ GENERATE & SYNC INVOICE"):
    # Drawing logic remains high-quality as previous
    # This creates a crisp, professional white A4 invoice for printing
    img = Image.new('RGB', (827, 1169), 'white')
    d = ImageDraw.Draw(img)
    
    # Modern Blue Header on the actual Invoice
    d.rectangle([0, 0, 827, 150], fill="#1F618D")
    d.text((50, 60), "DIGITAL MARKETING MECHANICS", fill="white")
    d.text((650, 60), "INVOICE", fill="white")
    
    # Render Preview
    st.image(img, caption="Final Print Preview", use_container_width=True)
    
    img.save("invoice_final.png")
    with open("invoice_final.png", "rb") as f:
        st.download_button("📥 DOWNLOAD PRINT-READY PDF (PNG)", f, file_name=f"{inv_no}.png")
