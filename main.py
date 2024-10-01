import sys # only use it for the function:      sys.stdout.write()
import os  # only get sued for:     os.get_terminal_size().columns     and     os.get_terminal_size().lines

COLOR_BLACK="\033[0;30m"
COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_BROWN="\033[0;33m"
COLOR_BLUE="\033[0;34m"
COLOR_PURPLE="\033[0;35m"
COLOR_CYAN="\033[0;36m"
COLOR_LIGHT_GRAY="\033[0;37m"
COLOR_DARK_GRAY="\033[1;30m"
COLOR_LIGHT_RED="\033[1;31m"
COLOR_LIGHT_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_LIGHT_BLUE="\033[1;34m"
COLOR_LIGHT_PURPLE="\033[1;35m"
COLOR_LIGHT_CYAN="\033[1;36m"
COLOR_LIGHT_WHITE="\033[1;37m"
COLOR_BOLD="\033[1m"
COLOR_FAINT="\033[2m"
COLOR_ITALIC="\033[3m"
COLOR_UNDERLINE="\033[4m"
COLOR_BLINK="\033[5m"
COLOR_NEGATIVE="\033[7m"
COLOR_CROSSED="\033[9m"

BG_COLOR_BLACK = "\033[40m"
BG_COLOR_RED = "\033[41m"
BG_COLOR_GREEN = "\033[42m"
BG_COLOR_BROWN = "\033[43m"  
BG_COLOR_BLUE = "\033[44m"
BG_COLOR_PURPLE = "\033[45m"
BG_COLOR_CYAN = "\033[46m"
BG_COLOR_LIGHT_GRAY = "\033[47m"
BG_COLOR_DARK_GRAY = "\033[100m"  # ANSI code for bright black (dark gray)
BG_COLOR_LIGHT_RED = "\033[101m"
BG_COLOR_LIGHT_GREEN = "\033[102m"
BG_COLOR_YELLOW = "\033[103m"
BG_COLOR_LIGHT_BLUE = "\033[104m"
BG_COLOR_LIGHT_PURPLE = "\033[105m"
BG_COLOR_LIGHT_CYAN = "\033[106m"
BG_COLOR_LIGHT_WHITE = "\033[107m"

# Text styles (already provided, just including for reference)
COLOR_BOLD = "\033[1m"
COLOR_FAINT = "\033[2m"
COLOR_ITALIC = "\033[3m"
COLOR_UNDERLINE = "\033[4m"
COLOR_BLINK = "\033[5m"
COLOR_NEGATIVE = "\033[7m"
COLOR_CROSSED = "\033[9m"

# Reset to default colors
COLOR_RESET = "\033[0m"

class Player:
    def __init__(self, Name: str, Icon: str) -> None:
        self.Name = Name
        self.Icon = Icon


class Board:
    Spaces: list[list[bool]] = [[False, False, False],
                                [False, False, False],
                                [False, False, False]]


class Game:
    Players: list[Player] # usealy just to people, but this could be fun later if 
    # Spaces contain ht einfoamation how a players board is filled out
   
    
    def PrintBoard(self):
       for x in self.Spaces:
           if x != 0:
               print("fuck you")

# moves the cursor, to a location in the terminal
def movecursor(y, x):
    print("\033[%d;%dH" % (y, x))


def WipeScreen():
    movecursor(0,0)
    sys.stdout.write(" " * os.get_terminal_size().columns * os.get_terminal_size().lines)
    movecursor(0,0)


