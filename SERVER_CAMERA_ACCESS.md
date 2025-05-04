Let me walk you through this **"local proxy server + SSH tunnel"** solution step-by-step. It's a neat and reliable way to make your local Wi-Fi camera accessible from your EC2 instance.
---

## ✅ Goal

You’ll:

1. Run a **FastAPI proxy** on your **local machine**.
2. Fetch camera snapshots via `http://192.168.252.100/640x480.jpg`.
3. Expose this local proxy to your **EC2 instance** using **SSH tunneling**.
4. On the EC2, access the camera like:
   ```
   http://localhost:9000/proxy-image
   ```

---

## 🧠 Why Do This?

Because the **camera is on your private local network**, AWS can’t see it directly. But your **local PC can**, and we’re just asking your PC to fetch the image and **forward it over SSH** like a middleman.

---

## 🛠️ Step-by-Step Guide

---

### 1. 🔧 Set up a FastAPI Proxy Server on Your Local Machine

```bash
pip install fastapi uvicorn requests
```

Then, create a file called `camera_proxy.py`:

```python
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()

CAMERA_IP = "192.168.252.100"

@app.get("/proxy-image")
def get_image():
    camera_url = f"http://{CAMERA_IP}/640x480.jpg"
    try:
        resp = requests.get(camera_url, stream=True, timeout=5)
        return StreamingResponse(resp.raw, media_type="image/jpeg")
    except Exception as e:
        return Response(content=f"Error fetching image: {str(e)}", status_code=500)
```

Run it:

```bash
uvicorn camera_proxy:app --host 127.0.0.1 --port 8000
```

Check it in your browser or with `curl`:

```bash
curl http://127.0.0.1:8000/proxy-image
```

If your camera is working on your local machine, this will show the image.

---

### 2. 🔐 Create SSH Reverse Tunnel to EC2

Now expose this local FastAPI server to EC2:

```bash
ssh -i your-key.pem -N -R 9000:localhost:8000 ubuntu@your-ec2-public-ip
```

- `-R 9000:localhost:8000`: Maps port 9000 on EC2 → port 8000 on your local machine
- `-N`: Don’t start a shell
- `-i`: SSH key for EC2
- `ubuntu@...`: EC2 login

✅ Once connected, EC2 can access `http://localhost:9000/proxy-image`

---

### 3. 🚀 From Your EC2 App Server

Now just change your `image_url` in EC2 to:

```python
image_url = "http://localhost:9000/proxy-image"
```

This will:
- Call EC2 `localhost:9000`
- Which tunnels to your local FastAPI server
- Which fetches from your camera
- And sends the image back!

---

## ✅ Advantages

- Secure (tunnel only runs when you start it)
- No need to open ports or expose your home network
- Easily debug locally

---

## 🔁 Optional: Make Tunnel Persistent

You can use `autossh` or a systemd service to keep the tunnel always alive if needed.
