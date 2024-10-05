# To run this program, I recommend the following steps:
# 
# 1. Open a full-screen terminal or console window.
#    - This is important because the program uses ASCII art that may not display correctly in smaller windows.
# 
# 2. Navigate to the folder where this script (main.py) is saved.
#    - You can use the `cd` (change directory) command in the terminal to do this.
#    - For example, if the file is in a folder called "my_project" on the desktop:
#        cd Desktop/my_project
#
# 3. Run the program using one of the following commands:
#    - On Windows, use: `python main.py`
#    - On Linux/macOS, or if Python 3 is required: `python3 main.py`
# This import is simple, and get used ones... it enables the program to know the size of the console screen..
# the os module is part of python core lib, and nothing is needed to be installed. 
import os  # only get used for:     os.get_terminal_size().columns     and     os.get_terminal_size().lines

COLOR_RED="\033[0;31m"
COLOR_GREEN="\033[0;32m"
COLOR_BLUE="\033[0;34m"
COLOR_CYAN="\033[0;36m"
COLOR_YELLOW="\033[1;33m"
COLOR_LIGHT_RED="\033[1;31m"
COLOR_LIGHT_GREEN="\033[1;32m"
COLOR_LIGHT_BLUE="\033[1;34m"
COLOR_LIGHT_PURPLE="\033[1;35m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

# moves the cursor, to a location in the terminal
def TeleportCursor(y, x):
    print("\033[%d;%dH" % (y, x), end="")


def MoveCursor(x, y) -> str:
    movement = ""
    # Move down or up based on the y value
    if y > 0: movement += f"\033[{y}B"  # Move down
    elif y < 0: movement += f"\033[{abs(y)}A"  # Move up

    # Move right or left based on the x value
    if x > 0: movement += f"\033[{x}C"  # Move right
    elif x < 0: movement += f"\033[{abs(x)}D"  # Move left 

    return movement


# basicly set cursor to wipe from and print space to fill screen
def WipeScreen(LineStart: int):
    TeleportCursor(LineStart,0)
    print(" " * os.get_terminal_size().columns * (os.get_terminal_size().lines - 7), end="")
    TeleportCursor(LineStart,0)


def AskForMove(Spaces: list[int], BoardLoacations: list[list[int]], Width: int, Height: int) -> int:
    OutputLocation = (BoardLoacations[0][0]-7)/2+7
    TeleportCursor(OutputLocation, BoardLoacations[0][1])
    print("(q for quit) Please Pick a Space... ", end="")
    for x in Spaces:
        print(str(x) + ", ", end="")
    while True:
        Choise = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, Spaces)
        if Choise in StringSpaces:
            break
        if Choise == "q":
            TeleportCursor(Height-1,Width)
            exit(0)
    # wipeping 
    TeleportCursor(OutputLocation, 0)
    print(" "*Width, end="")
    TeleportCursor(Height-1, Width)
    return int(Choise)


def AskSwap(SpacesFrom: list[int], SpacesTo: list[int], BoardLoacations: list[list[int]], Width: int, Height: int) -> int:
    OutputLocation = (BoardLoacations[0][0]-7)/2+7
    TeleportCursor(OutputLocation, BoardLoacations[0][1])
    print("Please Pick a Space To Move From ", end="")
    for x in SpacesFrom:
        print(str(x) + ", ", end="")
    while True:
        ChoiseFrom = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, SpacesFrom)
        if ChoiseFrom in StringSpaces:
            break
    TeleportCursor(OutputLocation, BoardLoacations[0][1])
    print("Please Pick a Space To Move to ", end="")
    
    for x in SpacesTo:
        print(str(x) + ", ", end="")
    while True:
        ChoiseTo = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, SpacesTo)
        if ChoiseTo in StringSpaces:
            break

    # wipeping 
    TeleportCursor(OutputLocation, 0)
    print(" "*Width, end="")
    TeleportCursor(Height-1, Width)
    return int(ChoiseFrom), int(ChoiseTo)
    

def PrintCenter(StringList: list[str], Width, Height):
    WipeScreen(7)
    for idx, x in enumerate(StringList):
        TeleportCursor((Height-len(StringList))/2 + idx, (Width-len(StringList[0]))/2)
        print(x, end="")
    TeleportCursor(Height-1,Width)


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


