# ai_manager.py

from vision_ai import ask_ai_about_image
from camera_viewer import get_camera_grid
import numpy as np

# AI instance placeholders (could later become persistent context agents)
def get_camera_frame(cam_id):
    """Return a cropped section of the camera grid for the given camera ID (1–4)"""
    full_grid = get_camera_grid()
    h, w, _ = full_grid.shape
    cam_w, cam_h = w // 2, h // 2

    positions = {
        1: (0, 0),
        2: (0, cam_w),
        3: (cam_h, 0),
        4: (cam_h, cam_w)
    }

    y, x = positions.get(cam_id, (0, 0))
    return full_grid[y:y+cam_h, x:x+cam_w]

def query_camera_ai(cam_id):
    """Send the camera feed for cam_id to the respective AI"""
    frame = get_camera_frame(cam_id)
    try:
        print(f"🔍 Querying AI for camera {cam_id}...")
        response = ask_ai_about_image(frame)
        return f"[Camera {cam_id}] {response}"
    except Exception as e:
        return f"[Camera {cam_id}] ❌ AI error: {e}"

def query_interface_ai(prompt):
    """Very basic routing logic"""
    prompt = prompt.lower()

    if "camera" in prompt:
        for i in range(1, 5):
            if f"{i}" in prompt or f"camera {i}" in prompt:
                return query_camera_ai(i)

    return "(Interface AI): I'm not sure which camera you mean. Try 'What do you see on camera 1?'"
