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
root.configure(bg="#1e1e2f")  # Dark stylish background

# Fonts and colors
font_text = ("Helvetica", 12)
font_button = ("Helvetica", 12, "bold")
bg_text = "#2e2e3e"
fg_text = "#ffffff"
button_bg = "#ff5c5c"
button_fg = "#ffffff"

# Heading Label
heading = tk.Label(
    root, text="One.com AI Chat", font=("Helvetica", 18, "bold"), bg="#1e1e2f", fg="#ffcc00"
)
heading.pack(pady=15)

# Response Area
response_area = tk.Text(
    root, width=50, height=10, bg=bg_text, fg=fg_text, font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
response_area.pack(pady=(0, 10))
response_area.config(state=tk.DISABLED)

# Input Area
text_area = tk.Text(
    root, width=50, height=3, bg=bg_text, fg=fg_text, font=font_text, bd=0, padx=10, pady=10, wrap="word"
)
text_area.pack(pady=(0, 15))

# Submit Button
submit_button = tk.Button(
    root,
    text="Submit",
    command=lambda: threading.Thread(target=main).start(),  # Run main in background
    bg=button_bg,
    fg=button_fg,
    font=font_button,
    activebackground="#ff7b7b",
    activeforeground="#ffffff",
    bd=0,
    padx=20,
    pady=10,
)
submit_button.pack()

# Rounded corners effect (subtle look)
for widget in [response_area, text_area]:
    widget.config(highlightthickness=2, highlightbackground="#ffcc00", highlightcolor="#ffcc00")

def main():
    user_input = text_area.get("1.0", "end-1c").strip()
    if not user_input:
        return
    
    # Show "typing..." to improve UX
    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, "Thinking...")
    response_area.config(state=tk.DISABLED)

    # Make the API call
    response = client.models.generate_content(
        model="gemini-2.5-pro", contents=user_input
    )
    
    # Update the UI with the response
    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, response.candidates[0].content.parts[0].text)
    response_area.config(state=tk.DISABLED)
    text_area.delete("1.0", tk.END)

root.mainloop()
