import tkinter as tk
from tkinter import messagebox
import threading
import time

class SimplePomodoro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍅 Simple Pomodoro Timer")
        self.root.geometry("350x300")
        self.root.resizable(False, False)
        
        self.work_time = 25 * 60
        self.rest_time = 5 * 60
        self.time_left = self.work_time
        self.is_running = False
        self.is_work_time = True
        self.sessions_completed = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(
            self.root,
            text="🍅 Pomodoro Timer",
            font=("Arial", 18, "bold"),
            fg="#FF5722"
        ).pack(pady=10)
        
        self.timer_label = tk.Label(
            self.root,
            text="25:00",
            font=("Arial", 48, "bold"),
            fg="#FF5722"
        )
        self.timer_label.pack(pady=20)
        
        self.status_label = tk.Label(
            self.root,
            text="Work Time",
            font=("Arial", 12),
            fg="#4CAF50"
        )
        self.status_label.pack()
        
        self.session_label = tk.Label(
            self.root,
            text=f"Sessions completed: {self.sessions_completed}",
            font=("Arial", 11)
        )
        self.session_label.pack(pady=5)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            bg="#4CAF50",
            fg="white",
            width=8,
            font=("Arial", 11)
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            bg="#FFC107",
            fg="black",
            width=8,
            font=("Arial", 11),
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            bg="#F44336",
            fg="white",
            width=8,
            font=("Arial", 11)
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            self.root,
            text="Reset Counter",
            command=self.reset_counter,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10)
        ).pack(pady=10)
    
    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def timer_thread(self):
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.root.after(0, self.update_display)
        
        if self.is_running and self.time_left == 0:
            self.root.after(0, self.timer_complete)
    
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            threading.Thread(target=self.timer_thread, daemon=True).start()
    
    def pause_timer(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def reset_timer(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        self.is_work_time = True
        self.time_left = self.work_time
        self.status_label.config(text="Work Time", fg="#4CAF50")
        self.timer_label.config(fg="#FF5722")
        self.update_display()
    
    def timer_complete(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        if self.is_work_time:
            self.sessions_completed += 1
            self.session_label.config(text=f"Sessions completed: {self.sessions_completed}")
            messagebox.showinfo("Time's Up!", "Work session complete! Time for a break!")
            self.is_work_time = False
            self.time_left = self.rest_time
            self.status_label.config(text="Break Time", fg="#FF9800")
            self.timer_label.config(fg="#FF9800")
        else:
            messagebox.showinfo("Break Over!", "Break finished! Ready to work?")
            self.is_work_time = True
            self.time_left = self.work_time
            self.status_label.config(text="Work Time", fg="#4CAF50")
            self.timer_label.config(fg="#FF5722")
        
        self.update_display()
    
    def reset_counter(self):
        if messagebox.askyesno("Reset Counter", "Reset session counter to 0?"):
            self.sessions_completed = 0
            self.session_label.config(text=f"Sessions completed: {self.sessions_completed}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimplePomodoro()
    app.run()