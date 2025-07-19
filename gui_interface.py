import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import cv2
import threading

from camera_viewer import get_camera_grid
from ai_manager import query_interface_ai

# Constants
UPDATE_INTERVAL = 40  # ms (~25 FPS)

class AIInterfaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vision AI Interface")

        # --- Master vertical layout with expandable panes ---
        main_pane = tk.PanedWindow(root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # --- Video feed section ---
        self.video_label = tk.Label(main_pane)
        main_pane.add(self.video_label)

        # --- Scrollable AI output box ---
        self.output_box = scrolledtext.ScrolledText(main_pane, wrap=tk.WORD, height=12, font=("Consolas", 10))
        self.output_box.config(state=tk.DISABLED)
        main_pane.add(self.output_box)

        # --- Input frame (Text + Scrollbar) ---
        input_frame = tk.Frame(main_pane)
        self.input_text = tk.Text(input_frame, height=3, font=("Consolas", 10), wrap=tk.WORD)
        scrollbar = tk.Scrollbar(input_frame, command=self.input_text.yview)
        self.input_text.config(yscrollcommand=scrollbar.set)

        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_pane.add(input_frame)

        # --- Bindings ---
        self.input_text.bind("<Return>", self.send_prompt)
        self.input_text.bind("<Shift-Return>", self.insert_newline)

        # --- Start camera update loop ---
        self.update_video()

    def update_video(self):
        frame = get_camera_grid()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = img_tk
        self.video_label.config(image=img_tk)
        self.root.after(UPDATE_INTERVAL, self.update_video)

    def send_prompt(self, event=None):
        # Prevent default Return behavior
        if event:
            event.preventDefault = True

        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            return

        self.input_text.delete("1.0", tk.END)
        self.append_output(f"> {prompt}\n")
        self.handle_prompt(prompt)
        return "break"

    def insert_newline(self, event=None):
        self.input_text.insert(tk.INSERT, "\n")
        return "break"

    def append_output(self, text):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.insert(tk.END, text)
        self.output_box.see(tk.END)
        self.output_box.config(state=tk.DISABLED)

    def handle_prompt(self, prompt):
        def run_ai():
            response = query_interface_ai(prompt)
            self.append_output(response + "\n")

        threading.Thread(target=run_ai, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    gui = AIInterfaceGUI(root)
    root.mainloop()
