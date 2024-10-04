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

# basicly set cursor to wipe from and print space to fill screen
def WipeScreen(LineStart: int):
    movecursor(LineStart,0)
    print(" " * os.get_terminal_size().columns * (os.get_terminal_size().lines - 7), end="")
    movecursor(LineStart,0)


def AskForMove(Spaces: list[int], BoardLoacations: list[list[int]], Width: int, Height: int) -> int:
    OutputLocation = (BoardLoacations[0][0]-7)/2+7
    movecursor(OutputLocation, BoardLoacations[0][1])
    print("(q for quit) Please Pick a Space... ", end="")
    for x in Spaces:
        print(str(x) + ", ", end="")
    while True:
        Choise = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, Spaces)
        if Choise in StringSpaces:
            break
        if Choise == "q":
            movecursor(Height-1,Width)
            exit(0)
    # wipeping 
    movecursor(OutputLocation, 0)
    print(" "*Width, end="")
    movecursor(Height-1, Width)
    return Choise


def AskSwap(SpacesFrom: list[int], SpacesTo: list[int], BoardLoacations: list[list[int]], Width: int, Height: int) -> int:
    OutputLocation = (BoardLoacations[0][0]-7)/2+7
    movecursor(OutputLocation, BoardLoacations[0][1])
    print("Please Pick a Space To Move From ", end="")
    for x in SpacesFrom:
        print(str(x) + ", ", end="")
    while True:
        ChoiseFrom = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, SpacesFrom)
        if ChoiseFrom in StringSpaces:
            break
    movecursor(OutputLocation, BoardLoacations[0][1])
    print("Please Pick a Space To Move to ", end="")
    
    for x in SpacesTo:
        print(str(x) + ", ", end="")
    while True:
        ChoiseTo = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, SpacesTo)
        if ChoiseTo in StringSpaces:
            break

    # wipeping 
    movecursor(OutputLocation, 0)
    print(" "*Width, end="")
    movecursor(Height-1, Width)
    return int(ChoiseFrom), int(ChoiseTo)
    

def PrintCenter(StringList: list[str], Width, Height):
    WipeScreen(7)
    for idx, x in enumerate(StringList):
        movecursor((Height-len(StringList))/2 + idx, (Width-len(StringList[0]))/2)
        print(x, end="")
    movecursor(Height-1,Width)
            




def OptionMenu(Width: int, Height: int) -> int:
    # This loops until player deside to player ither by another person or internal bot
    while True:
        WipeScreen(7)
        print(COLOR_BLUE, end="")
        QuestionList = [
        "Play with another human, assuming you actually have friends, lol. ",
        "Challenge a bot, because... friends? Not really your thing? ",
        "Move pieces, strategic mode... You sure you're up for this? ",
        "Super Tic-Tac-Toe—oh, so you think you're a genius now? ",
        "Looking for an escape route already? "]
        QuestionListMaker = [COLOR_BLUE +"[" + COLOR_LIGHT_RED + "1" + COLOR_BLUE + "]", 
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "2" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "3" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "4" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "Q" + COLOR_BLUE + "]"]

        # This len is done to the index of the longest string
        Longest = len(QuestionList[0]) + 2
        LongestFirstLocationX = (Width - Longest)/2

        movecursor(9,(Width-5)/2)
        print(COLOR_BOLD + "Game Modes", end=COLOR_RESET+COLOR_BLUE)       
        for idx, Question in enumerate(QuestionList):
            movecursor(idx + 10, LongestFirstLocationX)
            print(Question, end="")
        for idx, Maker in enumerate(QuestionListMaker):
            movecursor(idx + 10, LongestFirstLocationX + Longest)
            print(Maker, end="")
       
        print(COLOR_LIGHT_RED, end="")
        movecursor(idx+ 14, (Width-10)/2)
        print("‾‾‾‾‾‾‾‾‾‾‾‾", end="")
        movecursor(idx+ 13, (Width-10)/2)
        Answer = input("Pick one: ")
        print(COLOR_BLUE, end="")
        
        if Answer == "1":
            WipeScreen(7)
            movecursor(Height,0)
            print( COLOR_LIGHT_PURPLE +"Friend Mode" + COLOR_BLUE, end="")
            return 1
        elif Answer == "2":
            WipeScreen(7)
            movecursor(Height,0)
            print( COLOR_LIGHT_PURPLE +"Machine Mode" + COLOR_BLUE, end="")
            return 2
        elif Answer == "3":
            WipeScreen(7)
            movecursor(Height,0)
            print(COLOR_LIGHT_PURPLE + "Swap Mode" + COLOR_BLUE, end="")
            return 3
        elif Answer == "4":
            WipeScreen(7)
            movecursor(Height,0)
            print(COLOR_LIGHT_PURPLE + "Super Mode, Bot" + COLOR_BLUE, end="")
            return 4
        elif Answer == "q":
            print("noob")
            exit(0)


