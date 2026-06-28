from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter as tk
import re
from PIL import Image, ImageOps
import numpy as np
import easyocr
import json
import requests
from bs4 import BeautifulSoup
from search import search_web 
from ocr import extract_text, find_sku

#tk variables
root = tk.Tk()
choose_image_button = tk.Button(root, text="Choose Image",)
continue_button = tk.Button(root, text="continue")
clear_button = tk.Button(root, text="clear")
search_button = tk.Button(root, text="search")
image_entry = tk.Entry(root) ## may need to change for pillow
output_entry = tk.Entry(root)
filepath_text = tk.Text(root, height=1, width=50)
success_text = tk.Text(root, height=1, width=50)

#body variables
#selected_image = None
#selected_image_path = None
#reader = easyocr.Reader(['en'])

#window config
root.title("Find SKU Code")
root.geometry("600x350")
root.resizable(False, False)

#functions
def load_image():

    global selected_image
    global selected_image_path

    file_path = askopenfilename(
        parent=root,
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")
            ]
    )
    
    if not file_path:
        return
    else:
        selected_image = Image.open(file_path)
        selected_image = ImageOps.exif_transpose(selected_image)
        selected_image = selected_image.convert('RGB')
        print("image size: ", selected_image.size)
        print("image mode: ", selected_image.mode)
        selected_image_path = file_path
        #selected_image.save("debug_loaded_image.jpg")
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)

    print("loaded image: ", selected_image)
    return selected_image


#def extract_text(selected_image):

    image = selected_image.resize(
        (selected_image.width * 3, selected_image.height * 3)
    )

    image_array = np.array(image)
    #text = reader.readtext(selected_image)
    
    result = reader.readtext(
        image_array,
        detail=1,
        paragraph=False,
        mag_ratio=2,
        text_threshold=0.3,
        low_text=0.2,
        link_threshold=0.2
    )
    
    print("Easy-OCR raw result: ", result)
    
    text = "\n".join([item[1] for item in result])
    text = text.upper()
    text = text.replace("*", "#")

    print("Extracted text: ")
    print((repr(text)))
    return text

#def find_sku(text):
    
    lines = text.splitlines()
    
    patterns = [

    r'([A-Z]{2}\#[0-9]{5})',

    # RN#73277
    r'(RN#\d+)',

    # RN 73277
    r'(RN\s+\d+)',

    # DX1234-001 (Nike)
    r'([A-Z]{2}\d{4}-\d{3})',

    # ABC123456
    r'([A-Z]{3}\d{6})',

    # ABC12345
    r'([A-Z]{3}\d{5})',

    # ABC1234
    r'([A-Z]{3}\d{4})',

    # 12345678
    r'(\d{8})',

    # 123456789
    r'(\d{9})',

    # 123456789012
    r'(\d{12})',

    # 1234567890123
    r'(\d{13})',

    # ABC-123
    r'([A-Z]{3}-\d{3})',

    # ABCD-1234
    r'([A-Z]{4}-\d{4})',

    # ABC123-456
    r'([A-Z]{3}\d{3}-\d{3})',

    # ABC123456789
    r'([A-Z]{3}\d{9})',

    # AA123456
    r'([A-Z]{2}\d{6})',

    # A12345678
    r'([A-Z]\d{8})',

    # ABCD1234
    r'([A-Z]{4}\d{4})',

    # ABCD12345
    r'([A-Z]{4}\d{5})',

    # Style: DX1234-001
    r'Style[:\s]*([A-Z]{2}\d{4}-\d{3})',

    # SKU: ABC12345
    r'SKU[:\s]*([A-Z0-9\-]+)',

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
    identifier = find_sku(text)

    if identifier:
        output_entry.insert(0, identifier)
    else:
        output_entry.insert(0, "Identifier not found")

    return identifier

def clear_fields():
    image_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)

def continue_button_pressed():
    image_path = load_image()
    text = extract_text(image_path)
    identifier = find_sku(text)
    candidates = search_web(identifier)

    print(f"Candidates: {candidates}")

def search_button_pressed():
    pass

#layout
tk.Label(root, text="Insert image").place(x=15, y=25)
image_entry.place(x=15, y=50) ## may need to change for pillow
continue_button.place(x=195, y=50)
output_entry.place(x=15, y=100)
clear_button.place(x=195, y=100)
choose_image_button.place(x=15, y=135)
success_text.place(x=15, y=170)
search_button.place(x=195, y=135)

#button config
choose_image_button.config(command=load_image)
continue_button.config(command=continue_button_pressed)
clear_button.config(command=clear_fields)
#search_button.config(command=search_web)

## possible function call for search_web() ##
        #identifier = print_sku()
        #candidates = search_web(identifier)

        #for candidate in candidates:
        #    print(candidate["score"], candidate["url"])
######

root.mainloop()