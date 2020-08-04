import os
import pytess_extract as tess
#import gcv_extract as gcv
import dateparser as dp

path = os.getcwd()
img_folder = os.listdir(path+"/images")


## TODO:
# Extract the date
    # Try importing dateparser or datefinder and
    # https://github.com/scrapinghub/dateparser
    # https://github.com/akoumjian/datefinder
# Extract the category
    # P

def only_images(files):
    """
    Will return a list containing only .jpg, .png, and .jpeg
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
    """
    files = []
    for img_name in img_folder:
        files.append(img_name)
    # Get rid of non-image files
    files = only_images(files)
    # print("files:", files)
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
        gcv.detect_text(files, path+"/images/")
    else:
        tess.get_text(files)

def get_date(text):
    pass

def get_category(text):
    pass

# Run this to test out pytesseract or gcv on your images
extract_text()