def EndMessage(Message: str, Width: int, Height: int):
    if Message == "X Won":
        MessageString = [
            " __  __        __     __     ______     __   __    ",
            '/\_\_\_\      /\ \  _ \ \   /\  __ \   /\ "-.\ \   ',
            '\/_/\_\/_     \ \ \/ ".\ \  \ \ \/\ \  \ \ \-.  \  ',
            '  /\_\/\_\     \ \__/".~\_\  \ \_____\  \ \_\\"\_ \ ',
            "  \/_/\/_/      \/_/   \/_/   \/_____/   \/_/ \/_/ "]
        PrintCenter(MessageString, Width, Height)
    elif Message == "O Won":
        MessageString = [
            " ______        __     __     ______     __   __    ",
            '/\  __ \      /\ \  _ \ \   /\  __ \   /\ "-.\ \   ',
            '\ \ \/\ \     \ \ \/ ".\ \  \ \ \/\ \  \ \ \-.  \  ',
            ' \ \_____\     \ \__/".~\_\  \ \_____\  \ \_\\"\_\ ',
            "  \/_____/      \/_/   \/_/   \/_____/   \/_/ \/_/ "]
        PrintCenter(MessageString, Width, Height)
    elif Message == "Tie":
        # sub zero big font...
        MessageString = [
            ' ______   __     ______     _____    ',
            '/\__  _\ /\ \   /\  ___\   /\  __-.  ',
            '\/_/\ \/ \ \ \  \ \  __\   \ \ \/\ \ ',
            '   \ \_\  \ \_\  \ \_____\  \ \____- ',
            '    \/_/   \/_/   \/_____/   \/____/ ']
        PrintCenter(MessageString, Width, Height)
        
    
    elif Message == "You Won":
        pass
    elif Message == "Bot Won":
        pass

def CheckWinner(Player: list[bool]) -> bool:
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


def render_icon(icon_type: str) -> list[str]:
    """Returns the corresponding icon as a list of strings based on the icon type."""
    if icon_type == "x":
        return [
            "    __  __    ",
            "    \ \/ /    ",
            "     \  /     ",
            "     /  \     ",
            "    /_/\_\    ",
            "              "
        ], COLOR_LIGHT_RED
    else:
        return [
            "      ___     ",
            "     / _ \    ",
            "    | | | |   ",
            "    | |_| |   ",
            "     \___/    ",
            "              "
        ], COLOR_LIGHT_GREEN


def render_number(num: int) -> list[str]:
    """Returns the corresponding number as a list of strings."""
    num_list = [
        [
            "       _      ",
            "      / |     ",
            "      | |     ",
            "      | |     ",
            "      |_|     "
        ],
        [
            "     ____     ",
            "    |___ \    ",
            "      __) |   ",
            "     / __/    ",
            "    |_____|   "
        ],
        [
            "     _____    ",
            "    |___ /    ",
            "      |_ \    ",
            "     ___) |   ",
            "    |____/    "
        ],
        [
            "     _  _     ",
            "    | || |    ",
            "    | || |_   ",
            "    |__   _|  ",
            "       |_|    "
        ],
        [
            "     ____     ",
            "    | ___|    ",
            "    |___ \    ",
            "     ___) |   ",
            "    |____/    "
        ],
        [
            "      __      ",
            "     / /_     ",
            "    | '_ \    ",
            "    | (_) |   ",
            "     \___/    "
        ],
        [
            "     _____    ",
            "    |___  |   ",
            "       / /    ",
            "      / /     ",
            "     /_/      "
        ],
        [
            "      ___     ",
            "     ( _ )    ",
            "     / _ \    ",
            "    | (_) |   ",
            "     \___/    "
        ],
        [
            "      ___     ",
            "     / _ \    ",
            "    | (_) |   ",
            "     \__, |   ",
            "       /_/    "
        ]
    ]
    return num_list[num - 1] if 1 <= num <= 9 else []