def MiniMaxAlgo(BotSpaces: list[bool], Player: list[bool]) -> int:
    '''
    returns: get the score of all spaces which can be pciked, and sums it. 
    +1, -1, 0 = win, loss, tie. 
    '''
    # assuming its the Bot turn when this function is called.
    Spaces: list[int] = []
    for idx in range(9):
        if BotSpaces[idx] == False and Player[idx] == False:
            Spaces.append(idx)
    # making a score for each space...
    Scores: list[int] = []
    for Space in Spaces:
        # Copy bot space to temp one...
        TempBotSpace: list[bool] =  BotSpaces.copy()
        TempBotSpace[Space] = True      
        # get score of the space
        win = CheckWinner(TempBotSpace) # if the bot just won, score of one i given to that space. 
        if win: 
            Scores.append(1)
        else:
            if len(Spaces) == 1:
                return 0

        # if player did not win, are score needs to be determant by the function self.
        SumScore = MiniMaxAlgo(Player, TempBotSpace)
        # these score is with ther perspection from player.  Spaces Scores is based on the later scores of the remaning spaces.
        Scores.append(-SumScore)
    # Assuming all scores in now noted.
    SumScore: int = 0
    for Score in Scores:
        SumScore = SumScore + Score
    
    return SumScore


def OptionMenu(Width: int, Height: int) -> int:
    # This loops until player deside to player ither by another person or internal bot
    while True:
        WipeScreen(7)
        print(COLOR_BLUE, end="")
        QuestionList = [
        "Play with another human, assuming you actually have friends, lol. ",
        "Challenge a bot, because... friends? Not really your thing? ",
        "Move pieces, strategic mode... You sure you're up for this? ",
        "Super Tic-Tac-Toe, so you think you're a genius now? ",
        "Looking for an escape route already? "]
        QuestionListMaker = [COLOR_BLUE +"[" + COLOR_LIGHT_RED + "1" + COLOR_BLUE + "]", 
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "2" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "3" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "4" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "Q" + COLOR_BLUE + "]"]

        # This len is done to the index of the longest string
        Longest = len(QuestionList[0]) + 2
        LongestFirstLocationX = (Width - Longest)/2

        TeleportCursor(9,(Width-5)/2)
        print(COLOR_BOLD + "Game Modes", end=COLOR_RESET+COLOR_BLUE)       
        for idx, Question in enumerate(QuestionList):
            TeleportCursor(idx + 10, LongestFirstLocationX)
            print(Question, end="")
        for idx, Maker in enumerate(QuestionListMaker):
            TeleportCursor(idx + 10, LongestFirstLocationX + Longest)
            print(Maker, end="")
       
        print(COLOR_LIGHT_RED, end="")
        TeleportCursor(idx+ 14, (Width-10)/2)
        print("‾‾‾‾‾‾‾‾‾‾‾‾", end="")
        TeleportCursor(idx+ 13, (Width-10)/2)
        Answer = input("Pick one: ")
        print(COLOR_BLUE, end="")
        
        WipeScreen(7)
        TeleportCursor(Height,0)
        if Answer == "1":
            print( COLOR_LIGHT_PURPLE +"Friend Mode" + COLOR_BLUE, end="")
            return 1
        elif Answer == "2":
            print( COLOR_LIGHT_PURPLE +"Machine Mode" + COLOR_BLUE, end="")
            return 2
        elif Answer == "3":
            print(COLOR_LIGHT_PURPLE + "Swap Mode" + COLOR_BLUE, end="")
            return 3
        elif Answer == "4":
            print(COLOR_LIGHT_PURPLE + "Super Mode, Bot" + COLOR_BLUE, end="")
            return 4
        elif Answer == "q":
            print("noob")
            exit(0)


