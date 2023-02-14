import sys, tty, termios
from random import randint
from colorama import Fore, Back, Style
from os import system, name
from time import time

"""
TODO: 
    -- PUT THE LOGO IN A LIST OF STRINGS WHERE
    EACH LINE IS A STRING
"""
TABS = "\t\t\t\t"
ESCAPE = chr(27)
BACKSPACE = chr(127)
LOGO = f" _____                 _____\n\
|_   _|__ _ __ _ __ __|_   _|   _ _ __   ___\n\
  | |/ _ \\ '__| '_ ` _ \\| || | | | '_ \\ / _ \\\n\
  | |  __/ |  | | | | | | || |_| | |_) |  __/\n\
  |_|\___|_|  |_| |_| |_|_| \__, | .__/ \___|\n\
                            |___/|_|"

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def clearScreen() -> None:
    system('cls' if name == 'nt' else 'clear')

def pickText() -> str:
    with open("../docs/texts.txt") as f:
        lines = f.readlines()
        text = lines[randint(0, len(lines) - 1)]
        if text.endswith('\n'):
            text = text[:len(text) - 1]
        return text

def calculateWPM(word_count: int, elapsed_time: float) -> float:
    return round(word_count / ((elapsed_time) / 60), 0)

def calculateAccuracy(errors: int, n_chars: int) -> float:
    return round((1 - errors / n_chars) * 100, 1)

def displayStats(wpm: float, accuracy: float) -> None:
    print(f"\nWPM: {wpm}")
    print(f"Accuracy: {accuracy}%")

def displayTime(tic: float, toc: float) -> None:
    print(f"Time: {round(toc - tic if tic > 0 else tic, 1)}\n")

def displayWholeText(text: str) -> None:
    print(Fore.GREEN + text + Style.RESET_ALL)

def displayText(text: str, current: int, wrong_span: int) -> None:
    wrong_start = current - wrong_span

    if wrong_span == 0:
        disp = Fore.GREEN + text[:current]  + Back.WHITE + Fore.BLACK + text[current] + \
        Style.RESET_ALL + Style.DIM + text[current + 1:] + Style.RESET_ALL
    else:
        disp = Fore.GREEN + text[:wrong_start] + Style.RESET_ALL+ Back.RED + \
        text[wrong_start:wrong_start + wrong_span] + Style.RESET_ALL + Style.DIM + \
        text[wrong_start + wrong_span:] + Style.RESET_ALL
    print(disp)
"""
TODO:
    -- ADD KEYS FOR SPACE AND BACKSPACE

    -- ADD DIFFERENTIATION BETWEEN UPPER CASE 
    AND LOWER CASE 
"""
def displayKeyboard(typed: chr=None, correct: chr=None) -> None:
    # Set up keys
    keyb = f"\t\t\t\t1234567890-=\n{TABS}QWERTYUIOP?'\
        \n{TABS}ASDFGHJKL;,\"\n{TABS}ZXCVBNM[].()"
    keyb = list(keyb)

    # In case we haven't typed anything just yet
    if typed is None or typed.upper() not in keyb:
        print("\n " + " ".join(keyb))
        return
    
    # Normalize everything to upper case
    typed = typed.upper()
    correct = correct.upper()

    # Set background color: green if correct, red if wrong
    bg_color = Back.GREEN if typed == correct else Back.RED
    keyb[keyb.index(typed)] = bg_color + Fore.BLACK + \
        typed + Style.RESET_ALL
    
    print("\n " + " ".join(keyb))
    
"""
TODO:
    -- NEED TO REWRITE THE CODE I USE TO DETERMINE
    WHEN TO GO FORWARD IN INDEX, INCREASE WRONG
    COUNTER, ETC AS IT HAS GOTTEN TOO COMPLICATED 
    AND SPAGHETTIFIED AND IS NOW CAUSING ISSUES
    (NAMELY, IF THE LAST CHARACTER IS WRONG, IT GETS MESSY)

    -- 
"""
def run() -> None:
    text = pickText()
    tic = 0.0
    total_errors = 0
    curr_wrong = 0
    char = None

    idx = 0
    while idx < len(text) or curr_wrong > 0:
        clearScreen()
        print(LOGO)
        print("Press 'esc' to quit")
        displayTime(tic, time())
        displayText(text, idx, curr_wrong)
        displayKeyboard(char, text[idx - 1 if idx > 0 else 0])

        char = getch()
        if char == ESCAPE:
            quit()

        if idx == 0 and curr_wrong == 0:
            tic = time()

        if char == text[idx] and curr_wrong == 0:
            idx += 1
        elif curr_wrong > 0 and curr_wrong > 0 and char == BACKSPACE:
            curr_wrong -= 1
            if idx < len(text) - 1:
                idx -= 1
        elif char != BACKSPACE and curr_wrong < 7:
            if idx < len(text) - 1:
                idx += 1
                curr_wrong += 1
            elif idx < len(text) and curr_wrong < 1:
                curr_wrong = 1
            total_errors += 1
    toc = time()
    clearScreen()
    print("Finished!")
    displayTime(tic, time())
    displayWholeText(text)
    displayKeyboard()

    displayStats(calculateWPM(len(text.split()), toc - tic), 
        calculateAccuracy(total_errors, len(text)))
if __name__ == "__main__":
    run()