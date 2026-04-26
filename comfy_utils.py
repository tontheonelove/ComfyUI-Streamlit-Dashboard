import json
import requests
import websocket
import uuid
import random

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def generate_ai_image_with_progress(prompt_text, seed, width, height, config):
    # 1. โหลด JSON ตามไฟล์ที่ระบุใน config
    workflow_path = config["file"]
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 2. ปรับแต่ง Prompt
    workflow[config["prompt_id"]]["inputs"]["text"] = prompt_text

    # 3. ปรับแต่ง Seed
    seed_key = config.get("seed_key", "seed")
    actual_seed = seed if seed != -1 else random.randint(1, 10**14)
    workflow[config["seed_id"]]["inputs"][seed_key] = actual_seed

    # 4. ปรับขนาดรูปภาพ (รองรับทั้งแบบ Latent Node เดียว และแบบแยก Width/Height Node)
    if "latent_id" in config:
        workflow[config["latent_id"]]["inputs"]["width"] = width
        workflow[config["latent_id"]]["inputs"]["height"] = height
    elif "width_id" in config and "height_id" in config:
        workflow[config["width_id"]]["inputs"]["value"] = width
        workflow[config["height_id"]]["inputs"]["value"] = height

    # 5. เชื่อมต่อ WebSocket
    ws = websocket.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

    # 6. ส่ง Prompt
    p = {"prompt": workflow, "client_id": client_id}
    response = requests.post(f"http://{server_address}/prompt", json=p).json()
    prompt_id = response['prompt_id']
    
    # 7. ฟังสถานะ Progress และ Node Status
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            
            # ส่งเปอร์เซ็นต์ความคืบหน้า
            if message['type'] == 'progress':
                data = message['data']
                yield {"status": "progress", "value": data['value'], "max": data['max']}
            
            # ส่งสถานะว่ากำลังรัน Node ไหนอยู่ (ดึงชื่อจาก _meta)
            if message['type'] == 'executing':
                node_id = message['data']['node']
                if node_id is not None:
                    node_title = workflow[node_id].get('_meta', {}).get('title', 'Processing...')
                    yield {"status": "node_status", "node_name": node_title}
                
                # เมื่อรันจบ
                if node_id is None and message['data']['prompt_id'] == prompt_id:
                    break
    
    # 8. ดึงรูปภาพกลับมา
    history = requests.get(f"http://{server_address}/history/{prompt_id}").json()
    output_images = []
    for node_id, node_output in history[prompt_id]['outputs'].items():
        for img in node_output.get('images', []):
            img_url = f"http://{server_address}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
            img_data = requests.get(img_url).content
            output_images.append(img_data)

    used_seed = workflow[config["seed_id"]]["inputs"][seed_key]
    yield {"status": "done", "images": output_images, "seed": used_seed}
    ws.close()