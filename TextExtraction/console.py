"""
## TODO:
# Extract the date
    # Done
# Extract the vendor
    # Company title
    # We have to figure out how to isolate the vendor
# Extract the payment
    # Done
"""
import os
import datetime
import sys
import pytess_extract as tess
# import gcv_extract as gcv
import dateparser as dp
from dateparser.search import search_dates


path = os.getcwd()
img_folder = os.listdir(path+"/TextExtraction/images") # Use this line when executing outside TextExtraction
# img_folder = os.listdir(path+"/images") # Use this line when running from IDE


class Receipt:
    def __init__(self, date="DD/MM/YYYY", vendor="undefined", amount=0):
        self.date = date
        self.vendor = vendor
        self.amount = amount

    def __str__(self):
        return "Date: {} Category: {} Amount: {}".format(self.date, self.vendor, self.amount)

    def set_date(self, date):
        self.date = date

    def set_vendor(self, vendor):
        self.vendor = vendor

    def set_amount(self, amount):
        self.amount = amount

    def get_date(self):
        return self.date

    def get_vendor(self):
        return self.vendor

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

    # tool = input("GCV or Tess?\n")
    # if (tool.lower() == "gcv"):
    #     receipts = gcv.detect_text(files, path+"/images/")
    # else:
    receipts = tess.get_text(files)
    if(len(receipts) == 1):
        return receipts[0]
    return receipts


def get_date(text):
    """
    Return a datetime object of the first full date in text. Return today's date on fail.
    """
    dates = []
    language = tess.get_language(text)
    # If the text isn't in english we have to translate each word
    # because translating the text as a whole changes the date format
    if(language != "en"):
        text = tess.translate_words(text, language)
        for word in text:
            date = search_dates(word)
            # date format: [('string', datetimeformat)]
            # we want the string hence [0][0]
            # and the string should be at least 'yymmdd' len (6) long
            if(date is not None and len(date[0][0]) >= 6):
                dates.append(date[0])
    else:
        dates = search_dates(text)
    try:
        for date in dates:
            # print(f"date: {date}")
            date_parsed = dp.parse(date[0], settings={'STRICT_PARSING': True, 'REQUIRE_PARTS': ['day', 'month', 'year'], 'PREFER_DATES_FROM': 'past', 'locale': 'de-AT'})
            # print(f"dateparsed: {date_parsed}")
            if(date_parsed != None and date[1].year > 2000 and date[1].year <= datetime.date.today().year):
                return date_parsed
    except:
        print("We didn't catch the right date")
    return datetime.date.today()


def get_vendor(text):
    pass


def get_amount(text):
    pass

# Main
text = extract_text()
print(f"text in main: {text}")
date = get_date(text)
print("date {}".format(date))
# vendor = get_vendor(text)
# amount = get_amount(text)
# receipt = Receipt(date, vendor, amount)

# Next steps
# Pass receipt var to a function that updates the database

