import os
import base64
import openai
from dotenv import load_dotenv

load_dotenv()

NRP_API_KEY = os.getenv("NRP_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = "https://llm.nrp-nautilus.io/v1"

if not NRP_API_KEY:
    raise RuntimeError("No NRP_API_KEY found. Please set it in your .env file.")

client = openai.OpenAI(
    api_key=NRP_API_KEY,
    base_url=BASE_URL
)

def frame_to_base64(frame):
    import cv2
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode()

def ask_ai_about_image(frame):
    img_b64 = frame_to_base64(frame)

    response = client.chat.completions.create(
        model="llava-onevision",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe what's in this image."},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}"}
                    }
                ]
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content
