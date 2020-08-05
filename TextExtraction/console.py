import os
import pytess_extract as tess
#import gcv_extract as gcv
import dateparser as dp
from dateparser.search import search_dates
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
    """
    Return a datetime object of the first date in text
    """
    dates = search_dates(text)
    print("dates {}".format(dates))
    try:
        for date in dates:
            date_parsed = dp.parse(date[0], settings={'STRICT_PARSING': True, 'REQUIRE_PARTS': ['day', 'month', 'year'], 'PREFER_DATES_FROM': 'past'})
            # print("date_parsed: {}".format(date_parsed))
            # print("date.year: {}".format(date[1].year))
            # print("today.year: {}".format(datetime.date.today().year))
            if(date_parsed != None and date[1].year > 2000 and date[1].year <= datetime.date.today().year):
                return date_parsed
    except:
        print("We didn't catch the right date")
    return -1


def get_category(text):
    pass


def get_amount(text):
    pass

# Main
text = extract_text()
date = get_date(text[0])
if(date == -1):
    date = datetime.date.today()
print("date {}".format(date))
# category = get_category(text)
# amount = get_amount(text)
# receipt = Receipt(date, category, amount)

# Next steps
# Pass receipt var to a function that updates the database

