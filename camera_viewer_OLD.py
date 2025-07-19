import cv2
import numpy as np
import time
from vision_ai import ask_ai_about_image  # ✅ FIXED

# Constants
CAMERA_COUNT = 4
FEED_WIDTH, FEED_HEIGHT = 320, 240
BUTTON_SIZE = 30
WINDOW_NAME = "Camera Grid"

# Track enabled state per camera
enabled = [True for _ in range(CAMERA_COUNT)]
last_ai_check = time.time()
ai_interval = 5  # seconds

# Initialize cameras
cams = [cv2.VideoCapture(i) for i in range(CAMERA_COUNT)]

# Set resolution
for cam in cams:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FEED_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FEED_HEIGHT)

def draw_button(frame, index):
    color = (0, 255, 0) if enabled[index] else (0, 0, 255)
    text = "ON" if enabled[index] else "OFF"
    cv2.rectangle(frame, (0, 0), (BUTTON_SIZE, BUTTON_SIZE), color, -1)
    cv2.putText(frame, text, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

def mouse_callback(event, x, y, flags, param):
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

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

while True:
    feeds = []
    ai_frame = None

    for i in range(CAMERA_COUNT):
        if not enabled[i]:
            feeds.append(np.zeros((FEED_HEIGHT, FEED_WIDTH, 3), dtype=np.uint8))
            continue

        ret, frame = cams[i].read()
        if not ret:
            frame = np.zeros((FEED_HEIGHT, FEED_WIDTH, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (FEED_WIDTH, FEED_HEIGHT))

        if i == 0:
            ai_frame = frame.copy()  # Save for AI processing

        draw_button(frame, i)
        feeds.append(frame)

    # Create 2x2 grid
    top = cv2.hconcat(feeds[0:2])
    bottom = cv2.hconcat(feeds[2:4])
    grid = cv2.vconcat([top, bottom])

    # Show window
    cv2.imshow(WINDOW_NAME, grid)

    # Call AI every few seconds using camera 0
    current_time = time.time()
    if current_time - last_ai_check > ai_interval and enabled[0] and ai_frame is not None:
        print("🔎 Sending frame to AI...")
        try:
            response = ask_ai_about_image(ai_frame)
            print("🧠 AI says:", response)
        except Exception as e:
            print("❌ AI request failed:", e)
        last_ai_check = current_time

    # Quit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
for cam in cams:
    cam.release()
cv2.destroyAllWindows()
