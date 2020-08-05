import cv2
import pytesseract
import os

path = os.getcwd()
img_folder = os.listdir(path+"/TextExtraction/images")

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
            split = img_text.split()

            print("-" * 20)  # Separator, delete if unnecessary
            get_total(split)
            print("-" * 20)
            get_company(split)
            print("-" * 20)
        except:
            print(img_name, " image object unsupported")
    return receipts


def get_total(split) -> float:
    # testing prints
    print("-" * 20)
    print('SPLIT HERE:')
    print(split)
    print("-" * 20)

    for item in reversed(split):
        # we identify the total amount by checking for the last '.' token
        if '.' in item:
            print(f'found item: {item}')
            # get rid of all characters that are not a number or '.'
            # then return the cleaned total
            total = ''
            for c in item:
                print(f'--- loop: {c}')
                if c == '.' or (47 < ord(c) < 58):
                    print(f'--- loop: add {c}')
                    total += c
            total = round(float(total), 2)
            print(f'total: {total}')
            return total
    return -1


#print(os.listdir(os.getcwd()+"/images"))

def get_company(split) -> str:
    # we identify a company name by checking from the top
    # for letters until we read in a character that is not a letter
    company = []
    # we keep a boolean to see if we've already started
    # seeing the company name
    hit = False
    for item in split:
        item = item.replace(':', '')
        # if we haven't seen the company name yet
        # and we hit an alpha char
        # then add it to the company name
        if not hit:
            if item.isalpha():
                hit = True
                company.append(item)
        # if we have already started building the company name
        # then check if this item is non alpha
        # if it isn't, then we break
        # otherwise, we add it to the company name
        else:
            if not item.isalpha():
                break
            else:
                company.append(item)
    company = " ".join(company)
    print(f'company: {company}')
    return company


print(os.listdir(os.getcwd() + "/TextExtraction/images"))
