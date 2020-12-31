from Board import Board
import os
import sys

CTRL_C = "\x03"
if sys.platform.startswith("win"):
    import msvcrt
    WINDOWS = True
    ESCAPE_SEQUENCE = "\xe0"
    ARROW_CODES = {"H": "w", "P": "s", "M": "d", "K": "a"}
else:
    from subprocess import Popen, PIPE
    WINDOWS = False
    ESCAPE_SEQUENCE = "\x1b"
    ARROW_CODES = {"A": "w", "B": "s", "C": "d", "D": "a"}


# Waits for a single character of input and returns the string
# "left", "down", "right", "up", "exit", or None.
def getInput():
    if WINDOWS:
        key = msvcrt.getwch()
        if key == ESCAPE_SEQUENCE:
            character = msvcrt.getwch()
            return ARROW_CODES.get(character)
        elif key in ('rwasd'):
            return key
        elif key == CTRL_C:
            return "exit"
    else:
        original_terminal_state = None
        try:
            original_terminal_state = Popen("stty -g", stdout=PIPE, shell=True).communicate()[0]
            # Put the terminal in raw mode so we can capture one keypress at a time
            # instead of waiting for enter.
            os.system("stty raw -echo")
            key = sys.stdin.read(1)
            # The arrow keys are read from stdin as an escaped sequence of 3 bytes.
            if key == ESCAPE_SEQUENCE:
                # The next two bytes will indicate which arrow key was pressed.
                character = sys.stdin.read(2)
                return ARROW_CODES.get(character[1])
            elif key in 'rwsad':
                return key
            elif key == CTRL_C:
                return "exit"
        finally:
            os.system(b"stty " + original_terminal_state)
    return None


b = Board(10, 10)

if sys.stdout.isatty():
    while True:
        key = getInput()
        if not key or key == "exit":
            print("exiting")
            break
        if b.play(key):
            break
else:
    while True:
        inp = input('Enter a direction (wasd): ')
        if inp == 'exit' or b.play(inp):
            break
