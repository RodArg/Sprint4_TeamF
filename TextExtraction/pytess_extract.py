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
            get_total(img_text)
            print("-"*20)
        except:
            print(img_name, " image object unsupported")
    return receipts


def get_total(img_text) -> float:
    split = img_text.split()

    # testing prints
    print("-" * 20)
    print('SPLIT HERE:')
    print(split)
    print("-" * 20)

    for item in reversed(split):
        # we identify the total amount by checking for
        # a $ and a decimal number
        if '.' in item and '$' in item:
            print(f'found item: {item}')
            # get rid of all characters that are not a number or '.'
            # then return the cleaned total
            total = ''
            for c in item:
                print(f'--- loop: {c}')
                if c == '.' or (ord(c) > 47 and ord(c) < 58):
                    print(f'--- loop: add {c}')
                    total += c
            total = round(float(total), 2)
            print(f'total: {total}')
            return total
    return -1


print(os.listdir(os.getcwd()+"/images"))
