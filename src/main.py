import sys, tty, termios
from random import randint
from colorama import Fore, Back, Style
from os import system, name
from time import time

ESCAPE = chr(27)
BACKSPACE = chr(127)

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
        # text = lines[randint(0, len(lines) - 1)]
        # test line
        text = lines[17]
        if text.endswith('\n'):
            text = text[:len(text) - 1]
        return text

def displayText(text: str, current: int, wrong_start: int, wrong_span: int, status: bool) -> None:
    if status:
        print(text[:current] + Back.WHITE + Fore.BLACK + text[current] + 
        Style.RESET_ALL + Style.DIM + text[current+1:] + Style.RESET_ALL)
    else:
        print(text[:wrong_start] + Back.RED + text[wrong_start:wrong_start+wrong_span] + 
        Style.RESET_ALL + Style.DIM + text[wrong_start+wrong_span:] + Style.RESET_ALL)

"""
TODO:  
    - FIX ISSUE WHERE WHEN THE LAST FEW CHARACTERS ARE WRONG, IT
    DOESN'T ALLOW YOU TO MISTYPE FURTHER THAN THE PENULTIMATE 
    CHARACTER (IT SHOULD ALLOW YOU TO TYPE UNTIL THE LAST ONE)

    - FIX THE ISSUE WHERE WHEN YOU BACKSPACE AND DELETE THE MISTYPED
    CHARACTER, THERE'S NO CURSOR HIGHLIGHTING (SHOULD BE WHITE
    HIGHLIGHTING SINCE THERE ARE NO MORE WRONG CHARACTERS)
"""
def run() -> None:
    text = pickText()
    word_count = len(text.split())
    tic = 0.0
    errors = 0
    curr_wrong = 0
    correct = True
    wrong_idx = -1

    idx = 0
    while idx < len(text) or curr_wrong > 0:
        clearScreen()
        print("Press 'esc' to quit")
        print(f"Time: {round(time() - tic if tic > 0 else tic, 1)}\n")
        displayText(text, idx, wrong_idx, curr_wrong, correct)
        
        char = getch()
        if char == ESCAPE:
            quit()

        if idx == 0 and correct:
            tic = time()

        if char == text[idx] and curr_wrong == 0:
            correct = True
            idx += 1
        elif not correct and curr_wrong > 0 and char == BACKSPACE:
            curr_wrong -= 1
            idx -= 1
        elif char != BACKSPACE and curr_wrong < 7:
            if curr_wrong == 0:
                wrong_idx = idx
            if idx < len(text) - 1:
                idx += 1
                curr_wrong += 1
            errors += 1
            correct = False
    toc = time()

    print(f"WPM: {round(word_count / ((toc - tic) / 60), 0)}")
    print(f"Accuracy: {round((1 - errors / len(text)) * 100, 1)}%")

if __name__ == "__main__":
    run()