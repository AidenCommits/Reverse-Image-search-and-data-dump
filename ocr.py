import re
import numpy as np
import easyocr

reader = easyocr.Reader(['en'])
#selected_image = load_image()
#selected_image_path = None

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
    text = text.upper()
    text = text.replace("*", "#")

    print("Extracted text: ")
    print((repr(text)))
    return text

def find_sku(text):
    
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
