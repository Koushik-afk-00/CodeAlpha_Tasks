import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator


# Language Dictionary

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Japanese": "ja",
    "Korean": "ko",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}


# Translation Function

def translate_text():

    text = input_text.get("1.0", tk.END).strip()

    source_language = source_combo.get()
    target_language = target_combo.get()

    if text == "":
        messagebox.showwarning(
            "Warning",
            "Please enter some text."
        )
        return

    try:

        if source_language == "Auto Detect":
            source_code = "auto"
        else:
            source_code = languages[source_language]

        target_code = languages[target_language]

        translated = GoogleTranslator(
            source=source_code,
            target=target_code
        ).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

    except Exception as error:

        messagebox.showerror(
            "Translation Error",
            str(error)
        )


# Copy Function

def copy_text():

    translated = output_text.get("1.0", tk.END).strip()

    if translated == "":
        messagebox.showwarning(
            "Warning",
            "There is no translation to copy."
        )
        return

    window.clipboard_clear()
    window.clipboard_append(translated)

    messagebox.showinfo(
        "Copied",
        "Translation copied to clipboard!"
    )


# Clear Function

def clear_text():

    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)


# Main Window

window = tk.Tk()

window.title("Language Translation Tool")
window.geometry("800x600")
window.resizable(False, False)


# Title

title = tk.Label(
    window,
    text="🌐 Language Translation Tool",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)


# Language Selection Frame

language_frame = tk.Frame(window)
language_frame.pack(pady=10)


# Source Language

source_label = tk.Label(
    language_frame,
    text="Source Language",
    font=("Arial", 12)
)

source_label.grid(
    row=0,
    column=0,
    padx=20
)

source_combo = ttk.Combobox(
    language_frame,
    values=["Auto Detect"] + list(languages.keys()),
    state="readonly",
    width=18
)

source_combo.set("Auto Detect")

source_combo.grid(
    row=1,
    column=0,
    padx=20
)


# Target Language

target_label = tk.Label(
    language_frame,
    text="Target Language",
    font=("Arial", 12)
)

target_label.grid(
    row=0,
    column=1,
    padx=20
)

target_combo = ttk.Combobox(
    language_frame,
    values=list(languages.keys()),
    state="readonly",
    width=18
)

target_combo.set("Tamil")

target_combo.grid(
    row=1,
    column=1,
    padx=20
)


# Input Text

input_label = tk.Label(
    window,
    text="Enter Text",
    font=("Arial", 14, "bold")
)

input_label.pack(
    anchor="w",
    padx=80,
    pady=(20, 5)
)

input_text = tk.Text(
    window,
    height=7,
    width=75,
    font=("Arial", 12)
)

input_text.pack()


# Translate Button

translate_button = tk.Button(
    window,
    text="Translate",
    command=translate_text,
    font=("Arial", 12, "bold"),
    padx=30,
    pady=8
)

translate_button.pack(pady=15)


# Output Text

output_label = tk.Label(
    window,
    text="Translated Text",
    font=("Arial", 14, "bold")
)

output_label.pack(
    anchor="w",
    padx=80,
    pady=(5, 5)
)

output_text = tk.Text(
    window,
    height=7,
    width=75,
    font=("Arial", 12)
)

output_text.pack()


# Buttons

button_frame = tk.Frame(window)
button_frame.pack(pady=15)


# Copy Button

copy_button = tk.Button(
    button_frame,
    text="Copy Translation",
    command=copy_text,
    font=("Arial", 11),
    padx=15,
    pady=5
)

copy_button.grid(
    row=0,
    column=0,
    padx=10
)


# Clear Button

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_text,
    font=("Arial", 11),
    padx=25,
    pady=5
)

clear_button.grid(
    row=0,
    column=1,
    padx=10
)


# Start Application

window.mainloop()