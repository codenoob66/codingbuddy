from google import genai
from dotenv import load_dotenv
import tkinter as tk
import threading

# --- Setup Google GenAI Client ---
load_dotenv()
client = genai.Client()

# --- UI Setup ---
root = tk.Tk()
root.title("One.com AI")
root.geometry("500x400")
root.configure(bg="#000000")

font_text = ("Helvetica", 12)
font_button = ("Helvetica", 12, "bold")
bg_main = "#3c3c3c"
fg_main = "#ffffff"
accent = "#76b82a"

# --- Heading ---
heading = tk.Label(
    root,
    text="One.com AI Chat",
    font=("Helvetica", 18, "bold"),
    bg="#000000",
    fg=accent
)
heading.pack(pady=15)

# --- Response Area ---
response_area = tk.Text(
    root,
    width=50,
    height=10,
    bg=bg_main,
    fg=fg_main,
    font=font_text,
    bd=1,
    padx=10,
    pady=10,
    wrap="word",
    highlightthickness=2,
    highlightbackground=accent,
    highlightcolor=accent
)
response_area.pack(pady=(0, 10))
response_area.config(state=tk.DISABLED)

# --- Input Area ---
text_area = tk.Text(
    root,
    width=50,
    height=3,
    bg=bg_main,
    fg=fg_main,
    font=font_text,
    bd=1,
    padx=10,
    pady=10,
    wrap="word",
    highlightthickness=2,
    highlightbackground=accent,
    highlightcolor=accent
)
text_area.pack(pady=(0, 15))


# --- Stream Logic ---
def stream_response(user_input: str):
    # Show "Thinking..." feedback
    response_area.config(state=tk.NORMAL)
    response_area.delete("1.0", tk.END)
    response_area.insert(tk.END, "Thinking...\n")
    response_area.config(state=tk.DISABLED)

    try:
        # Start streaming from Gemini
        stream = client.models.generate_content_stream(
            model="gemini-2.5-pro",
            contents=user_input
        )

        response_area.config(state=tk.NORMAL)
        response_area.delete("1.0", tk.END)

        # Stream chunks as they arrive
        for chunk in stream:
            if hasattr(chunk, "text") and chunk.text:
                response_area.insert(tk.END, chunk.text)
                response_area.see(tk.END)
                response_area.update_idletasks()

        response_area.config(state=tk.DISABLED)

    except Exception as e:
        response_area.config(state=tk.NORMAL)
        response_area.delete("1.0", tk.END)
        response_area.insert(tk.END, f"Error: {e}")
        response_area.config(state=tk.DISABLED)


# --- Button Handler ---
def on_submit():
    user_input = text_area.get("1.0", "end-1c").strip()
    if not user_input:
        return

    text_area.delete("1.0", tk.END)
    threading.Thread(target=stream_response, args=(user_input,)).start()


# --- Submit Button ---
submit_button = tk.Button(
    root,
    text="Submit",
    command=on_submit,
    bg=accent,
    fg=fg_main,
    font=font_button,
    activebackground="#3c3c3c",
    activeforeground=accent,
    bd=0,
    padx=20,
    pady=10,
)
submit_button.pack()

root.mainloop()
