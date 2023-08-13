# hacker-sim-scripts

#### What are these?

These are scripts for the game "Hacker Simulator", sold on [Steam](https://store.steampowered.com/app/1754840/Hacker_Simulator/) and developed by Save All Studios.

These scripts are not ran ingame, rather they are external scripts that aid in, or automate gameplay. This readme assumes readers are already familiar with game mechanics, if you are not you may find [this steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2645422003) helpful.

# hackersim_auto_phish.py
#### What does this do?

This script reads images of a target _Phishbook_ profile. The images are parsed to compute which type of _Phishbook_ account you need to purchase and to execute a phishing attack against the target. The game designers intended this to be done by hand, counting your targets interests abd guessing the correct account type. This script does the guesswork for you, which seems quite fair for Hacker Simulator.

#### How does it work?
The easiest method Deconkle (original developer) could come up with to parse target interests using python is to take a windows screenshot ( WIN + SHIFT + S or Print Screen ) and draw the box around their interests. Python reads the PNG image from the command-line or clipboard and sharpens the image so Google's **Tesseract** OCR module can reliably convert the text in image to a string. The image is parsed into a list of strings. Finally, the strings are parsed and compared to the master list of all possible interests to compute the most likely phishing attack method.

#### Examples
One option is to take the screenshots, save them to file, and pass the file paths on the command-line.

The other is to run the script with -c, then take a screenshot of ***just*** the targets interest (as shown in red below). The python script will then print the account type needed for a successful phish. 
![20220324083101_1_fishbook_crop](https://user-images.githubusercontent.com/24526230/160257747-3cf6f54c-554e-4de1-8e99-daaced3c19c8.jpg)

The command-line output will be similar to:
![image](https://user-images.githubusercontent.com/24526230/160290217-7341cbe1-2938-4ed2-b480-e1049ad55b0d.png)

## Installation

Install [Python 3.x](https://www.python.org/downloads/) if you don't have it already.

Download the python script from this repository.

Install Google's [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract#installing-tesseract) and [add it to PATH](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

Using [Pythons Package Installer (PIP)](https://pip.pypa.io/en/stable/getting-started/), install Pillow (aka PIL) and pytesseract

``pip install Pillow``

``pip install pytesseract`` 

Test with pytest:

``pip install pytest``

## Usage
Run the script in a terminal/cmd window using ``py path/to/hackersim_auto_phish.py [filepaths]``. It helps to have this running on another monitor, or otherwise visible along with Hacker Simulator. The script opens input filepaths, reports the most likely phishing attack for each image, then exits.

Options:

-h: Displays help

-c: Clipboard mode (previous behavior) - Waits for and processes images passed to the clipboard. Exit using CTRL + C.

### NOTICE
Taking screenshots via the method described above is a pain in the ass when the game is in fullscreen. There is no option ingame to change out of fullscreen, but you can force it using the windows keybind ALT + ENTER ingame. Then you can change to fullscreen-borderless-windowed by changing to your desired resolution in Graphics options.

A simpler approach is to take screenshots with Print Screen, save it to file, and pass the path on the command-line.