def RenderSelection(Choise: int, Icon: str, BoardLocation: list[list[int]]):
    RenderIcon, Color = render_icon(Icon)
    x = BoardLocation[Choise-1]

    movecursor(x[0], x[1])
    for idx, s in enumerate(RenderIcon):
        movecursor(x[0]+idx, x[1])
        print(Color+ s,end="")
        print(COLOR_LIGHT_BLUE, end="")


def RenderSwapSelection(ChoiseFrom: int, ChoiseTo: int, Icon: str, BoardLocation: list[list[int]]):

    # render new locatiton with the old functino for gamemode 1 
    RenderSelection(ChoiseTo, Icon, BoardLocation)
    
    x = BoardLocation[ChoiseFrom - 1]

    movecursor(x[0], x[1])
    for idx, s in enumerate(render_number(ChoiseTo)):
        movecursor(x[0]+idx, x[1])
        print(COLOR_LIGHT_BLUE+ s,end="")
        print(COLOR_LIGHT_BLUE, end="")
    

def RenderBoard(Width: int, Height: int) -> list[list[int]]:
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
        for idx, s in enumerate(render_number(i+ 1)):
            movecursor(x[0]+idx, x[1])
            print(s,end="")
    # just setting the cursor in the corner, if it gets closed or cras, it will not nuke the text
    movecursor(Height-1,Width)
    return SpaceLoactions


def RenderSuperBoard(Width: int, Height: int) -> list[list[list[int]]]:
    BoardStringList = [
    "┌───┬───┬───┐ ┃ ┌───┬───┬───┐ ┃ ┌───┬───┬───┐",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "└───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘",
    "━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━",
    "┌───┬───┬───┐ ┃ ┌───┬───┬───┐ ┃ ┌───┬───┬───┐",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "└───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘",
    "━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━",
    "┌───┬───┬───┐ ┃ ┌───┬───┬───┐ ┃ ┌───┬───┬───┐",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤",
    "│   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │",
    "└───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘"]
    BoardHeight = len(BoardStringList)
    BoardWidth = len(BoardStringList[0])
    BoardLocation: list[int] = [((Height-7 - BoardHeight)/2)+7, (Width-BoardWidth) / 2]
    movecursor(BoardLocation[0], BoardLocation[1])
    for idx, BoardString in enumerate(BoardStringList):
        movecursor(((Height-7 - BoardHeight)/2)+7 + idx, (Width-BoardWidth) / 2)
        print(COLOR_BLUE + BoardString, end="")
    movecursor(Height-1,Width)

    # Function to offset an existing board's locations
    def offset_board_locations(base_board: list[list[int]], y_offset: int = 17, x_offset: int = 0) -> list[list[int]]:
        return [[x + x_offset, y + y_offset] for x, y in base_board]
    
    # index all locations by board and hardcoded ofsets
    Board1Location: list[list[int]] = [[BoardLocation[0]+1, BoardLocation[1]+2],[BoardLocation[0]+1, BoardLocation[1]+2+4],[BoardLocation[0]+1, BoardLocation[1]+2+8],
                                       [BoardLocation[0]+1+2, BoardLocation[1]+2],[BoardLocation[0]+1+2, BoardLocation[1]+2+4],[BoardLocation[0]+1+2, BoardLocation[1]+2+8],
                                       [BoardLocation[0]+1+4, BoardLocation[1]+2],[BoardLocation[0]+1+4, BoardLocation[1]+2+4],[BoardLocation[0]+1+4, BoardLocation[1]+2+8]]
    Board2Location = offset_board_locations(Board1Location, y_offset=16)
    Board3Location = offset_board_locations(Board2Location, y_offset=16)

    # Board4Location through Board9Location add offsets based on Board1Location, Board2Location, Board3Location
    Board4Location = offset_board_locations(Board1Location, x_offset=8, y_offset=0)
    Board5Location = offset_board_locations(Board2Location, x_offset=8, y_offset=0)
    Board6Location = offset_board_locations(Board3Location, x_offset=8, y_offset=0)

    Board7Location = offset_board_locations(Board4Location, x_offset=8, y_offset=0)
    Board8Location = offset_board_locations(Board5Location, x_offset=8, y_offset=0)
    Board9Location = offset_board_locations(Board6Location, x_offset=8, y_offset=0)

    return [Board1Location, Board2Location, Board3Location, Board4Location, Board5Location, Board6Location, Board7Location, Board8Location, Board9Location]


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
    WipeScreen(0)
    # after printing the string made above 
    print(WelcomeString, end="")
    print('—' * Width, end="")


