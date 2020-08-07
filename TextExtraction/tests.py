import os
import pytess_extract as tess
import console as cons

# Run from /TextExtraction directory
imagepath = tess.set_path()
testfile = "test.txt"
def doublecheck(name, data):
    ans = input(name+f": >{data}< change? (y/n)\n")
    if (ans.lower() == "y"):
        data = input(f"Input the {name} you want:\n")
    return data

def test_components(categories, receipt, receipt_test):
    fail = 0
    print(f"Testing {categories[0]}")

    receipt_date = receipt.get_date_str()
    receipt_test_date = receipt_test.get_date_str()
    receipt_vendor = receipt.get_vendor()
    receipt_test_vendor = receipt_test.get_vendor()
    receipt_amount = str(receipt.get_amount())
    receipt_test_amount = str(receipt_test.get_amount())

    if(receipt_date != receipt_test_date):
        print(f"Fail on {categories[1]}. Got {receipt_date} expected {receipt_test_date}")
        fail += 1
    if (receipt_vendor != receipt_test_vendor):
        print(f"Fail on {categories[2]}. Got {receipt_vendor} expected {receipt_test_vendor}")
        fail += 1
    if (receipt_amount != receipt_test_amount):
        print(f"Fail on {categories[3]}. Got {receipt_amount} expected {receipt_test_amount}")
        fail += 1
    if(not fail):
        print(f"Complete success.")
    print("-"*15)

def build(quick=False):
    categories = ["filename", "date", "vendor", "amount"]
    file = open(testfile, "w")
    file.write(",".join(categories)+"\n")
    filenames = os.listdir(imagepath)
    filenames = cons.only_images(filenames)
    texts = cons.extract_text(filenames)
    for i in range(len(texts)):
        receipt = cons.build_receipt(texts[i])

        date = receipt.get_date_str()
        vendor = receipt.get_vendor()
        amount = str(receipt.get_amount())

        if (not quick):
            date = doublecheck("date", date)
            vendor = doublecheck("vendor", vendor)
            amount = doublecheck("amount", amount)

            receipt.set_date(date)
            receipt.set_vendor(vendor)
            receipt.set_amount(amount)

        payload = ",".join([filenames[i],date,vendor,amount]) + "\n"
        print(f"{filenames[i]}:\n{receipt}")
        file.write(payload)
    file.close()
    print("done building test file")

def test():
    file = open(testfile, "r")
    categories = file.readline()[:-1].split(",")

    for line in file:
        words = line.split(",")
        filename = words[0]
        date = cons.datetime.datetime.strptime(words[1], cons.YYYYMMDD)
        vendor = words[2]
        amount = words[3][:-1]

        text = cons.extract_text([filename])[0]
        receipt = cons.build_receipt(text)
        receipt_test = cons.Receipt(date,vendor,amount)

        test_components(categories, receipt, receipt_test)

# build(quick=True)
test()


