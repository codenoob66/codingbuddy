import os, sys, tkinter as tk, threading
from dotenv import load_dotenv
from google import genai

# Works both during dev and when compiled
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

# Load the .env safely (works for both .py and .exe)
load_dotenv(resource_path(".env"))

# Initialize the Google AI client
client = genai.Client()

# ---- UI ----
root = tk.Tk()
root.title("One.com AI")
root.geometry("500x400")
root.configure(bg="#000000")
root.iconbitmap(resource_path("oneai.ico"))

# Styles
font_text = ("Helvetica", 12)
bg_text, fg_text = "#000000", "#ffffff"
button_bg, button_fg = "#76b82a", "#ffffff"

# Layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.rowconfigure(3, weight=0)

# Heading
heading = tk.Label(
    root, text="One.com AI Chat", font=("Helvetica", 18, "bold"),
    bg="#000000", fg="#76b82a"
)
heading.grid(row=0, column=0, columnspan=2, pady=15)

# Response box
response_area = tk.Text(
    root, width=50, height=10, bg=bg_text, fg=fg_text,
    font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
response_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
response_area.config(state=tk.DISABLED)

# Input box
text_area = tk.Text(
    root, width=40, height=2, bg=bg_text, fg=fg_text,
    font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
text_area.grid(row=2, column=0, padx=(10, 5), pady=(0, 15), sticky="ew")

# Main AI call
def main():
    user_input = text_area.get("1.0", "end-1c").strip()
    if not user_input:
        return

    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, "Thinking...")
    response_area.config(state=tk.DISABLED)

    response = client.models.generate_content(
        model="gemini-2.5-pro", contents=user_input
    )

    text = response.candidates[0].content.parts[0].text

    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, text)
    response_area.config(state=tk.DISABLED)
    text_area.delete("1.0", tk.END)

# Button
submit_button = tk.Button(
    root, text="Submit",
    command=lambda: threading.Thread(target=main).start(),
    bg=button_bg, fg=button_fg, font=("Helvetica", 11, "bold"),
    activebackground="#76b82a", bd=0, padx=10, pady=6
)
submit_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 15), sticky="e")

root.mainloop()
