import tkinter as tk
import threading
import mss
import cv2
import numpy as np
import time

class ScreenRecorderApp:
    def __init__(self, master):
        self.master = master
        self.is_recording = False
        self.stop_event = threading.Event()
        self.recording_thread = None

        # Create GUI buttons
        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)

        # Add buttons to the window
        self.start_button.pack()
        self.stop_button.pack()

    def start_recording(self):
        """Start the screen recording in a separate thread."""
        if not self.is_recording:
            self.is_recording = True
            self.stop_event.clear()  # Reset stop signal
            self.recording_thread = threading.Thread(target=self.record_screen)
            self.recording_thread.start()
            # Update button states
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_recording(self):
        """Stop the screen recording and reset button states."""
        if self.is_recording:
            self.stop_event.set()  # Signal the thread to stop
            self.recording_thread.join()  # Wait for the thread to finish
            self.is_recording = False
            # Update button states
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def record_screen(self):
        """Capture the screen and save it as a video."""
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            width = monitor['width']
            height = monitor['height']

            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

            while not self.stop_event.is_set():
                # Capture a frame
                frame = sct.grab(monitor)
                frame = np.array(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert to BGR for OpenCV

                # Write the frame to the video
                out.write(frame)

                # Control frame rate (~20 FPS)
                time.sleep(0.05)

            # Clean up
            out.release()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Screen Recorder")
    app = ScreenRecorderApp(root)
    root.mainloop()