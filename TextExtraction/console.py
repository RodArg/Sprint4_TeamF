import os
import pytess_extract as tess
import gcv_extract as gcv
path = os.getcwd()
img_folder = os.listdir(path+"/images")
def extract_tess():
    files = []
    for img_name in img_folder:
        files.append(img_name)
    print("files:", files)
    print("Here are the files available:")
    for i in range(1,len(files)):
        print("({}) {}".format(i, files[i]),end="; ")
    print()
    inp = input("Choose a file to extract or extract (all)")
    if (inp.lower() != "all"):
        inp = int(inp)
        files = files[inp]

    tool = input("GCV or Tess?")
    if(tool.lower() == "gcv"):
        gcv.detect_text(files,path)
    else:
        tess.get_text(files)


def extract_gcv():
    gcv.detect_text("sbucks_hk.jpg")

extract_gcv()



