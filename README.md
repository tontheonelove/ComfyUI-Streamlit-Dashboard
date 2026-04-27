# ComfyUI-Streamlit-Dashboard

<img width="2466" height="1175" alt="image" src="https://github.com/user-attachments/assets/b6d2aef9-85b1-43aa-8e05-894ed590df7f" />


## Update 🚀🚀 (26-4-26)

🚀 Support Model  Z-Image Turbo , Flux2. Klein9B

## ✨ Key Features

✅Intuitive Dashboard UI: A clean, two-column layout designed for a distraction-free creative process.

✅Real-time Progress Tracking: Live WebSocket integration to monitor generation progress step-by-step.

✅Dynamic Aspect Ratio Selector: Easily switch between Square (1:1), Portrait (9:16), Landscape (16:9), and FHD (1080p).

✅Advanced Parameter Control: Fine-tune Seeds and prompts with a persistent session state that remembers your last masterpiece.

✅One-Click Download: Instantly save your generated high-resolution images.

✅Support Computer / Ipad / Mobile UI


## 🛠️ Local Installation
1. Clone the Repository:

```
git clone https://github.com/tontheonelove/ComfyUI-Streamlit-Dashboard
cd ComfyUI-Streamlit-Dashboard
```

2. Install Dependencies:
Make sure you have Python 3.10+ installed.
```
pip install -r requirements.txt
```
3. Prepare ComfyUI:

    - Ensure ComfyUI is running locally (default: 127.0.0.1:8188).

    - Load the provided yourworkflow.json  workflow into your ComfyUI to ensure all custom nodes are present.

4. Run the App:

```
streamlit run app.py
```


## 🌐 Deploying to Production (Public Server)

To access your dashboard from anywhere, use a Cloudflare Tunnel to securely expose your local Streamlit port (8501) without opening router ports:

1. Install cloudflared.

2. Run the tunnel:

```
cloudflared tunnel --url http://localhost:8501
```

3. Access the provided .trycloudflare.com URL on your mobile or remote device.



## ☁️ Running on RunPod / Cloud GPU

If you don't have a local GPU , you can run this on RunPod:

1. Deploy a ComfyUI Pod: Use the official ComfyUI template.

2. Expose Ports: Ensure ports 8188 (ComfyUI) and 8501 (Streamlit) are exposed in the Pod settings.

3. Update comfy_utils.py:
 
Change server_address from 127.0.0.1:8188 to your RunPod's public IP/Proxy address.

4. Launch: Open the web terminal and run streamlit run app.py --server.port 8501.










