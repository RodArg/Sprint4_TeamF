import cv2
import pytesseract
import os

path = os.getcwd()
img_folder = os.listdir(path+"/images")

# Single file test
img = cv2.imread("images/text1.png")
text = pytesseract.image_to_string(img)
print("images/text1.png:", text)

def get_text(images):
    for img_name in images:
        print("Looking at:", img_name)
        img_name = "images/"+img_name
        try:
            img = cv2.imread(img_name)
            text = pytesseract.image_to_string(img)
            print(img_name, ":", text)
            print("-"*20)
        except:
            print(img_name, " image object unsupported")

print(os.listdir(os.getcwd()+"/images"))
