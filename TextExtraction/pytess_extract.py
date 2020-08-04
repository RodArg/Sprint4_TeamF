import cv2
import pytesseract
import os

path = os.getcwd()
img_folder = os.listdir(path+"/images")

# Single hardcoded file test
# img = cv2.imread("images/text1.png")
# text = pytesseract.image_to_string(img)
# print("images/text1.png:", text)


def get_text(images):
    receipts = []
    for img_name in images:
        print("Looking at:", img_name)
        try:
            img_path = "images/" + img_name
            img = cv2.imread(img_path)
            img_text = pytesseract.image_to_string(img)

            receipts.append(img_text)

            print(img_name, ":")
            print(img_text)
            print("-"*20)  # Separator, delete if unnecessary
        except:
            print(img_name, " image object unsupported")
    return receipts


print(os.listdir(os.getcwd()+"/images"))
