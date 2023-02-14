import sys, tty, termios
from random import randint
from colorama import Fore, Back, Style
from os import system, name
from time import time

TABS = "\t\t\t\t"
SPACE = chr(32)
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
    keyb_uppercase = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '=', '«', '»', 'DEL'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '?', "'", '*', '_', '-'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', ',', '"', 'SPACE'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '[', ']', '.', '(', ')']
    ]

    keyb_lowercase = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '=', '«', '»', 'DEL'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '?', "'", '*', '_', '-'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', ',', '"', 'SPACE'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', '[', ']', '.', '(', ')']
    ]

    # Figure out which of these to use
    layout = keyb_uppercase \
        if (typed is None or typed.isupper() and typed not in [SPACE, BACKSPACE] ) \
        else keyb_lowercase
    
    # Special cases for SPACE and BACKSPACE
    if typed == SPACE:
        if typed == correct:
            correct = typed = 'SPACE'
        else:
            typed = 'SPACE'
    elif typed == BACKSPACE:
        typed = 'DEL'
    
    # Change current key color
    if typed == 'DEL':
        key_color = Back.WHITE
    elif typed == correct:
        key_color = Back.GREEN
    else:
        key_color = Back.RED
    key_color += Fore.BLACK

    # Just for new line
    print()
    for line in layout:
        if typed in line:
            line[line.index(typed)] = key_color + typed + Style.RESET_ALL
        print(TABS + " ".join(line))

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