import cv2
import pytesseract
import os
from statistics import mode
from googletrans import Translator

translator = Translator()


def set_path():
    """
    Detect and set proper path based on current directory
    """
    path = os.getcwd()

    if (path[-14:] == "TextExtraction"):
        return os.path.join(path, "images")  # When inside the IDE
    return os.path.join(path, "TextExtraction", "images")  # When inside the command line


path = set_path()


# print(f"path: {path}")

def get_language(text):
    """
    Input: A single string of text in an identifiable language
    Output: a two-char string language identifier (en = english, de = deutsch, etc.)
    """
    print(f"text in get_language:\n{text}")
    text = text.split()
    # print(f"text after split:\n{text}")
    text.reverse()
    # print(f"text after reverse:\n{text}")
    languages = translator.detect(text[:len(text) // 4])  # Parsing the whole text is slow so we only look at 1/4th

    for i in range(len(languages)):
        languages[i] = languages[i].lang  # languages[i] are language objects, .lang is a string
    language = mode(languages)
    print(f"language: {language}")
    return language


def translate_words(text, language=""):
    """
    Input:
        text: List of strings
        language: two-char string language symbol (en, fr, cn, etc) of source text
    Output: list of strings translated to english
    """
    if (language == ""):
        language = get_language(text)

    text = text.split()
    translations = translator.translate(text, src=language, dest='en')
    translated_text = []

    for translation in translations:
        translated_text.append(translation.text)

    return translated_text


def get_text(img_name):
    """
    Input: The name of the image to be converted to text
    Output: A list of strings of images converted to text
    """
    print("Looking at:", img_name)
    try:
        img_path = os.path.join(path, img_name)
        # print(f"img path: {img_path}")
        img = cv2.imread(img_path)
        img_text = pytesseract.image_to_string(img)

        print(f"{img_name} text in get_text:\n{img_text}")
        print("-" * 20)  # Separator, delete if unnecessary
        # get_total(img_text)
        print("-" * 20)
        print(f"file {img_name} text right before returning:\n{img_text}")
        return img_text
    except:
        print(img_name, " image object unsupported")


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
        if '.' in item:
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
