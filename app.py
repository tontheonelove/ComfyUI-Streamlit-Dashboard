import streamlit as st
from comfy_utils import generate_ai_image_with_progress

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Z-Image Pro Studio", layout="wide", page_icon="🚀")

# 2. Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { border-radius: 15px; border: 1px solid #30363d; }
    .stButton button { width: 100%; border-radius: 12px; font-weight: bold; height: 3rem; background: linear-gradient(45deg, #2ecc71, #27ae60); border: none; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Connection Settings ---
with st.sidebar:
    st.title("🌐 Server Settings")
    cloud_mode = st.toggle("Enable Cloud Mode (RunPod)", value=False)
    
    if cloud_mode:
        # ใส่ URL RunPod ของคุณที่นี่ (แนะนำให้ใส่ค่าเริ่มต้นไว้เลย)
        runpod_url = st.text_input("RunPod URL", "xxxxxxxxx-8188.proxy.runpod.net")
        active_url = runpod_url.replace("https://", "").replace("http://", "").strip("/")
        st.info("☁️ Status: Connected to Cloud")
    else:
        active_url = "127.0.0.1:8188"
        st.success("🏠 Status: Connected Locally")

# --- HEADER SECTION ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.title("🚀 AI Studio WebUI")
    st.caption("Advanced AI Generation Dashboard | Powered by TON LIKE IT ❤️")

with col_t2:
    status_label = "Cloud GPU" if cloud_mode else "Local GPU"
    st.metric(label=status_label, value="Ready", delta="Online")

st.divider()

# --- CONFIGURATION ---
WORKFLOW_SETTINGS = {
    "Z-Image Turbo": {
        "file": "workflow/image_z_image_turbo_runpod.json",
        "prompt_id": "57:27",
        "seed_id": "57:3",
        "latent_id": "57:13"
    },
    "Flux 2 Klein": {
        "file": "workflow/image_flux2_text_to_image_9b.json",
        "prompt_id": "75:74",               
        "seed_id": "75:73",                
        "width_id": "75:68",               
        "height_id": "75:69",               
        "seed_key": "noise_seed"         
    }
}

# --- MAIN DASHBOARD ---
col_input, col_display = st.columns([1, 2], gap="large")

with col_input:
    with st.container(border=True):
        st.subheader("⌨️ ใส่ PROMPT เพื่อสร้างรูป")
        selected_model = st.selectbox("Select AI Model", list(WORKFLOW_SETTINGS.keys()))
        current_config = WORKFLOW_SETTINGS[selected_model]
        prompt = st.text_area("Positive Prompt", "A young woman in a sunlit room...", height=150)
        
        with st.expander("🛠️ Advanced Settings", expanded=True):
            seed = st.number_input("Seed", value=-1, help="-1 for random")
            size_option = st.selectbox(
                "Select Aspect Ratio", 
                ["1024x1024 (Square)", "720x1280 (Portrait)", "1280x720 (Landscape)", "1920x1080 (FHD)"]
            )
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
        
        if generate_btn:
            with st.status(f"🚀 Initializing {selected_model}...", expanded=True) as status:
                status_text = st.empty()
                prog_bar = st.progress(0)
                
                try:
                    current_node = "Starting..."
                    
                    # ส่ง active_url และ cloud_mode เข้าไปในฟังก์ชัน
                    for res in generate_ai_image_with_progress(
                        prompt, seed, target_width, target_height, current_config, active_url, cloud_mode
                    ):
                        if res['status'] == 'node_status':
                            current_node = res['node_name']
                            status.update(label=f"Running: {current_node}...", state="running")
                            status_text.markdown(f"🔍 **Current Step:** `{current_node}`")
                        
                        if res['status'] == 'progress':
                            val = int((res['value'] / res['max']) * 100)
                            prog_bar.progress(val)
                            status_text.markdown(f"🔍 **Current Step:** `{current_node}` (**{val}%**)")
                        
                        if res['status'] == 'done':
                            status.update(label="Generation Complete!", state="complete", expanded=False)
                            status_text.empty()
                            prog_bar.empty()
                            st.toast("Success!", icon="🎨")
                            
                            for img in res['images']:
                                res_placeholder.image(img, use_container_width=False, width=600)
                                st.download_button(
                                    label="📥 Download Image", 
                                    data=img, 
                                    file_name=f"{selected_model}_{res['seed']}.png", 
                                    mime="image/png"
                                )
                except Exception as e:
                    status.update(label="System Error", state="error")
                    st.error(f"Error: {e}")
        else:
            res_placeholder.info(f"Model: {selected_model} is ready. Press Generate to start.")