import subprocess
import sys
import nltk
import tkinter as tk
from tkinter import scrolledtext, messagebox
from transformers import pipeline
import threading

# Install essential libraries (only once)
def install_packages():
    packages = ["transformers", "torch", "nltk"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_packages()

# Ensure punkt tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load model pipeline
summarizer = pipeline("summarization")

# Start GUI
app = tk.Tk()
app.title("🤖 TEXT SUMMARIZATION TOOL")
app.geometry("950x720")
app.config(bg="#eef2f5")

# Fonts
FONT_TITLE = ("Poppins", 20, "bold")
FONT_LABEL = ("Poppins", 12)
FONT_TEXT = ("Poppins", 11)

# --- GUI Layout ---

# Title
tk.Label(app, text="🧠 TEXT SUMMARIZATION TOOL", font=FONT_TITLE, bg="#eef2f5").pack(pady=10)

# Token Counter
token_var = tk.StringVar()
token_var.set("Words: 0")
token_label = tk.Label(app, textvariable=token_var, bg="#eef2f5", font=FONT_LABEL)
token_label.pack(anchor="e", padx=20)

# Input Label
tk.Label(app, text="Paste your long content/article here:", font=FONT_LABEL, bg="#eef2f5").pack(anchor="w", padx=20)

# Input Area
input_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=15, font=FONT_TEXT)
input_area.pack(padx=20, pady=(5, 15), fill="both", expand=True)

# Summary Length Slider
tk.Label(app, text="Set maximum summary length (words):", font=FONT_LABEL, bg="#eef2f5").pack(anchor="w", padx=20)
length_slider = tk.Scale(app, from_=50, to=300, orient=tk.HORIZONTAL, length=300)
length_slider.set(120)
length_slider.pack(pady=(0, 10))

# Output Label
tk.Label(app, text="Summary Output:", font=FONT_LABEL, bg="#eef2f5").pack(anchor="w", padx=20)

# Output Area
output_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=10, font=FONT_TEXT, bg="#fff")
output_area.pack(padx=20, pady=10, fill="both", expand=True)

# --- Functionalities ---

# Update token count live
def update_word_count(event=None):
    text = input_area.get("1.0", tk.END)
    word_count = len(text.strip().split())
    token_var.set(f"Words: {word_count}")

input_area.bind("<KeyRelease>", update_word_count)

# Summarize logic
def summarize_text():
    text = input_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter some text.")
        return

    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, "🔄 Summarizing...")

    summarize_btn.config(state="disabled")

    def run_summary():
        try:
            max_len = length_slider.get()
            min_len = max(30, max_len // 2)

            summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, summary[0]['summary_text'])
        except Exception as e:
            output_area.delete("1.0", tk.END)
            output_area.insert(tk.END, f"Error: {str(e)}")
        finally:
            summarize_btn.config(state="normal")

    threading.Thread(target=run_summary).start()

# Clear all
def clear_text():
    input_area.delete("1.0", tk.END)
    output_area.delete("1.0", tk.END)
    token_var.set("Words: 0")

# Buttons
frame = tk.Frame(app, bg="#eef2f5")
frame.pack(pady=10)

summarize_btn = tk.Button(frame, text="✨ Summarize", command=summarize_text,
                          font=FONT_LABEL, bg="#007acc", fg="white", padx=15, pady=5)
summarize_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(frame, text="🧹 Clear All", command=clear_text,
                      font=FONT_LABEL, bg="#f44336", fg="white", padx=15, pady=5)
clear_btn.grid(row=0, column=1, padx=10)

# Start GUI loop
app.mainloop()