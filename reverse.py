### Version 1.0 ### Find SKU From Image ###

##install pillow, pytesseract and re
import tkinter as tk
#import re
#from PIL import Image
#import pytesseract

#variables
root = tk.Tk()
continue_button = tk.Button(root, text="continue")
clear_button = tk.Button(root, text="clear")
image_entry = tk.Entry(root) ## may need to change for pillow
output_entry = tk.Entry(root) 


#window config
root.title("Find SKU Code")
root.geometry("600x350")
root.resizable(False, False)

#functions
def load_image():
    pass

def extract_text():
    pass

def find_sku():
    pass

def print_sku():
    pass


#layout
tk.Label(root, text="Insert image").place(x=15, y=25)
image_entry.place(x=15, y=50) ## may need to change for pillow
continue_button.place(x=195, y=50)
output_entry.place(x=15, y=100)
clear_button.place(x=195, y=100)


root.mainloop()