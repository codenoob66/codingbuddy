from google import genai
from dotenv import load_dotenv
import tkinter as tk
import threading

# Load env and initialize client once
load_dotenv()
client = genai.Client()

root = tk.Tk()
root.title("One.com AI")
root.geometry("500x400")
root.configure(bg="#000000")  # Dark stylish background

# Fonts and colors
font_text = ("Helvetica", 12)
font_button = ("Helvetica", 12, "bold")
bg_text = "#000000"
fg_text = "#ffffff"
button_bg = "#76b82a"
button_fg = "#ffffff"

# Configure grid weights for resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.rowconfigure(3, weight=0)

# Heading Label
heading = tk.Label(
    root, text="One.com AI Chat", font=("Helvetica", 18, "bold"), bg="#000000", fg="#76b82a"
)
heading.grid(row=0, column=0, columnspan=2, pady=15)

# Response Area
response_area = tk.Text(
    root, width=50, height=10, bg=bg_text, fg=fg_text, font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
response_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
response_area.config(state=tk.DISABLED)

# Input Area
text_area = tk.Text(
    root, width=40, height=2, bg=bg_text, fg=fg_text, font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
text_area.grid(row=2, column=0, padx=(10, 5), pady=(0, 15), sticky="ew")

# Submit Button (beside input)
submit_button = tk.Button(
    root,
    text="Submit",
    command=lambda: threading.Thread(target=main).start(),
    bg=button_bg,
    fg=button_fg,
    font=("Helvetica", 11, "bold"),  # slightly smaller font
    activebackground="#76b82a",
    bd=0,
    padx=10,   # smaller horizontal padding
    pady=6,    # smaller vertical padding
)
submit_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 15), sticky="e")


# Rounded corners effect
for widget in [response_area, text_area]:
    widget.config(highlightthickness=2)

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
    
    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, response.candidates[0].content.parts[0].text)
    response_area.config(state=tk.DISABLED)
    text_area.delete("1.0", tk.END)

root.mainloop()
