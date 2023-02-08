import sys, tty, termios
from random import randint
from colorama import Fore, Back, Style
from os import system, name
from time import time

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

def displayText(text: str, current: int, status: bool) -> None:
    if status:
        print(text[:current] + Back.WHITE + Fore.BLACK + text[current] + 
        Style.RESET_ALL + Style.DIM + text[current+1:] + Style.RESET_ALL)
    else:
        print(text[:current] + Back.RED + text[current] + 
        Style.RESET_ALL + Style.DIM + text[1+current:] + Style.RESET_ALL)

def run() -> None:
    text = pickText()
    wordCount = len(text.split())

    tic = 0.0
    errors = 0
    correct = True
    idx = 0
    while idx < len(text):
        clearScreen()
        print(f"Time: {round(time() - tic if tic > 0 else tic, 1)}\n")
        displayText(text, idx, correct)
        
        character = getch()
        if idx == 0 and correct:
            tic = time()

        if character == text[idx]:
            correct = True
            idx += 1
        else:
            errors += 1
            correct = False
    toc = time()

    print(f"WPM: {round(wordCount / ((toc - tic) / 60), 0)}")
    print(f"Accuracy: {round((1 - errors / len(text)) * 100, 1)}%")

if __name__ == "__main__":
    run()