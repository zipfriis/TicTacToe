import os  # only get sued for:     os.get_terminal_size().columns     and     os.get_terminal_size().lines

highlight_start = "\033[1;37;44m"  # Bright white text on blue background
highlight_end = "\033[0m"  # Reset formatting

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

# moves the cursor, to a location in the terminal
def movecursor(y, x):
    print("\033[%d;%dH" % (y, x), end="")

def WipeScreen():
    movecursor(0,0)
    print(" " * os.get_terminal_size().columns * os.get_terminal_size().lines, end="")
    movecursor(0,0)


def AskForMove(Spaces: list[int], BoardLoacations: list[list[int]], Width, Height) -> int:
    OutputLocation = (BoardLoacations[0][0]-7)/2+7
    movecursor(OutputLocation, BoardLoacations[0][1])
    print("Please Pick a Space... ", end="")
    for x in Spaces:
        print(str(x) + ", ", end="")
    while True:
        Choise = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + " " * (Width - BoardLoacations[0][1] - 2)+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, Spaces)
        if Choise in StringSpaces:
            break
    # wipeping 
    movecursor(OutputLocation, 0)
    print(" "*Width, end="")
    movecursor(Height-1, Width)
    return Choise


def OptionMenu():
    # This loops until player deside to player ither by another person or internal bot
    movecursor(7,0)
    Human = True
    PlayersKnown: bool = False
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
    

def CheckWinner(Player: list[int]) -> bool:
    # rows
    if Player[0] and Player[1] and Player[2]:
        return True
    elif Player[3] and Player[4] and Player[5]:
        return True
    elif Player[6] and Player[7] and Player[8]:
        return True
    elif Player[0] and Player[3] and Player[6]: # colums
        return True
    elif Player[1] and Player[4] and Player[7]:
        return True
    elif Player[2] and Player[5] and Player[8]:
        return True
    elif Player[0] and Player[4] and Player[8]:  # diangel
        return True
    elif Player[2] and Player[4] and Player[6]:
        return True
    else:
        return False


def RenderSelection(Choise: int, Icon: str, BoardLocation: list[list[int]]):
    RenderIcon: list[str]
    Color: str
    if Icon == "x":
        Color = COLOR_LIGHT_RED
        RenderIcon = [
            "    __  __    ",
            "    \ \/ /    ",
            "     \  /     ",
            "     /  \     ",
            "    /_/\_\    ",
            "              ",]
    else:
        Color = COLOR_LIGHT_GREEN
        RenderIcon = [
            "      ___     ",
            "     / _ \    ",
            "    | | | |   ",
            "    | |_| |   ",
            "     \___/    ",
            "              "]
        
    x = BoardLocation[Choise-1]

    movecursor(x[0], x[1])
    for idx, s in enumerate(RenderIcon):
        movecursor(x[0]+idx, x[1])
        print(Color+ s,end="")
        print(COLOR_LIGHT_BLUE, end="")

    

def RenderBoard(Width, Height) -> list[list[int]]:
    BoardStringList = [
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
    "       _      ",
    "      / |     ",
    "      | |     ",
    "      | |     ",
    "      |_|     "]

    Number2String = [
    "     ____     ",
    "    |___ \    ",
    "      __) |   ",
    "     / __/    ",
    "    |_____|   "]

    Number3String = [
    "     _____    ",
    "    |___ /    ",
    "      |_ \    ",
    "     ___) |   ",
    "    |____/    "]

    Number4String = [
    "     _  _     ",
    "    | || |    ",
    "    | || |_   ",
    "    |__   _|  ",
    "       |_|    "]

    Number5String = [
    "     ____     ",
    "    | ___|    ",
    "    |___ \    ",
    "     ___) |   ",
    "    |____/    "]

    Number6String = [
    "      __      ",
    "     / /_     ",
    "    | '_ \    ",
    "    | (_) |   ",
    "     \___/    "]

    Number7String = [
    "     _____    ",
    "    |___  |   ",
    "       / /    ",
    "      / /     ",
    "     /_/      "]

    Number8String = [
    "      ___     ",
    "     ( _ )    ",
    "     / _ \    ",
    "    | (_) |   ",
    "     \___/    "]

    Number9String = [
    "      ___     ",
    "     / _ \    ",
    "    | (_) |   ",
    "     \__, |   ",
    "       /_/    "]

    NumberStringList: list[list[int]] = [Number1String, Number2String, Number3String, Number4String, Number5String, Number6String, Number7String, Number8String, Number9String]


    movecursor(7,0)
    TopSpace = ((int(Height/2))-15)
    print((" " * Width ) * TopSpace, end="")
    
    LeftSpace = int((Width - 46) / 2)
    for x in BoardStringList:
        print(" " * LeftSpace + x, end="")

    SpaceLoactions: list[list[int]] = [
        [TopSpace+7+1,LeftSpace+2],[TopSpace+7+1,LeftSpace+2+15],[TopSpace+7+1,LeftSpace+2+30],
        [TopSpace+7+1+7,LeftSpace+2],[TopSpace+7+1+7,LeftSpace+2+15],[TopSpace+7+1+7,LeftSpace+2+30],
        [TopSpace+7+1+14,LeftSpace+2],[TopSpace+7+1+14,LeftSpace+2+15],[TopSpace+7+1+14,LeftSpace+2+30]]

    for i, x in enumerate(SpaceLoactions):
        movecursor(x[0], x[1])
        for idx, s in enumerate(NumberStringList[i]):
            movecursor(x[0]+idx, x[1])
            print(s,end="")
    # just setting the cursor in the corner, if it gets closed or cras, it will not nuke the text
    movecursor(Height-1,Width)
    return SpaceLoactions

                                                                           

def PrintStartScreen(Width: int):
    print(COLOR_LIGHT_BLUE, end="")

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
    print(WelcomeString, end="")
    print('—' * Width, end="")


def GameLoop():
    Screen_width = os.get_terminal_size().columns
    Screen_Height = os.get_terminal_size().lines

    if Screen_width < 95:
        print("The game is made in mind for the 95 width and above...")
        print("Rezise and rerun... Thanks")
        exit(0)
    if Screen_Height < 42:
        print("The game is made in mind for the 42 and above in height...")
        print("Rezise and rerun... Thanks")
        exit(0)

    PrintStartScreen(Screen_width)
    print(COLOR_CYAN, end="")
    
    OptionMenu()
    # Print the size of terminal

    BoardLocation = RenderBoard(Screen_width, Screen_Height)

    Spaces: list[int] = [1,2,3,4,5,6,7,8,9]

    Player1: list[bool] = [False, False, False, False, False, False, False, False, False]
    Player2: list[bool] = [False, False, False, False, False, False, False, False, False]
    Round: int = 0
    while True:
        Choise = AskForMove(Spaces, BoardLocation, Screen_width, Screen_Height)
        Choise = int(Choise)
        # assuming that the value excict other could not be chosen, in AskForMove
        Spaces.remove(int(Choise))

        Player: list[bool]
        Icon: str = "O"
        if Round % 2 == 0:
            Icon = "x"
            Player = Player1

        else:
            Icon = "O"
            Player = Player2
        Player[Choise-1] = True
        RenderSelection(Choise, Icon, BoardLocation)
        movecursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            exit()

        Round = Round + 1
       


    


if __name__=="__main__":
    GameLoop()
