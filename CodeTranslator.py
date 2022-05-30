# Text To Morse Code
# 
# Author:   Miska Rihu 
# Date:     2022-05-30
#
##############################################################################
# Imports
import sys

import msg
import err


##############################################################################
# Global Constants

# timings
dot = 1             
dash = 3 * dot      
space1 = dot        # space between parts of the same letter
space2 = 3 * dot    # space between two different letters
space3 = 7 * dot    # space between words

# Special Characters
INVALID_CHAR = '?'
VALID_SYMBOLS = []
VALID_CODES = []
DELIMITER = ";"

ERROR = "[ERROR]"
INFO = "[INFO]"
WARNING = "[WARN]"


##############################################################################
# Functions

# Custom print functions
def pinfo(text):
    print("{0}\t{1}".format(INFO, text))


def pwarn(text):
    print("{0}\t{1}".format(WARNING, text))


def perror(text, exception):
    print("{0}\t{1}: {2}".format(ERROR, text, exception))


# Configuration loading
def loadSymbols():
    count = 0

    filename = "symbols.csv"
    pinfo(msg.INF_LOADING_SYMBOLS.format(file=filename))
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for row in file:
                columns = row[:-1].split(DELIMITER)
                VALID_SYMBOLS.append(columns[0])
                VALID_CODES.append(columns[1])
                count += 1
    except FileNotFoundError as e:
        perror(msg.ERR_CANNOT_OPEN_FILE.format(file=filename), e)
        print(msg.PROVIDE_SYMBOLS_FILE)
        input(msg.PRESS_ENTER_TO_QUIT)
        sys.exit(err.FAILED_TO_LOAD_SYMBOLS)

    pinfo(msg.INF_LOADED_SYMBOLS.format(count=count, file=filename))


# Program functionality
def mainMenu():
    min = "0"
    max = "2"

    print("Main Menu:")
    print("1) Translate text into morse code")
    print("2) Translate morse code into text (not implemented)")
    print("0) Quit")
    selection = input("Selection: ")

    while (True):
        if (min <= selection <= max):
            break
        selection = input(msg.ERR_UNKNOWN_SELECTION)

    return selection


def validCharacter(char):
    return char in VALID_SYMBOLS


def characterToMorse(char):
    index = VALID_SYMBOLS.index(char)
    code = VALID_CODES[index]
    return code


def translateToMorse(text):
    invalid_char_count = 0
    text_words = text.split(" ")
    morse_words = []

    for text_word in text_words:
        morse_chars = []
        text_chars = list(text_word)
        position = 0

        while (position < len(text_chars)):
            char = text_chars[position]

            if not (validCharacter(char)):
                invalid_char_count += 1
                text_chars.pop(text_chars.index(char))
                morse_chars.append(INVALID_CHAR)
                continue
            else:
                morse_chars.append(characterToMorse(char))

            position += 1
        
        morse_words.append((text_chars, morse_chars))

    if (invalid_char_count > 0):
        pwarn(msg.WRN_INVALID_CHARS_DETECTED.format(count=invalid_char_count, replace_with=INVALID_CHAR))

    return morse_words


def printMorse(text_and_codes):
    for pair in text_and_codes:
        print()
        text_chars = pair[0]
        morse_chars = pair[1]
        for i in morse_chars:
            print(i, end="\t")


def textToMorse():
    print()
    print("Enter text to translate into morse code.")
    print("Valid characters are the letters a-z (either in lower or upper case), numbers 0-9, and the space.")
    print("Invalid characters will be denoted with '{0}' in the final output.".format(INVALID_CHAR))
    text = input("> ").upper()
    text_and_codes = translateToMorse(text)
    print()
    print("'{0}' in morse code is as follows.".format(text))
    print("Spaces are denoted with line breaks.")
    printMorse(text_and_codes)



##############################################################################
# Main Program

def main():
    loadSymbols()
    print()

    while (True):
        selection = mainMenu()

        if (selection == "0"):
            # Quit.
            break
        elif (selection == "1"):
            # Convert text into morse code.
            textToMorse()
        elif (selection == "2"):
            # Convert morse code into text.
            print("Sorry but this feature is not implemented yet.")

        print()
        print()
        print()

    print("Thank you for using the program.")


##############################################################################
# Run Main Program

main()

##############################################################################
# EOF