def EndMessage(Message: str, Width: int, Height: int):
    if Message == "X Won":
        # sub zero big font...
        MessageString = [
            " __  __        __     __     ______     __   __    ",
            '/\_\_\_\      /\ \  _ \ \   /\  __ \   /\ "-.\ \   ',
            '\/_/\_\/_     \ \ \/ ".\ \  \ \ \/\ \  \ \ \-.  \  ',
            '  /\_\/\_\     \ \__/".~\_\  \ \_____\  \ \_\\"\_ \ ',
            "  \/_/\/_/      \/_/   \/_/   \/_____/   \/_/ \/_/ "]
        PrintCenter(MessageString, Width, Height)
    elif Message == "O Won":
        # sub zero big font...
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
        # sub zero big font...
        # https://patorjk.com/software/taag/#p=display&f=Sub-Zero&t=Bot%20Won
        MessageString = ['                                                                             ',
                         COLOR_RED,
                         '          .                                                      .           ',
                         '        .n                   .                 .                  n.         ',
                         '  .   .dP                  dP                   9b                 9b.    .  ',
                         ' 4    qXb         .       dX                     Xb       .        dXp     t ',
                         'dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb',
                         '9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP',
                         ' 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP ',
                         "  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP   ",
                         "    `9XXXXXXXXXXXP' `9XX'   YOU    `98v8P'    LOST   `XXP' `9XXXXXXXXXXXP    ",
                         '        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~        ',
                         "                        )b.  .dbo.dP'`v'`9b.odb.  .dX(                       ",
                         '                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.                      ',
                         "                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb                     ",
                         '                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb                    ',
                         "                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP                    ",
                         "                     `'      9XXXXXX(   )XXXXXXP      `'                     ",
                         "                              XXXX X.`v'.X XXXX                              ",
                         "                              XP^X'`b   d'`X^XX                              ",
                         "                              X. 9  `   '  P )X                              ",
                         "                              `b  `       '  d                               ",
                         "                               `             '                               "]
        PrintCenter(MessageString, Width, Height)

# https://patorjk.com/software/taag/#p=testall&f=Isometric2&t=O%20X
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

# uses https://patorjk.com/software/taag/#p=testall&f=Isometric2&t=O%20X 
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

    TeleportCursor(x[0], x[1])
    for idx, s in enumerate(RenderIcon):
        TeleportCursor(x[0]+idx, x[1])
        print(Color+ s,end="")
        print(COLOR_LIGHT_BLUE, end="")


def RenderSwapSelection(ChoiseFrom: int, ChoiseTo: int, Icon: str, BoardLocation: list[list[int]]):

    # render new locatiton with the old functino for gamemode 1 
    RenderSelection(ChoiseTo, Icon, BoardLocation)
    
    x = BoardLocation[ChoiseFrom - 1]

    TeleportCursor(x[0], x[1])
    for idx, s in enumerate(render_number(ChoiseTo)):
        TeleportCursor(x[0]+idx, x[1])
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

    TeleportCursor(7,0)
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
        TeleportCursor(x[0], x[1])
        for idx, s in enumerate(render_number(i+ 1)):
            TeleportCursor(x[0]+idx, x[1])
            print(s,end="")
    # just setting the cursor in the corner, if it gets closed or cras, it will not nuke the text
    TeleportCursor(Height-1,Width)
    return SpaceLoactions


def RenderSuperBoard(Width: int, Height: int) -> list[list[list[int]]]:
    GigO = ["     ____    ",
            "    / __ \   ",
            "   | |  | |  ",
            "   | |  | |  ",
            "   | |__| |  ",
            "    \____/   "]
    GigX = ["   __   __   ",
            "   \ \ / /   ",
            "    \ V /    ",
            "     > <     ",
            "    / . \    ",
            "   /_/ \_\   "]
    BoardStringList = [
        "┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓",
        "┃ ┌───┬───┬───┐1┃ ┌───┬───┬───┐2┃ ┌───┬───┬───┐3┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫",
        "┃ ┌───┬───┬───┐4┃ ┌───┬───┬───┐5┃ ┌───┬───┬───┐6┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫",
        "┃ ┌───┬───┬───┐7┃ ┌───┬───┬───┐8┃ ┌───┬───┬───┐9┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │   │   │   │ ┃ │   │   │   │ ┃ │   │   │   │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛"]
    BoardHeight = len(BoardStringList)
    BoardWidth = len(BoardStringList[0])
    BoardLocation: list[int] = [((Height-7 - BoardHeight)/2)+7, (Width-BoardWidth) / 2]
    TeleportCursor(BoardLocation[0], BoardLocation[1])
    for idx, BoardString in enumerate(BoardStringList):
        TeleportCursor(((Height-7 - BoardHeight)/2)+7 + idx, (Width-BoardWidth) / 2)
        print(COLOR_BLUE + BoardString, end="")
    TeleportCursor(Height-1,Width)

    # Function to offset an existing board's locations
    def offset_board_locations(base_board: list[list[int]], y_offset: int = 17, x_offset: int = 0) -> list[list[int]]:
        return [[x + x_offset, y + y_offset] for x, y in base_board]
    
    # index all locations by board and hardcoded ofsets
    Board1Location: list[list[int]] = [[BoardLocation[0]+2, BoardLocation[1]+4],[BoardLocation[0]+2, BoardLocation[1]+4+4],[BoardLocation[0]+2, BoardLocation[1]+4+8],
                                       [BoardLocation[0]+2+2, BoardLocation[1]+4],[BoardLocation[0]+2+2, BoardLocation[1]+4+4],[BoardLocation[0]+2+2, BoardLocation[1]+4+8],
                                       [BoardLocation[0]+2+4, BoardLocation[1]+4],[BoardLocation[0]+2+4, BoardLocation[1]+4+4],[BoardLocation[0]+2+4, BoardLocation[1]+4+8]]
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


