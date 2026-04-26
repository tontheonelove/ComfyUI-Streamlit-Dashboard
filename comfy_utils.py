import json
import requests
import websocket
import uuid
import random

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

# เพิ่ม width และ height เป็นพารามิเตอร์
def generate_ai_image_with_progress(prompt_text, seed, width=1024, height=1024, workflow_file="image_z_image_turbo.json"):
    # 1. โหลด JSON
    with open(workflow_file, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 2. ปรับแต่งค่าพื้นฐาน
    workflow["57:27"]["inputs"]["text"] = prompt_text
    workflow["57:3"]["inputs"]["seed"] = seed if seed != -1 else random.randint(1, 10**9)

    # 3. ปรับขนาดรูปภาพ (ตรวจสอบ ID Node "Empty Latent Image" ใน JSON ของคุณอีกที)
    # สมมติว่าเป็น ID "5" ถ้าไม่ใช่ให้เปลี่ยนเลขตรง ["5"] เป็นเลขที่ถูกต้องครับ
    if "57:13" in workflow:
        workflow["57:13"]["inputs"]["width"] = width
        workflow["57:13"]["inputs"]["height"] = height

    # 4. เชื่อมต่อ WebSocket
    ws = websocket.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")

    # 5. ส่ง Prompt
    p = {"prompt": workflow, "client_id": client_id}
    response = requests.post(f"http://{server_address}/prompt", json=p).json()
    prompt_id = response['prompt_id']
    
    # 6. ฟังสถานะ Progress
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'progress':
                data = message['data']
                yield {"status": "progress", "value": data['value'], "max": data['max']}
            
            if message['type'] == 'executing':
                if message['data']['node'] is None and message['data']['prompt_id'] == prompt_id:
                    break
    
    # 7. ดึงรูปภาพกลับมา
    history = requests.get(f"http://{server_address}/history/{prompt_id}").json()
    output_images = []
    for node_id, node_output in history[prompt_id]['outputs'].items():
        for img in node_output.get('images', []):
            img_url = f"http://{server_address}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
            img_data = requests.get(img_url).content
            output_images.append(img_data)

    yield {"status": "done", "images": output_images, "seed": workflow["57:3"]["inputs"]["seed"]}
    ws.close()