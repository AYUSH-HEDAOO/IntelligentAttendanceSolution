import requests
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

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
