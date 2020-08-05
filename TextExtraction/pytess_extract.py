import cv2
import pytesseract
import os
from statistics import mode
from googletrans import Translator

path = os.getcwd()
img_folder = os.listdir(path+"/TextExtraction/images") # Use this line when executing outside TextExtraction
# img_folder = os.listdir(path+"/images") # Use this line when running from IDE

translator = Translator()

def get_language(text):
    """
    Input: A single string of text in an identifiable language
    Output: a two-char string language identifier (en = english, de = deutsch, etc.)
    """
    text = text.split()
    text.reverse()
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
    if(language == ""):
        language = get_language(text)

    text = text.split()
    translations = translator.translate(text, src=language, dest='en')
    translated_text = []

    for translation in translations:
        translated_text.append(translation.text)

    return translated_text


def get_text(images):
    """
    Input: A list of filenames of images to be converted to text
    Output: A list of strings of images converted to text
    """
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
