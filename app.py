import streamlit as st
from comfy_utils import generate_ai_image_with_progress

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Z-Image Pro Dashboard", layout="wide", page_icon="🚀")

# 2. Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { border-radius: 15px; border: 1px solid #30363d; }
    .stButton button { width: 100%; border-radius: 12px; font-weight: bold; height: 3rem; background: linear-gradient(45deg, #2ecc71, #27ae60); border: none; }
    .css-1r6slb0 { border-radius: 20px; border: 1px solid #30363d; padding: 20px; background-color: #161b22; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.title("🚀 Z-Image Pro Studio")
    st.caption("Advanced AI Generation Dashboard | Powered by TON LIKE IT ❤️")

with col_t2:
    st.metric(label="GPU Status", value="Ready", delta="Online")

st.divider()

# --- MAIN DASHBOARD ---
col_input, col_display = st.columns([1, 2], gap="large")

with col_input:
    with st.container(border=True):
        st.subheader("⌨️ ใส่ Prompt เพื่อสร้างรูปได้เลย")
        prompt = st.text_area("Positive Prompt", "A young woman in a sunlit room...", height=200)
        
        with st.expander("🛠️ Advanced Settings", expanded=True):
            seed = st.number_input("Seed", value=-1, help="-1 for random")
            
            # 1. เพิ่มตัวเลือกขนาดรูปภาพ
            size_option = st.selectbox(
                "Select Aspect Ratio", 
                ["1024x1024 (Square)", "720x1280 (Portrait)", "1280x720 (Landscape)", "1920x1080 (FHD)"]
            )
            
            # 2. สร้างระบบ Map ค่าข้อความไปเป็นตัวเลข (Width, Height)
            size_map = {
                "1024x1024 (Square)": (1024, 1024),
                "720x1280 (Portrait)": (720, 1280),
                "1280x720 (Landscape)": (1280, 720),
                "1920x1080 (FHD)": (1920, 1080)
            }
            target_width, target_height = size_map[size_option]
        
        generate_btn = st.button("✨ Generate Masterpiece")

with col_display:
    with st.container(border=True):
        res_placeholder = st.empty()
        prog_placeholder = st.empty()
        
        if generate_btn:
            try:
                # 3. ส่งค่า width และ height เข้าไปในฟังก์ชันด้วย
                for res in generate_ai_image_with_progress(prompt, seed, width=target_width, height=target_height):
                    if res['status'] == 'progress':
                        val = int((res['value'] / res['max']) * 100)
                        prog_placeholder.progress(val, text=f"Processing... {val}%")
                    
                    if res['status'] == 'done':
                        prog_placeholder.empty()
                        st.toast("Generation Complete!", icon="🎨")
                        
                        for img in res['images']:
                            res_placeholder.image(img, use_container_width=False, width=600)
                            st.download_button("📥 Download Image", img, file_name=f"ai_art_{target_width}x{target_height}.png", mime="image/png")
            except Exception as e:
                st.error(f"Connection Error: {e}")
        else:
            res_placeholder.info("Ready for your prompt. Press Generate to start.")