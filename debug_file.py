import easyocr

reader = easyocr.Reader(['en'])

#result = reader.readtext('/home/aiden/RIM/IMG_2900.jpeg')
result = reader.readtext('/home/aiden/RIM/IMG_2901.jpeg')

print(result)