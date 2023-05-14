from PIL import Image, ImageGrab, PngImagePlugin, ImageFilter
from time import sleep
import argparse
import os
import pytesseract # OCR, get TEXT(str) from PIL.ImageGrab obj.
import sys

# Consider reducing sleeptime
SLEEPTIME = 4
# Clipboard saves PngImageFiles
clipboard = None
# Compiled by Steam community: https://steamcommunity.com/sharedfiles/filedetails/?id=2645422003
interests_dict = {
    "Family and Relationships": ['Dating','Family','Fatherhood','Friendship','Marriage','Motherhood','Parenting','Weddings'],
    "Shopping and Fashion": ['Clothing','Cosmetics','Coupons','Dresses','Fragrances','Handbags','Jewelry','Malls','Shoes','Sunglasses','Tattoos','Toys'],
    'Food and Drink': ['Baking','Barbecue','Beer','Chocolate','Coffee','Coffeehouses','Desserts','Juice','Pizza','Recipes','Tea','Veganism','Wine'],
    "Business": ['Advertising','Agriculture','Architecture','Aviation','Banking','Business','Construction','Design','Economics','Engineering','Design','Entrepreneurship','Finance','Investment','Insurance','Management','Marketing','Online','Retail','Sales','Science'],
    "Entertainment": ['Bars','Books','Comics','Concerts','Dancehalls','Documentary','Festivals','Games','Literature','Magazines','Manga','Movies','Music','Newspapers','Nightclubs','Parties','Plays','Poker','Talkshows','Theatre']
}

def find_most_likely_phish(interest_list: list):
    """Computes the most likely Phishbook account type from a list of interests
    Argument: List of interests, ex. ['Marketing','Documentary','Engineering','Aviation','Literature','Business','Manga','Online','Construction','Plays']"""
    interest_count = {} # Count of target's interests, ex: {"Family and Relationships": 0, "Shopping and Fashion": 6, "Food and Drink": 4, "Business": 0, "Entertainment": 0}
    for interest_type in interests_dict: # This nested loop looks sloppy
        next_count = 0
        interest_values = interests_dict[interest_type]
        for interest in interest_values:
            if interest in interest_list:
                next_count += 1 # Found a match -> increment
        interest_count[interest_type] = next_count
        print(f"Target has {next_count} interests of type {interest_type}")
    sorted_interests = sorted(interest_count, key=interest_count.get, reverse=True)
    # Sort this dict by keys, set largest_interest to the key with the highest value.
    recommended_interest = [interest for interest in sorted_interests][0]
    print(f"The target's greatest interest is {recommended_interest}")

def phish_pngimage(image: PngImagePlugin.PngImageFile):
    """Runs OCR on image - Consider error handling
    Argument: image - PNGImageFile"""
    sharpened = image.filter(ImageFilter.SHARPEN)
    out = []
    for line in pytesseract.image_to_string(sharpened).split("\n"):
        # Add to new list only if its NOT end character added by tessaract
        if 1 < len(line):
            out.append(line)
    find_most_likely_phish(out)

def images_are_equal(imageA, imageB):
    """Tests whether images are equal"""
    return type(imageA) == PngImagePlugin.PngImageFile and type(imageB) == PngImagePlugin.PngImageFile and list(imageA.getdata()) == list(imageB.getdata())

def phish_file(filepath: str):
    """Runs phishing on input filepath"""
    if filepath == None:
        print("ERROR: Invalid filepath argument")
    with Image.open(filepath, mode="r") as image:
        phish_pngimage(image)

def recurse_dir(filepath: str):
    if os.path.isdir(filepath):
        inner_files = os.listdir(filepath)
        for nextfile in inner_files:
            nextpath = f"{filepath}/{nextfile}"
            recurse_dir(nextpath)
    elif os.path.isfile(filepath):
        phish_file(filepath)
    else:
        print("Cannot open input path " + filepath)

def phish_clipboard():
    """Phishes image on clipboard"""
    clip = ImageGrab.grabclipboard() # grab our clipboard
    if type(clip) == PngImagePlugin.PngImageFile: # is our clipboard a png image?
        if not images_are_equal(clip, clipboard):  # if the image we just grabbed from clipboard is still saved to our global clipboard var, it doesn't need to be processed again.
            clipboard = clip # update our global var
            phish_pngimage(clip)
    elif clip is not None:
        print(f"WARNING: Clipboard has unexpected content of type {type(clip)}")

def clipboard_loop():
    """Loop through and handle images on clipboard"""
    print("Waiting for image on clipboard...")
    while True:
        phish_clipboard()
        sleep(SLEEPTIME)

def main():
    """Main method - Loops and handles screenshots"""
    parser = argparse.ArgumentParser("Parses screenshots and computes most likely Phishbook category for a target")
    parser.add_argument("-c", action="store_true", dest="clipboard_mode")
    parser.add_argument("filepaths", action="store", default=[], nargs="*")
    args = parser.parse_args()
    for filepath in args.filepaths:
        recurse_dir(filepath)
    if args.clipboard_mode:
        clipboard_loop()
    exit(0)

if __name__ == "__main__":
    main()
