from random import randint
from colorama import Fore, Back, Style
from os import system, name
import sys, tty, termios

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
    with open("texts.txt") as f:
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

    errors = 0
    correct = True
    idx = 0
    while idx < len(text):
        clearScreen()
        displayText(text, idx, correct)
        character = getch()
        if character == text[idx]:
            correct = True
            idx += 1
        else:
            errors += 1
            correct = False

    print(f"WPM: {6969}")
    print(f"Accuracy: {(1 - errors / len(text)) * 100}%")

if __name__ == "__main__":
    run()