def TicTacToe():
    Screen_width = os.get_terminal_size().columns
    Screen_Height = os.get_terminal_size().lines

    if Screen_width < 95 or Screen_Height < 42:
        WipeScreen(0)
        print("The game need 95 in width and 42 in height (close to square)")
        print("Rezise and rerun... Thanks :)")
        text_list = [
            "To run this program, follow these simple steps:",
            
            "1. Open a terminal/console window:",
            "    - On **Windows**, press `Win + R`, type `cmd`, and hit Enter to open the Command Prompt.",
            "    - On **macOS/Linux**, you can open the Terminal from the Applications menu.",
            
            "2. Navigate to the folder where this script (main.py) is saved:",
            "    - On **Windows**, use the `cd` command. For example, if the file is in a folder called 'my_project' on your desktop:",
            "        cd Desktop\\my_project",
            "    - On **macOS/Linux**, use the same `cd` command, but with forward slashes:",
            "        cd ~/Desktop/my_project",
            
            "3. Run the program using the correct command for your system:",
            "    - On **Windows**, type:",
            "        python main.py",
            "    - On **macOS/Linux**, type:",
            "        python3 main.py",
            
            "Note: If you're on Windows and `python` doesn't work, you may need to install Python or add it to your PATH. Follow online tutorials for setting up Python on Windows."
        ]
        for t in text_list:
            print(t)
        return

    PrintStartScreen(Screen_width)
    print(COLOR_CYAN, end="")
    
    GameMode: int # This int should only be 1,2,3,4 = freind, bot, swap friend, super tictactoe
    GameMode = OptionMenu(Screen_width, Screen_Height)
    # Print the size of terminal
    if GameMode == 1:
        GameMode1(Screen_width, Screen_Height)
    elif GameMode == 2:
        GameMode2(Screen_width, Screen_Height)
    elif GameMode == 3:
        GameMode3(Screen_width, Screen_Height)
    elif GameMode == 4: # this game mode is not done
        GameMode4(Screen_width, Screen_Height)

