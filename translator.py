from deep_translator import GoogleTranslator
from tkinter import *
from tkinter import ttk, messagebox
from gtts import gTTS
from gtts.lang import tts_langs  # NEW: Used to check supported speech languages
import playsound
import os

# Initialize application window
root = Tk()
root.title("Language Translation Tool - CodeAlpha")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#2c3e50")

# --- THE FIX: Filter languages for 100% compatibility ---
# 1. Get all translation languages: {'french': 'fr', 'spanish': 'es', ...}
all_trans_langs = GoogleTranslator().get_supported_languages(as_dict=True)

# 2. Get all speech-supported languages: {'fr': 'French', 'es': 'Spanish', ...}
speech_supported_codes = tts_langs().keys()

# 3. Create a final dictionary of only the languages that support BOTH
lang_dict = {}
for lang_name, lang_code in all_trans_langs.items():
    if lang_code in speech_supported_codes:
        lang_dict[lang_name] = lang_code

# Extract just the names for the dropdown menu
languages = list(lang_dict.keys())

# ------------------- FUNCTIONS -------------------

def translate_text():
    """Translate the source text to the target language."""
    try:
        src = source_lang.get()
        dest = target_lang.get()
        text = input_text.get("1.0", END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text to translate.")
            return

        # Translate the text
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        output_text.delete("1.0", END)
        output_text.insert("1.0", translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {str(e)}")

def copy_text():
    """Copy translated text to clipboard."""
    text = output_text.get("1.0", END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Copied", "Translated text copied to clipboard.")

def speak_text():
    """Convert translated text to speech."""
    try:
        text = output_text.get("1.0", END).strip()
        if not text:
            messagebox.showwarning("Warning", "No translated text to speak.")
            return

        # Get the 2-letter code for the selected language
        selected_lang_name = target_lang.get()
        lang_code = lang_dict.get(selected_lang_name, "en") 
        
        # Create and save the audio file
        tts = gTTS(text=text, lang=lang_code)
        filename = "translated_audio.mp3"
        tts.save(filename)
        
        # Play the audio
        playsound.playsound(filename)
        
        # Safely try to delete the file after playing
        try:
            os.remove(filename)
        except PermissionError:
            pass # Ignore if Windows keeps the file locked
            
    except Exception as e:
        messagebox.showerror("Error", f"Speech playback failed: {str(e)}")

def clear_text():
    """Clear both input and output fields."""
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)

# ------------------- UI LAYOUT -------------------

# Title
title_label = Label(
    root, text="🌐 Language Translation Tool",
    font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white"
)
title_label.pack(pady=10)

# Input label
Label(root, text="Enter Text:", font=("Arial", 12, "bold"),
      bg="#2c3e50", fg="white").pack(anchor="w", padx=20)

input_text = Text(root, height=6, width=65, font=("Arial", 11),
                  wrap=WORD, bd=2, relief=GROOVE)
input_text.pack(padx=20, pady=5)

# Language selection frame
lang_frame = Frame(root, bg="#2c3e50")
lang_frame.pack(pady=10)

Label(lang_frame, text="From:", font=("Arial", 11, "bold"),
      bg="#2c3e50", fg="white").grid(row=0, column=0, padx=5)

source_lang = ttk.Combobox(lang_frame, values=languages, width=15)
source_lang.set("english") 
source_lang.grid(row=0, column=1, padx=5)

Label(lang_frame, text="To:", font=("Arial", 11, "bold"),
      bg="#2c3e50", fg="white").grid(row=0, column=2, padx=5)

target_lang = ttk.Combobox(lang_frame, values=languages, width=15)
target_lang.set("french") 
target_lang.grid(row=0, column=3, padx=5)

# Buttons
button_frame = Frame(root, bg="#2c3e50")
button_frame.pack(pady=10)

Button(button_frame, text="Translate", command=translate_text,
       bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
       width=12).grid(row=0, column=0, padx=5)

Button(button_frame, text="Copy", command=copy_text,
       bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
       width=10).grid(row=0, column=1, padx=5)

Button(button_frame, text="Speak", command=speak_text,
       bg="#8e44ad", fg="white", font=("Arial", 10, "bold"),
       width=10).grid(row=0, column=2, padx=5)

Button(button_frame, text="Clear", command=clear_text,
       bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
       width=10).grid(row=0, column=3, padx=5)

# Output label
Label(root, text="Translated Text:", font=("Arial", 12, "bold"),
      bg="#2c3e50", fg="white").pack(anchor="w", padx=20)

output_text = Text(root, height=6, width=65, font=("Arial", 11),
                   wrap=WORD, bd=2, relief=GROOVE, bg="#ecf0f1")
output_text.pack(padx=20, pady=5)

# Run application
root.mainloop()