def GameLoop():
    Screen_width = os.get_terminal_size().columns
    Screen_Height = os.get_terminal_size().lines

    if Screen_width < 95 and Screen_Height < 42:
        WipeScreen(0)
        print("The game need 95 in width and 42 in height")
        print("Rezise and rerun... Thanks :)")
        exit(0)
    elif Screen_width < 95:
        WipeScreen(0)
        print("The game is made in mind for the 95 width and above...")
        print("Rezise and rerun... Thanks :)")
        exit(0)
    elif Screen_Height < 42:
        WipeScreen(0)
        print("The game is made in mind for the 42 and above in height...")
        print("Rezise and rerun... Thanks :)")
        exit(0)

    PrintStartScreen(Screen_width)
    print(COLOR_CYAN, end="")
    
    GameMode: int # This int should only be 1,2,3,4 = freind, bot, swap friend, super tictactoe
    GameMode = OptionMenu(Screen_width, Screen_Height)
    # Print the size of terminal
    if GameMode == 1:
        GameMode1(Screen_width, Screen_Height)
    elif GameMode == 2:
        PrintCenter(["Dont Have a bot programmed at this time"])
    elif GameMode == 3:
        GameMode3(Screen_width, Screen_Height)
        pass
    elif GameMode == 4: # this game mode is not done
        BoardLocations: list[list[list[int]]] = RenderSuperBoard(Screen_width, Screen_Height)

        Spaces: list[list[int]] = [[1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9],
                                   [1,2,3,4,5,6,7,8,9]]

        # super players board state, info https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe
        # 3x3 for each 3x3 
        Player1: list[bool] = [[False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False]]
        Player2: list[bool] = [[False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False]]
        while True:
            for x in range(9):
                SectionBoard = BoardLocations[x]
                for idx, t in enumerate(SectionBoard):
                    movecursor(t[0],t[1])
                    print(idx + 1, end= "")
                    Choise = AskForMove(Spaces[x], SectionBoard, int(Screen_width), Screen_Height)


def GameMode1(Screen_width, Screen_Height):
    BoardLocation = RenderBoard(Screen_width, Screen_Height)

    Spaces: list[int] = [1,2,3,4,5,6,7,8,9]

    # players board state
    Player1: list[bool] = [False, False, False, False, False, False, False, False, False]
    Player2: list[bool] = [False, False, False, False, False, False, False, False, False]
    Round: int = 0
    for x in range(9):
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
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("O Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1
    EndMessage("Tie", Screen_width, Screen_Height)       
    
       
def GameMode3(Screen_width, Screen_Height):
    BoardLocation = RenderBoard(Screen_width, Screen_Height)

    Spaces: list[int] = [1,2,3,4,5,6,7,8,9]

    # players board state
    Player1: list[bool] = [False, False, False, False, False, False, False, False, False]
    Player2: list[bool] = [False, False, False, False, False, False, False, False, False]
    Round: int = 0
    
    # limits the game mode 1 logic to 6 rounds... 
    for x in range(6):
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
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("O Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1
    
    # now you dont tie, but continue infinitly... until someone wins the game.
    # this logic is based upon to number number a picked... 
    while True:
        Player: list[bool]
        Icon: str = "O"
        if Round % 2 == 0:
            Icon = "x"
            Player = Player1
        else:
            Icon = "O"
            Player = Player2
        
        # finding what number a given player owns and therfore can mode from.
        # using the bool value list, which is normally used for checking the win condition.
        BoardLocationsFrom: list[int] = []
        for idx, x in enumerate(Player):
            if x: # checking bool values (True, False) maning no compare is done here. 
                # If location is used, will idx value + 1 be what to write... 
                BoardLocationsFrom.append(idx + 1)
        
        # finding spaces which is not used.
        BoardLocationsTo: list[int] = []
        for x in range(9): # there are 9 spaces, and i need both players value, so using index, for the player to check
            if Player1[x] == False and Player2[x] == False:
                BoardLocationsTo.append(x + 1) # convert from index to real(index start from 0, not 1)


        FromLocation, ToLocation = AskSwap(BoardLocationsFrom, BoardLocationsTo, BoardLocation, Screen_width, Screen_Height)
        Player[FromLocation-1] = False
        Player[ToLocation-1] = True

        RenderSwapSelection(FromLocation, ToLocation, Icon, BoardLocation)
        movecursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("O Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1

        

if __name__=="__main__":
    GameLoop()
