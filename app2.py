import tkinter as tk
from googletrans import Translator

translator = Translator()

def translate():
    # Get text from the entry widget
    text = text_entry.get("1.0", "end-1c")

    # Translate the text
    translation = translator.translate(text, dest=destination_lang.get())

    # Update the output label with the translation
    output_label.config(text=translation.text)

# Create the main window
window = tk.Tk()
window.title("Google Translate")

# Create the widgets
text_entry = tk.Text(window, height=10, width=40)
destination_lang = tk.StringVar()
destination_lang.set("en")
destination_menu = tk.OptionMenu(window, destination_lang, "en", "es", "fr", "de", "zh-cn")
translate_button = tk.Button(window, text="Translate", command=translate)
output_label = tk.Label(window, text="")

# Add the widgets to the window
text_entry.pack()
destination_menu.pack()
translate_button.pack()
output_label.pack()

# Start the main loop
window.mainloop()
