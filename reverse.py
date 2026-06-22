### Version 1.0 ### Find SKU From Image ###

from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter as tk
import re
from PIL import Image, ImageOps
import numpy as np
import easyocr

#tk variables
root = tk.Tk()
choose_image_button = tk.Button(root, text="Choose Image",)
continue_button = tk.Button(root, text="continue")
clear_button = tk.Button(root, text="clear")
image_entry = tk.Entry(root) ## may need to change for pillow
output_entry = tk.Entry(root)
filepath_text = tk.Text(root, height=1, width=50)

#body variables
selected_image = None
selected_image_path = None
reader = easyocr.Reader(['en'])

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



def extract_text(selected_image):

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

    print("Extracted text: ")
    print((repr(text)))
    return text

def find_sku(text):
    
    lines = text.splitlines()
    
    patterns = [
        r'(RN#\d+)'
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

def clear_fields():
    image_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)


#layout
tk.Label(root, text="Insert image").place(x=15, y=25)
image_entry.place(x=15, y=50) ## may need to change for pillow
continue_button.place(x=195, y=50)
output_entry.place(x=15, y=100)
clear_button.place(x=195, y=150)
choose_image_button.place(x=15, y=200)

#button config
choose_image_button.config(command=load_image)
continue_button.config(command=print_sku)
clear_button.config(command=clear_fields)

root.mainloop()