# Wheres_WALDO

# Vision AI Interface

A modular, multi-camera AI visual interface designed for real-time object recognition, AI interaction, and future robotic control.

---

## 🧠 Project Overview

WALDO is a Python-based AI assistant interface with live video input from up to 4 USB cameras. Each feed is processed independently by an associated AI instance, while a central "interface AI" receives typed input from the user and intelligently routes context-aware prompts.

This system is designed for rapid prototyping of AI perception systems, with the end goal of integrating with physical robotics such as Le Robot (open-source robotic arm).

---

## ✅ Features Implemented So Far

* **Modular Project Structure** with separate files for UI, camera, AI logic, and API integration.
* **4-Camera Feed Grid** with on/off toggles and camera index overlay.
* **Interface GUI** built using Tkinter:

  * Live 2x2 camera feed display (20-25 FPS)
  * Scrollable AI output log
  * Resizable, expandable interface layout (via PanedWindow)
  * Multiline input box with Shift+Enter for newline, Enter to send
* **API Integration** using NRP (Nautilus Research Platform) API with llava-onevision model
* **Query Routing** via `ai_manager.py` to link camera-specific prompts to appropriate AI instance
* **.bat Launcher** for easy startup without CLI or terminal

---

## 🛠️ Configuration & Setup

### 🔧 Requirements

* Python 3.10+
* Virtual environment activated (venv)
* Dependencies:

```bash
# Create and activate a virtual environment (if not done yet)
python -m venv venv
.\venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip

# Core dependencies
pip install opencv-python
pip install numpy
pip install pillow
pip install openai==1.30.1   # Match your API version & structure
pip install requests
pip install python-dotenv    # Optional, for storing API keys in a .env file

```
###📦 If You’re Using Image-to-Text Models (like LLaVA or Phi3-Vision)
You may need:

```bash
pip install matplotlib
pip install transformers
pip install torch torchvision torchaudio
```
###⚠️ These are only needed if you plan to run a local visual model like llava or phi3, which is not currently in place. ###Otherwise, they are not required for API-only use.

###🖼️ OpenCV Camera Access Issues on Windows
###If OpenCV can’t access your camera on Windows, install these:

```bash
pip install opencv-contrib-python
```







### 📁 Project Structure

```
project/
├── camera_viewer.py       # Handles video grid and feed logic
├── gui_interface.py       # User interface (Tkinter)
├── ai_manager.py          # Prompt routing & AI instance control
├── vision_ai.py           # NRP API integration
├── .env                   # Contains your NRP_API_KEY
├── run_interface.bat      # Windows launcher
```

### 🔐 .env File Format

```
NRP_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

Run the interface by double-clicking `run_interface.bat`

---

## 🔮 What’s Happening Next

### 🧠 Interface AI Enhancements

* No longer requires phrases like "What do you see on camera..."
* Interprets context (e.g., "Where is the red box?" → uses AI judgment to query and correlate feeds)
* Maintains ongoing conversation context (multimodal grounding)

### 🧼 Camera Feed Cleanup

* Exclude toggle buttons and number overlays from AI input images

### 🧊 Object Recognition Overlay

* Display bounding boxes and labels on objects identified in live feeds
* Include (x, y) pixel coordinates for object location

### 🧭 Spatial Mapping

* Estimate 3D position (x, y, z) using triangulation across camera angles
* Requires calibrated camera positioning configuration file

### 🤖 Robotic Arm Integration

* Connect AI output to control Le Robot (open-source)
* Allow AI to select and manipulate objects based on camera data and interface prompts
* Step toward full perception-actuation loop

---

## 🔗 External Resources / Dependencies

* [NRP Nautilus API](https://llm.nrp-nautilus.io/v1)
* [OpenAI Python SDK (custom base\_url support)](https://github.com/openai/openai-python)
* \[Le Robot GitHub (TBD: insert link)]
* [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
* [LLaVA (vision-language model)](https://llava-vl.github.io/)

---

## 📌 Contributions & Expansion

This system is modular and open to extension:

* Add persistent memory per AI
* Integrate voice recognition and TTS
* Enable external plugin system for additional sensors or actuators
* Allow in-GUI camera toggling, layout presets, and dark mode themes

---

> Built by Peter Shryock for a future where AI can see, speak, and act.
