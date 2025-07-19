# camera_viewer.py

import cv2
import numpy as np

# Constants
CAMERA_COUNT = 4
FEED_WIDTH, FEED_HEIGHT = 320, 240
BUTTON_SIZE = 30

# Track enabled state
enabled = [True] * CAMERA_COUNT
cams = [cv2.VideoCapture(i) for i in range(CAMERA_COUNT)]

# Set resolution for all cameras
for cam in cams:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FEED_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FEED_HEIGHT)

def draw_toggle_button(frame, index):
    """Draw ON/OFF button in top-left corner"""
    color = (0, 255, 0) if enabled[index] else (0, 0, 255)
    text = "ON" if enabled[index] else "OFF"
    cv2.rectangle(frame, (0, 0), (BUTTON_SIZE, BUTTON_SIZE), color, -1)
    cv2.putText(frame, text, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def draw_monitor_number(frame, index):
    """Draw monitor number in top-right corner"""
    text = f"{index + 1}"
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
    text_x = FEED_WIDTH - text_size[0] - 10
    text_y = 30
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

def handle_click(event, x, y, flags, param):
    """Handle click on toggle buttons"""
    col = x // FEED_WIDTH
    row = y // FEED_HEIGHT
    cam_index = row * 2 + col
    if cam_index >= CAMERA_COUNT:
        return

    rel_x = x % FEED_WIDTH
    rel_y = y % FEED_HEIGHT

    if event == cv2.EVENT_LBUTTONDOWN:
        if rel_x < BUTTON_SIZE and rel_y < BUTTON_SIZE:
            enabled[cam_index] = not enabled[cam_index]

def get_camera_grid():
    """Return the full 2x2 grid image from camera feeds"""
    feeds = []
    for i in range(CAMERA_COUNT):
        if not enabled[i]:
            feeds.append(np.zeros((FEED_HEIGHT, FEED_WIDTH, 3), dtype=np.uint8))
            continue

        ret, frame = cams[i].read()
        if not ret:
            frame = np.zeros((FEED_HEIGHT, FEED_WIDTH, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (FEED_WIDTH, FEED_HEIGHT))

        draw_toggle_button(frame, i)
        draw_monitor_number(frame, i)
        feeds.append(frame)

    top = cv2.hconcat(feeds[:2])
    bottom = cv2.hconcat(feeds[2:])
    return cv2.vconcat([top, bottom])

def release_cameras():
    for cam in cams:
        cam.release()