#  all the game modes a splitted up in functions. 
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
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("O Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1
    EndMessage("Tie", Screen_width, Screen_Height)       


def GameMode2(Screen_width: int, Screen_Height: int):
    BoardLocation = RenderBoard(Screen_width, Screen_Height)

    Spaces: list[int] = [1,2,3,4,5,6,7,8,9]

    # players board state
    Player1: list[bool] = [False, False, False, False, False, False, False, False, False]
    Player2: list[bool] = [False, False, False, False, False, False, False, False, False]

    Round: int = 0
    for _ in range(9):
        if Round % 2 == 0:
            Choise = int(AskForMove(Spaces, BoardLocation, Screen_width, Screen_Height))
        else:
            # move with a algo
            Scores: list[int] = []
            BestScore: int
            BestSpace: int
            for Space in Spaces:
                # Copy bot space to temp one...
                TempBotSpace: list[bool] = Player2.copy()
                TempBotSpace[Space-1] = True
                SumScore = MiniMaxAlgo(Player1, TempBotSpace)
                Scores.append(-SumScore)
            BestScore = Scores[0]
            BestSpace = Spaces[0]
            for idx, score in enumerate(Scores):
                if score > BestScore:
                    BestScore = score
                    BestSpace = Spaces[idx]
            Choise = BestSpace
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
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("Bot Won", Screen_width, Screen_Height)
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
        TeleportCursor(Screen_Height-1, Screen_width)
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
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("X Won", Screen_width, Screen_Height)
            else:
                EndMessage("O Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1

def AskBoardToUse(Spaces: list[int], BoardLocations: list[list[list[int]]], Width: int, Height: int) -> int:
    OutputLocation = (BoardLocations[0][0][0]-7)/2+7
    TeleportCursor(OutputLocation, BoardLocations[0][0][0] - 2)
    print("(q for quit) Please Pick a Board Number to Start ", end="")
    for x in Spaces:
        print(str(x) + ", ", end="")
    while True:
        Choise = input("\033[%d;%dH" % (OutputLocation, BoardLocations[0][0][0] - 2) +": " + (" " * int(Width - BoardLocations[0][0][0] - 2))+ "\033[%d;%dH" % (OutputLocation, BoardLocations[0][0][0] - 2))
        StringSpaces = map(str, Spaces)
        if Choise in StringSpaces:
            break
        if Choise == "q":
            TeleportCursor(Height-1,Width)
            exit(0)
    # wipeping 
    TeleportCursor(OutputLocation, 0)
    print(" "*Width, end="")
    TeleportCursor(Height-1, Width)
    return int(Choise)


def HighLightBoardSpace(BoardNumber: int, BoardLocations: list[list[list[int]]], Width: int, Height: int):
    CornerLocationY, CornerLocationX = BoardLocations[BoardNumber-1][0]
    # ofsets from frist space normal number location to the innner board location
    CornerLocationY = CornerLocationY - 1
    CornerLocationX = CornerLocationX - 2

    # This is a String which will not overwrite the number written in the spaces...
    # this become usefull if you like to change color of board but not the icons..
    InnerBoard = [
        "┌───┬───┬───┐",
        "│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│",
        "├───┼───┼───┤",
        "│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│",
        "├───┼───┼───┤",
        "│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│" + MoveCursor(3,0) +"│",
        "└───┴───┴───┘"]
    for idx, string in enumerate(InnerBoard):
        print(COLOR_YELLOW, end="")
        TeleportCursor(CornerLocationY + idx, CornerLocationX)
        print(string, end="")
        print(COLOR_BLUE)

    OtherBoards = [1,2,3,4,5,6,7,8,9]
    OtherBoards.remove(BoardNumber)
    
    for otherboard in OtherBoards:
        CLocationY, CLocationX = BoardLocations[otherboard-1][0]
        # ofsets from frist space normal number location to the innner board location
        CLocationY = CLocationY - 1
        CLocationX = CLocationX - 2
        for idx, string in enumerate(InnerBoard):
            print(COLOR_BLUE, end="")
            TeleportCursor(CLocationY + idx, CLocationX)
            print(string, end="")
    


def GameMode4(Screen_width, Screen_Height):
    # Returns the terminal cursor locations, first list is alll board, then 9 spaces and a list with 2 times, x and y...
    BoardLocations: list[list[list[int]]] = RenderSuperBoard(Screen_width, Screen_Height)

    Boards: list[int] = [1,2,3,4,5,6,7,8,9]
    BoardSpaces: list[list[int]] = [[1,2,3,4,5,6,7,8,9],
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
    PlayerBoardWin1 = [False, False, False, False, False, False, False, False, False]
    Player1: list[bool] = [[False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False]]
    PlayerBoardWin2 = [False, False, False, False, False, False, False, False, False]
    Player2: list[bool] = [[False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False]]
    CurrentSelectedBoard: int
    HaveNoBoardSlected: bool = False
    Round: int = 0
    while True: # Cant be sure how many rounds it will take, to finish a game...
        if HaveNoBoardSlected == False:
            BoardChoise = AskBoardToUse(Boards, BoardLocations, Screen_width, Screen_Height)
            CurrentSelectedBoard = BoardChoise
        Spaces = BoardSpaces[CurrentSelectedBoard-1]
        SubBoardLocations = BoardLocations[CurrentSelectedBoard-1]
        HighLightBoardSpace(CurrentSelectedBoard, BoardLocations, Screen_width, Screen_Height)
        Choise = AskForMove(Spaces, SubBoardLocations, Screen_width, Screen_Height)
        Player: list[bool]
        Icon = ""
        if Round % 2 == 0:
            Player = Player1[CurrentSelectedBoard-1]
            Icon = "X"
        else:
            Player = Player2[CurrentSelectedBoard-1]
            Icon = "O"
        Player[Choise-1] = True
        LocationY = SubBoardLocations[Choise-1][0]
        LocationX = SubBoardLocations[Choise-1][1]
        TeleportCursor(LocationY, LocationX)
        if Icon == "X": 
            print(COLOR_RED + Icon, end="")
        else:
            print(COLOR_GREEN + Icon, end="")
        # gives palyer new board
        CurrentSelectedBoard = Choise
        HaveNoBoardSlected = True
        # incriment round
        Round = Round + 1



if __name__=="__main__":
    TicTacToe()