def RenderBoard(Width, Height):
    BoardStringLight = [
    "┌──────────────┬──────────────┬──────────────┐\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "├──────────────┼──────────────┼──────────────┤\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "├──────────────┼──────────────┼──────────────┤\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "│              │              │              │\n",
    "└──────────────┴──────────────┴──────────────┘\n"]

    Number1String = [
    " _ ",
    "/ |",
    "| |",
    "| |",
    "|_|"]

    Number2String = [
    " ____  ",
    "|___ \ ",
    "  __) |",
    " / __/ ",
    "|_____|"]

    Number3String = [
    " _____ ",
    "|___ / ",
    "  |_ \ ",
    " ___) |",
    "|____/ "]

    Number4String = [
    " _  _   ",
    "| || |  ",
    "| || |_ ",
    "|__   _|",
    "   |_|  "]

    Number5String = [
    " ____  ",
    "| ___| ",
    "|___ \ ",
    " ___) |",
    "|____/ "]

    Number6String = [
    "  __   ",
    " / /_  ",
    "| '_ \ ",
    "| (_) |",
    " \___/ "]

    Number7String = [
    " _____ ",
    "|___  |",
    "   / / ",
    "  / /  ",
    " /_/   "]

    Number8String = [
    "  ___  ",
    " ( _ ) ",
    " / _ \ ",
    "| (_) |",
    " \___/ "]

    Number9String = [
    "  ___  ",
    " / _ \ ",
    "| (_) |",
    " \__, |",
    "   /_/ "]


    movecursor(7,0)
    Space = ((int(Height/2))-15)
    sys.stdout.write((" "*Width)*Space)
    

    for x in BoardStringLight:
        sys.stdout.write(" " * int(((Width - 46) / 2)) + x )
    
    #                _   ____    _____   _  _     ____     __     _____    ___     ___  
    #  ___   __  __ / | |___ \  |___ /  | || |   | ___|   / /_   |___  |  ( _ )   / _ \ 
    # / _ \  \ \/ / | |   __) |   |_ \  | || |_  |___ \  | '_ \     / /   / _ \  | (_) |
    #| (_) |  >  <  | |  / __/   ___) | |__   _|  ___) | | (_) |   / /   | (_) |  \__, |
    # \___/  /_/\_\ |_| |_____| |____/     |_|   |____/   \___/   /_/     \___/     /_/ 
                                                                               

def PrintStartScreen(Width: int):
    sys.stdout.write(COLOR_LIGHT_BLUE)

    ### This is only done with list and manual adding of spaces to center the text, if the ofset should be change later in the project idk.
    WelcomeStringList: list[str] = [" ______   __     ______        ______   ______     ______        ______   ______     ______    ",
                                    '/\__  _\ /\ \   /\  ___\      /\__  _\ /\  __ \   /\  ___\      /\__  _\ /\  __ \   /\  ___\   ',
                                    '\/_/\ \/ \ \ \  \ \ \____     \/_/\ \/ \ \  __ \  \ \ \____     \/_/\ \/ \ \ \/\ \  \ \  __\   ',
                                    '   \ \_\  \ \_\  \ \_____\       \ \_\  \ \_\ \_\  \ \_____\       \ \_\  \ \_____\  \ \_____\ ',
                                    '    \/_/   \/_/   \/_____/        \/_/   \/_/\/_/   \/_____/        \/_/   \/_____/   \/_____/ ']
    WelcomeString: str = ""
    SeparetorCount: int = int((Width - len(WelcomeStringList[0])) / 2)
    ColorList: list[str] = [COLOR_BLUE, COLOR_GREEN, COLOR_LIGHT_RED, COLOR_LIGHT_PURPLE, COLOR_CYAN]
    i = 0
    for x in WelcomeStringList:
        WelcomeString = WelcomeString + (" " * SeparetorCount) + ColorList[i] + x + "\n"
        i = i + 1 

    ## By now nothing on the screen is printed, but wipping for making sure no shell output wont fuck with the game
    WipeScreen()
    # after printing the string made above 
    sys.stdout.write(WelcomeString)
    sys.stdout.write('—' * Width )


def GameLoop():
    Screen_width = os.get_terminal_size().columns
    Screen_Height = os.get_terminal_size().lines
    PrintStartScreen(Screen_width)
    sys.stdout.write(COLOR_CYAN)

    Human = True
    
    # This loops until player deside to player ither by another person or internal bot
    PlayersKnown: bool = False
    movecursor(7,0)
    while PlayersKnown == False:
        playeramountstring = input("Do you like to play with human or bot? (h/b): ")
        if playeramountstring == "h":
            PlayersKnown = True
        elif playeramountstring == "b":
            Human = False
            PlayersKnown = True
        
    if Human == True: # do something becarse human idk
        print("hello world")
    else:
        print("i dont supprt bot at this time, sorry")
    # Print the size of terminal

    RenderBoard(Screen_width, Screen_Height)

    


if __name__=="__main__":
    GameLoop()
 