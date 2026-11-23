"""AirScroll desktop application."""
import queue
import threading
import tkinter as tk
from tkinter import messagebox

import cv2
import customtkinter as ctk
from PIL import Image

from modules.vision_controller import VisionController
from config import FRAME_QUEUE_SIZE, STATUS_UPDATE_INTERVAL_MS


class AirScrollApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AirScroll | Touchless Screen Control")
        self.geometry("1120x760")
        self.minsize(900, 650)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.mode = "Hand Pinch"
        self.active = False
        self.stop_event = threading.Event()
        self.frame_queue = queue.Queue(maxsize=FRAME_QUEUE_SIZE)
        self.worker = None
        self.last_status = "Ready - press Start Camera"

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(STATUS_UPDATE_INTERVAL_MS, self._update_preview)

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, corner_radius=0, fg_color="#101827")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="AirScroll", font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#65D6AD"
        ).grid(row=0, column=0, padx=26, pady=(18, 2), sticky="w")
        ctk.CTkLabel(
            header, text="Touchless screen control powered by Computer Vision",
            font=ctk.CTkFont(size=13), text_color="#B7C4D5"
        ).grid(row=1, column=0, padx=28, pady=(0, 18), sticky="w")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, padx=22, pady=20, sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        preview_card = ctk.CTkFrame(body, corner_radius=16)
        preview_card.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        preview_card.grid_rowconfigure(1, weight=1)
        preview_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            preview_card, text="LIVE CAMERA", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=18, pady=14, sticky="w")

        self.preview = ctk.CTkLabel(
            preview_card, text="Camera is off\n\nPress  START CAMERA  to begin",
            font=ctk.CTkFont(size=18), text_color="#AAB7C8",
            fg_color="#080D16", corner_radius=12
        )
        self.preview.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")

        side = ctk.CTkFrame(body, corner_radius=16)
        side.grid(row=0, column=1, sticky="nsew")
        side.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            side, text="CONTROL PANEL", font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        ctk.CTkLabel(side, text="Select interaction mode", text_color="#AAB7C8").grid(
            row=1, column=0, padx=18, pady=(8, 5), sticky="w"
        )
        self.mode_selector = ctk.CTkSegmentedButton(
            side, values=["Hand Pinch", "Blink"],
            command=self._change_mode
        )
        self.mode_selector.set("Hand Pinch")
        self.mode_selector.grid(row=2, column=0, padx=18, pady=(0, 16), sticky="ew")

        self.start_button = ctk.CTkButton(
            side, text="START CAMERA", height=44, corner_radius=10,
            fg_color="#15966D", hover_color="#117B5A", command=self.start_camera
        )
        self.start_button.grid(row=3, column=0, padx=18, pady=7, sticky="ew")

        self.stop_button = ctk.CTkButton(
            side, text="STOP CAMERA", height=42, corner_radius=10,
            fg_color="#9B3543", hover_color="#7D2935",
            command=self.stop_camera, state="disabled"
        )
        self.stop_button.grid(row=4, column=0, padx=18, pady=7, sticky="ew")

        ctk.CTkLabel(side, text="SYSTEM STATUS", text_color="#AAB7C8").grid(
            row=5, column=0, padx=18, pady=(24, 5), sticky="w"
        )
        self.status_label = ctk.CTkLabel(
            side, text="● OFFLINE", text_color="#F0B65A",
            font=ctk.CTkFont(size=14, weight="bold"), wraplength=230
        )
        self.status_label.grid(row=6, column=0, padx=18, pady=(0, 8), sticky="w")

        self.detail_label = ctk.CTkLabel(
            side, text=self.last_status, text_color="#AAB7C8",
            justify="left", wraplength=230
        )
        self.detail_label.grid(row=7, column=0, padx=18, pady=(0, 16), sticky="w")

        tips = ctk.CTkFrame(side, fg_color="#182438", corner_radius=12)
        tips.grid(row=8, column=0, padx=14, pady=(8, 16), sticky="ew")
        ctk.CTkLabel(
            tips, text="QUICK GUIDE", font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#65D6AD"
        ).pack(anchor="w", padx=12, pady=(12, 5))
        self.guide_label = ctk.CTkLabel(
            tips,
            text="Pinch thumb + index on either hand.\nUse both hands together and move up/down to scroll.",
            justify="left", wraplength=220, text_color="#D1D9E5"
        )
        self.guide_label.pack(anchor="w", padx=12, pady=(0, 12))

        footer = ctk.CTkLabel(
            self, text="AirScroll • OpenCV • MediaPipe • PyAutoGUI",
            text_color="#78879A", font=ctk.CTkFont(size=11)
        )
        footer.grid(row=2, column=0, pady=(0, 12))

    def _change_mode(self, value):
        self.mode = value
        if value == "Hand Pinch":
            self.guide_label.configure(
                text="Pinch thumb + index on either hand.\nUse both hands together and move up/down to scroll."
            )
        else:
            self.guide_label.configure(
                text="One deliberate blink: scroll down.\nQuick double blink: scroll up."
            )
        self.detail_label.configure(text=f"Selected mode: {value}")

    def _set_status(self, message):
        self.last_status = message
        if self.active:
            self.status_label.configure(text="● RUNNING", text_color="#65D6AD")
        else:
            self.status_label.configure(text="● OFFLINE", text_color="#F0B65A")
        self.detail_label.configure(text=message)

    def _on_worker_status(self, message):
        # Called by worker thread; schedule all Tk updates on main thread.
        self.after(0, lambda: self._set_status(message))

    def _put_frame(self, frame, status):
        try:
            if self.frame_queue.full():
                self.frame_queue.get_nowait()
            self.frame_queue.put_nowait((frame, status))
        except queue.Empty:
            pass
        except queue.Full:
            pass

    def start_camera(self):
        if self.active:
            return
        self.stop_event.clear()
        self.active = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self._set_status("Starting webcam...")
        self.worker = threading.Thread(
            target=self._worker_main, daemon=True
        )
        self.worker.start()

    def _worker_main(self):
        controller = None
        try:
            controller = VisionController(
                mode_getter=lambda: self.mode,
                status_callback=self._on_worker_status
            )
            controller.run(self._put_frame, self.stop_event)
        except Exception as exc:
            self._on_worker_status(f"Error: {exc}")
            self.after(0, lambda: messagebox.showerror("AirScroll error", str(exc)))
        finally:
            self.after(0, self._worker_finished)

    def _worker_finished(self):
        self.active = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        if self.last_status.startswith("Error:"):
            self.status_label.configure(text="● ERROR", text_color="#F06B75")
        else:
            self.status_label.configure(text="● OFFLINE", text_color="#F0B65A")

    def stop_camera(self):
        if not self.active:
            return
        self.stop_event.set()
        self._set_status("Stopping camera...")
        self.stop_button.configure(state="disabled")

    def _update_preview(self):
        try:
            frame, status = self.frame_queue.get_nowait()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            image.thumbnail((640, 360), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )
            self.preview.configure(image=photo, text="")
            self.preview.image = photo
            self.detail_label.configure(text=status)
        except queue.Empty:
            pass
        self.after(STATUS_UPDATE_INTERVAL_MS, self._update_preview)

    def on_close(self):
        self.stop_event.set()
        self.destroy()


if __name__ == "__main__":
    app = AirScrollApp()
    app.mainloop()
