import os
import pytess_extract as tess
import gcv_extract as gcv
import dateparser as dp
import datetime

path = os.getcwd()
img_folder = os.listdir(path+"/images")

## TODO:
# Extract the date
    # Try importing dateparser or datefinder
        # Explore statements that find common formats (YYYY/MM/DD, YY-MM-DD, DD Month YY, etc)
    # https://github.com/scrapinghub/dateparser
    # https://github.com/akoumjian/datefinder
# Extract the category
    # Company title
    # We have to figure out how to isolate the category
# Extract the payment
    # Usually listed next to "Total"
    # Select a list of words we can parse for (e.g. Total, Subtotal, Check Amount)
    #   and get the first number with a decimal after that word


class Receipt:
    def __init__(self, date="DD/MM/YYYY", category="undefined", amount=0):
        self.date = date
        self.category = category
        self.amount = amount

    def __str__(self):
        return "Date: {} Category: {} Amount: {}".format(self.date, self.category, self.amount)

    def set_date(self, date):
        self.date = date

    def set_category(self, category):
        self.category = category

    def set_amount(self, amount):
        self.amount = amount

    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def get_amount(self):
        return self.amount


def only_images(files):
    """
    Takes a list of filenames, return a list of only .jpg, .png, and .jpeg filenames
    """
    img_files = []
    # print("files at first:", files)
    for filename in files:
        format = filename.split(".")[-1]
        # print("{} format: {}".format(filename, format))
        if(format == "jpg" or format == "png" or format == "jpeg"):
            img_files.append(filename)
    return img_files


def extract_text():
    """
    Prints out the text of the files provided to either PyTesseract or Google Cloud Vision
    Returns a list of long strings of receipts, not individual words
    """
    files = []
    for img_name in img_folder:
        files.append(img_name)
    files = only_images(files)

    print("Here are the files available:")
    for i in range(len(files)):
        print("({}) {}".format(i, files[i]),sep="\n")
    print()

    inp = input("Choose a file to extract or extract (all)\n")
    if (inp.lower() != "all"):
        inp = int(inp)
        files = [files[inp]]

    tool = input("GCV or Tess?\n")
    if (tool.lower() == "gcv"):
        receipts = gcv.detect_text(files, path+"/images/")
    else:
        receipts = tess.get_text(files)
    return receipts


def get_date(text):
    pass


def get_category(text):
    pass


def get_amount(text):
    pass

# Main
text = extract_text()
date = get_date(text)
category = get_category(text)
amount = get_amount(text)
receipt = Receipt(date, category, amount)

# Next steps
# Pass receipt var to a function that updates the database

