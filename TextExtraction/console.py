import os
import datetime
import sys
import json
import pytess_extract as tess
# import gcv_extract as gcv
import dateparser as dp
from dateparser.search import search_dates

YYYYMMDD = "%Y-%m-%d"

class Receipt:
    def __init__(self, date=datetime.datetime(1,1,1), vendor="undefined", amount=0):
        self.date = date
        self.vendor = vendor
        self.amount = amount

    def __str__(self):
        return f"DATE: {self.date.strftime(YYYYMMDD)} VENDOR: {self.vendor} AMOUNT: ${self.amount}"

    def __eq__(self, other):
        return self.date == other.get_date and self.vendor == other.get_vendor and self.amount == other.get_amount

    def set_date(self, date):
        self.date = date

    def set_vendor(self, vendor):
        self.vendor = vendor

    def set_amount(self, amount):
        self.amount = amount

    def get_date(self, want_str=False):
        return self.date

    def get_date_str(self):
        return self.date.strftime(YYYYMMDD)

    def get_vendor(self):
        return self.vendor

    def get_amount(self):
        return self.amount

    def to_json(self):
        data = {"date": self.date.strftime(YYYYMMDD), # pass YYYY-MM-DD string
                "vendor": self.vendor,
                "amount": self.amount}
        json_data = json.dumps(data)
        return json_data

def build_receipt(text):
    date = get_date(text)
    vendor = get_vendor(text)
    amount = get_amount(text)
    return Receipt(date, vendor, amount)

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


def console_test():
    """
    Run when you want to interact with the console and provide input to choose
    """
    files = []
    img_folder = os.listdir(tess.path)
    for img_name in img_folder:
        files.append(img_name)
    files = only_images(files)
    #print("Here are the files available:")
    #for i in range(len(files)):
    #    print(f"({i}) {files[i]}", sep="\n")
    #print()

    inp = input("Choose a file to extract or extract (all)\n")
    if (inp.lower() != "all"):
        inp = int(inp)
        files = [files[inp]]

    texts = extract_text(files)

    receipts = []
    for text in texts:
        receipt = Receipt(date=get_date(text), vendor="undefined", amount=get_amount(text))
        receipts.append(receipt)
    #for receipt in receipts:
        #print(receipt)


def extract_text(filenames):
    """
    Prints out the text of the file provided to either PyTesseract or Google Cloud Vision
    Returns a list of long strings of receipts, not individual words
    """
    filenames = only_images(filenames)
    # print(f"filenames in extract_text:\n{filenames}")
    receipts = []
    for filename in filenames:
        extract = tess.get_text(filename)
        # print(f"{filename} text after extract:\n{extract}")
        receipts.append(extract)
    # print(f"receipts:\n{receipts}")
    return receipts


def get_date(text):
    """
    Return a datetime object of the first full date in text. Return today's date on fail.
    Ex. >>> dateparser.parse('12/12/12')
        datetime.datetime(2012, 12, 12, 0, 0)
    """
    # print(f"text in get_date:\n{text}")
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
            # print(f"dateparsed: {date_parsed} type: {type(date_parsed)}")
            if(date_parsed != None and date[1].year > 2000 and date[1].year <= datetime.date.today().year):
                return date_parsed
    except:
        print("We didn't catch the right date")
    return datetime.date.today()


def get_vendor(text):
    """
    Input: a string of text containing the receipt information
    Output: a string of text referring to the vendor
    """
    words = text.split()
    vendor = ""
    i = 0
    while(words[i].rstrip(":.").isalpha() and i < len(text)):
        vendor = " ".join([vendor, words[i].rstrip(":.")])
        i += 1
    return vendor


def get_amount(text):
    amount = tess.get_total(text)
    return amount


def main():
    """
    * Read image filenames from the command line
    * Convert images to text
    * Build Receipt(date, vendor, amount) objects from text
    * Return json object: {"date":YYYY-MM-DD, "vendor":vendor_name, "amount":XX.XX}
    """
    filenames = sys.argv[1:]
    if(len(sys.argv) == 1):
        return

    filenames = only_images(filenames)
    receipts = []
    texts = extract_text(filenames)

    for i in range(len(texts)):
        text = texts[i]
        filename = filenames[i]
        receipt = Receipt(date=get_date(text),vendor=get_vendor(text),amount=get_amount(text))
        receipts.append(receipt)
        print(f"Receipt text:\n>\n{text}\n<")
        print(f"{filename} receipt contents:\n{receipt}")
    return receipts[0].to_json()

main()
# print("*"*10,"NOW SWITCHING TO CONSOLE","*"*10)
# console_test() # Run this if you want to manually choose files

