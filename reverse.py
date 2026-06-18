### Version 1.0 ### Find SKU From Image ###

## verify code works with actual images

from tkinter.filedialog import *
import tkinter as tk
import re
from PIL import Image
import pytesseract

#variables
root = tk.Tk()
choose_image_button = tk.Button(root, text="Choose Image",)
continue_button = tk.Button(root, text="continue")
clear_button = tk.Button(root, text="clear")
image_entry = tk.Entry(root) ## may need to change for pillow
output_entry = tk.Entry(root) 

selected_image = None

#window config
root.title("Find SKU Code")
root.geometry("600x350")
root.resizable(False, False)

#functions
def load_image():

    global selected_image

    file_path = askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    image = Image.open(file_path)
    selected_image = image

def extract_text(selected_image):
    text = pytesseract.image_to_string(selected_image)
    return text

def find_sku(text):
    lines = text.splitlines()
    patterns = [
        r'\bSKU[:\s]*([A-Za-z0-9]+)\b',  # Matches "SKU: ABC123" or "SKU ABC123"
        r'\b([A-Za-z0-9]+-[A-Za-z0-9]+)\b'  # Matches patterns like "ABC-123"
    ]
    for line in lines:
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
    return None

def print_sku():
    if selected_image is None:
        return
    
    text = extract_text(selected_image)
    sku = find_sku(text)
    if sku:
        output_entry.insert(0, sku)
    else:
        output_entry.insert(0, "SKU not found")


#layout
tk.Label(root, text="Insert image").place(x=15, y=25)
image_entry.place(x=15, y=50) ## may need to change for pillow
continue_button.place(x=195, y=50)
output_entry.place(x=15, y=100)
clear_button.place(x=195, y=150)
choose_image_button.place(x=15, y=200)

#button config
choose_image_button.config(command=load_image)
continue_button.config(command=lambda: print_sku())

root.mainloop()