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

def TeleportCursor(y: int , x: int):
    """
    This fucntion allows the program to move the cursor. 
    Meaning the the starting point of where print funtion will place charactors.

    Teleport do not interact with nothing else then cursor... No return value
    """
    if not isinstance(y, int) or not isinstance(x, int):
        raise TypeError(f"Expected integers for y and x, but got {type(y)} and {type(x)}")
    print("\033[%d;%dH" % (y, x), end="")


def MoveCursor(x, y) -> str:
    """
    This function make a way to move cursor, without placing any chars.

    Move return a value based of the movement, this is done becaurse move negative is a defrind char.
    The trick here is it works as a char you can use multiple times, and the action does not need multiple calls to do the same action.
    """
    if not isinstance(y, int) or not isinstance(x, int):
        raise TypeError(f"Expected integers for y and x, but got {type(y)} and {type(x)}")
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
    """
    WipeScreen basicly prints space chars to fill out the screen.
    if the program want to wipe from a given point, it can use LineStart. which will be used by cursor before wipe.
    
    Importantly this function uses os core lib, to know how big the screen is.
    This is done, if in future cases of resizesing support, where the point of wipe is to re-render the whole game.
    """
    if not isinstance(LineStart, int) :
        raise TypeError(f"Expected integers for LineStart, but got {type(LineStart)}")
    # Get screen size.
    Width = os.get_terminal_size().columns
    Height = os.get_terminal_size().lines
    TeleportCursor(LineStart,0)
    print(" " * Width * (Height- 7), end="")
    TeleportCursor(LineStart,0)


def PrintCenter(StringList: list[str], Width, Height):
    """
    Takes a given list of strings, and makes sure it gets printed i the middle of the screen.
    This wipes the screen, so get mostly used in the end of the game to represent a win or loss.
    """
    WipeScreen(7)
    for idx, x in enumerate(StringList):
        TeleportCursor(int((Height-len(StringList))/2) + idx, int((Width-len(StringList[0]))/2))
        print(x, end="")
    TeleportCursor(Height-1,Width)


def AskForMove(Query: str, Options: list[int], BoardLoacations: list[list[int]], Width: int, Height: int) -> int:
    """
    This prompts the users for what place a piece should be placed on.
    the locatin of the prompt is bassed on the first board space location 
    """
    OutputLocation = int((BoardLoacations[0][0]-7)/2+7)
    TeleportCursor(OutputLocation, BoardLoacations[0][1])
    print(Query, end="")
    for x in Options:
        print(str(x) + ", ", end="")
    while True:
        Choise = input("\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1]) +": " + (" " * int(Width - BoardLoacations[0][1] - 2))+ "\033[%d;%dH" % (OutputLocation+1, BoardLoacations[0][1] + 2))
        StringSpaces = map(str, Options)
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
    win     =  +1
    loss    =  -1
    tie     =   0  
    '''
    # First realizing what paces that avilable for use.
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
        # get score of the space, sum of the trigle down space scores
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

def MiniMaxAlgoSuper(BotSpaces: list[list[bool]], Player: list[list[bool]]) -> int:
    # algo for the super tic tiac toe mode... dont have time.. 
    pass


def RenderRandomBottomArt(HeightLimit: int, WidthLimit: int, YLocation: int, XLocation: int, Height, Width:int):
    ArtList = []
    if HeightLimit > 14:
        StringList: list[str] = ["            .'              ",
                                 "           .-~<             ",
                                 "        __/    > -'         ",
                                 "      -~ ___--/             ",
                                 "     /_//     \__           ",
                                 "    '            \          ",
                                 "    |          __/          ",
                                 "   |O        |    .__,--_   ",
                                 "    )        / d  . _>   /. ",
                                 "   \       /.._  .)    <    ",
                                 "    `     |<   \  `-.__/    ",
                                 "    |    /  \__//.--...<|   ",
                                 "    '-.__\\  - ' '--~|      "]
        ArtList.append(StringList)
    if HeightLimit > 16:
        StringList: list[str] = ["                                                 *******                ",
                                 "                                 ~             *---*******              ",
                                 "                                ~             *-----*******             ",
                                 "                         ~                   *-------*******            ",
                                 "                        __      _   _!__     *-------*******            ",
                                 "                   _   /  \_  _/ \  |::| ___ **-----********   ~        ",
                                 "                 _/ \_/^    \/   ^\/|::|\|:|  **---*****/^\_            ",
                                 "              /\/  ^ /  ^    / ^ ___|::|_|:|_/\_******/  ^  \           ",
                                 "             /  \  _/ ^ ^   /    |::|--|:|---|  \__/  ^     ^\___       ",
                                 "           _/_^  \/  ^    _/ ^   |::|::|:|-::| ^ /_  ^    ^  ^   \_     ",
                                 "          /   \^ /    /\ /       |::|--|:|:--|  /  \        ^      \    ",
                                 "         /     \/    /  /        |::|::|:|:-:| / ^  \  ^      ^     \   ",
                                 "   _Q   / _Q  _Q_Q  / _Q    _Q   |::|::|:|:::|/    ^ \   _Q      ^      ",
                                 '  /_\)   /_\)/_/\\)  /_\)  /_\)  |::|::|:|:::|          /_\)            ',
                                 '_O|/O___O|/O_OO|/O__O|/O__O|/O__________________________O|/O_"_________ ',
                                 "//////////////////////////////////////////////////////////////////////  "]
        ArtList.append(StringList)
    if HeightLimit > 10:
        StringList: list[str] = ["  ◌                             ◌                                       ◌              ",
                                 "                                             ‧₊ *:･ﾟ彡       ◌                 ☽︎       ◌",
                                 "               ◌                                 ✩彡 ･ﾟ *:                              ",
                                 "                              ◌                                        ◌                ",
                                 "◌                                                                                       ",
                                 "                                                  ♡                                     ",
                                 "                                            (\_(\    /)_/)                              ",
                                 "                                            (    )  (    )                              ",
                                 "                                           ૮/ʚɞ  |ა ૮|  ʚɞ\ა                            ",
                                 "                                           ( ◌   |   |   ◌ )                            "]
        ArtList.append(StringList)
    StringHeight = len(StringList)
    print(COLOR_YELLOW)
    time = int(os.times().elapsed*100)
    HeightLocation = Height - StringHeight 
    WidthLocation = int((Width-len(StringList[0]))/2)
    for idx, x in enumerate(ArtList[time % len(ArtList)]):
        TeleportCursor(HeightLocation + idx, WidthLocation)
        print(x, end="")



def OptionMenu(Width: int, Height: int) -> int:
    # This loops until player deside to player ither by another person or internal bot
    while True:
        WipeScreen(7)
        print(COLOR_BLUE, end="")
        QuestionList = [
        "Play with another human, assuming you actually have friends, lol. ",
        "Challenge a bot, because... friends? Not really your thing? ",
        'Three pieces, you´ll need to exchange pieces to secure your victory. (buggy)',
        "Super Tic-Tac-Toe, so you think you're a genius now?",
        "Looking for an escape route already? "]
        QuestionListMaker = [COLOR_BLUE +"[" + COLOR_LIGHT_RED + "1" + COLOR_BLUE + "]", 
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "2" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "3" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "4" + COLOR_BLUE + "]",
                             COLOR_BLUE +"[" + COLOR_LIGHT_RED + "Q" + COLOR_BLUE + "]"]

        # This len is done to the index of the longest string
        Longest = len(QuestionList[2]) + 2
        LongestFirstLocationX = int((Width - Longest)/2)

        TeleportCursor(9,int((Width-5)/2))
        print(COLOR_BOLD + "Game Modes", end=COLOR_RESET+COLOR_BLUE)       
        for idx, Question in enumerate(QuestionList):
            TeleportCursor(idx + 10, LongestFirstLocationX)
            print(Question, end="")
        for idx, Maker in enumerate(QuestionListMaker):
            TeleportCursor(idx + 10, LongestFirstLocationX + Longest)
            print(Maker, end="")

        # calculating what Space is left under the query... drawing ascii art.   
        SpaceForArt = Height - idx+ 15
        RenderRandomBottomArt(SpaceForArt, Width - 10, idx + 15, 5, Height, Width)
       
        print(COLOR_LIGHT_RED, end="")
        TeleportCursor(idx+ 14, int((Width-10)/2))
        print("‾‾‾‾‾‾‾‾‾‾‾‾", end="")
        TeleportCursor(idx+ 13, int((Width-10)/2))
        

        # the program will stall here until the user have made some kind of input...
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
            print(COLOR_LIGHT_PURPLE + "Three Piece Swap (Bugs)" + COLOR_BLUE, end="")
            return 3
        elif Answer == "4":
            print(COLOR_LIGHT_PURPLE + "Super Mode, Bot" + COLOR_BLUE, end="")
            return 4
        elif Answer == "q":
            print("noob")
            exit(0)
        # if the answer not valid, it will re-render the option menu


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
        #https://ascii.co.uk/art/medal
        MessageString = ['                                                                             ',
                         COLOR_RED,
                              " _______________ ",
                              "|@@@@|     |####|",
                              "|@@@@|     |####|",
                              "|@@@@|     |####|",
                              "\@@@@|     |####/"
                              " \@@@|     |###/ ",
                              "  `@@|_____|##'  ",
                              "       (O)       ",
                              "    .-'''''-.    ",
                              "  .'  * * *  `.  ",
                              " :  *       *  : ",
                              ": ~    YOU    ~ :",
                              ": ~    WON    ~ :",
                              " :  *       *  : ",
                              "  `.  * * *  .'  ",
                              "    `-.....-'    "]
    elif Message == "Bot Won":
        # https://ascii.co.uk/art/skull
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
    

def RenderMiniBoard(Screen_Width: int, Screen_Height: int):
    MiniBaoard = [
        "┌───┬───┬───┐",
        "│ \ │ | │   │",
        "├───┼───┼───┤",
        "│   │ \ │   │",
        "├───┼───┼───┤",
        "│   │ | │ \ │",
        "└───┴───┴───┘"
    ]
    pass


def RenderBoard(Width: int, Height: int) -> list[list[int]]:
    # Type checking at the beginning
    if not isinstance(Width, int) or not isinstance(Height, int):
        raise TypeError(f"Expected integers for Width and Height, but got {type(Width)} and {type(Height)}")


    BoardStringList = [
        "┌──────────────┬──────────────┬──────────────┐",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "├──────────────┼──────────────┼──────────────┤",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "├──────────────┼──────────────┼──────────────┤",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "│              │              │              │",
        "└──────────────┴──────────────┴──────────────┘"]

    WipeScreen(7)
    TopSpace = int(((Height-7)-len(BoardStringList))/2) + 7 + 1 # + 1 is for inner location
    LeftSpace = int((Width-len(BoardStringList[0]))/2) + 1 # + 1 is for inner location
    for idx, string in enumerate(BoardStringList):
        TeleportCursor(TopSpace + idx - 1, LeftSpace - 1) # -1 to make the cursor of the outer location
        print(string, end="")


    SpaceLoactions: list[list[int]] = [
        [TopSpace,LeftSpace],[TopSpace,LeftSpace+15],[TopSpace,LeftSpace+30],
        [TopSpace+7,LeftSpace],[TopSpace+7,LeftSpace+15],[TopSpace+7,LeftSpace+30],
        [TopSpace+14,LeftSpace],[TopSpace+14,LeftSpace+15],[TopSpace+14,LeftSpace+30]]

    for i, x in enumerate(SpaceLoactions):
        TeleportCursor(x[0], x[1])
        for idx, s in enumerate(render_number(i+ 1)):
            TeleportCursor(x[0]+idx, x[1])
            print(s,end="")
    # just setting the cursor in the corner, if it gets closed or cras, it will not nuke the text
    TeleportCursor(Height-1,Width)
    return SpaceLoactions


def RenderSuperBoard(Width: int, Height: int) -> list[list[list[int]]]:

    BoardStringList = [
        "┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓",
        "┃ ┌───┬───┬───┐1┃ ┌───┬───┬───┐2┃ ┌───┬───┬───┐3┃",
        "┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫",
        "┃ ┌───┬───┬───┐4┃ ┌───┬───┬───┐5┃ ┌───┬───┬───┐6┃",
        "┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫",
        "┃ ┌───┬───┬───┐7┃ ┌───┬───┬───┐8┃ ┌───┬───┬───┐9┃",
        "┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃ │ 1 │ 2 │ 3 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃ │ 4 │ 5 │ 6 │ ┃",
        "┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃ ├───┼───┼───┤ ┃",
        "┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃ │ 7 │ 8 │ 9 │ ┃",
        "┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃ └───┴───┴───┘ ┃",
        "┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛"]
    BoardHeight = len(BoardStringList)
    BoardWidth = len(BoardStringList[0])
    BoardLocationHight: int = int((Height-7 - BoardHeight)/2)+7
    BoardLocationWidth: int = int((Width-BoardWidth) / 2)
    TeleportCursor(BoardLocationHight, BoardLocationWidth)
    for idx, BoardString in enumerate(BoardStringList):
        TeleportCursor(BoardLocationHight + idx, BoardLocationWidth)
        print(COLOR_BLUE + BoardString, end="")
    TeleportCursor(Height-1,Width)

    # Function to offset an existing board's locations
    def offset_board_locations(base_board: list[list[int]], y_offset: int = 17, x_offset: int = 0) -> list[list[int]]:
        return [[x + x_offset, y + y_offset] for x, y in base_board]
    
    # index all locations by board and hardcoded ofsets
    Board1Location: list[list[int]] = [[BoardLocationHight+2, BoardLocationWidth+4],[BoardLocationHight+2, BoardLocationWidth+4+4],[BoardLocationHight+2, BoardLocationWidth+4+8],
                                       [BoardLocationHight+2+2, BoardLocationWidth+4],[BoardLocationHight+2+2, BoardLocationWidth+4+4],[BoardLocationHight+2+2, BoardLocationWidth+4+8],
                                       [BoardLocationHight+2+4, BoardLocationWidth+4],[BoardLocationHight+2+4, BoardLocationWidth+4+4],[BoardLocationHight+2+4, BoardLocationWidth+4+8]]
    
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
    Screen_width: int = os.get_terminal_size().columns
    Screen_Height: int = os.get_terminal_size().lines

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
    Player1: list[bool] = [False]*9
    Player2: list[bool] = [False]*9
    Round: int = 0
    Icon: str = "O"
    for x in range(9):
        Player: list[bool]
        if Round % 2 == 0:
            Icon = "x"
            Player = Player1
        else:
            Icon = "O"
            Player = Player2
        Choise = AskForMove("(q for quit) '" + Icon  + "' Please Pick a Space... ", Spaces, BoardLocation, Screen_width, Screen_Height)
        Choise = int(Choise)
        # assuming that the value excict other could not be chosen, in AskForMove
        Spaces.remove(int(Choise))
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
    Icon: str = "X"
    for _ in range(9):
        Player: list[bool]
        if Round % 2 == 0:
            Icon = "x"
            Player = Player1
        else:
            Icon = "O"
            Player = Player2
        if Round % 2 == 0:
            Choise = int(AskForMove("(q for quit) '" + Icon  + "' Please Pick a Space... ", Spaces, BoardLocation, Screen_width, Screen_Height))
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
        Player[Choise-1] = True
        RenderSelection(Choise, Icon, BoardLocation)
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("You Won", Screen_width, Screen_Height)
            else:
                EndMessage("Bot Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1
    EndMessage("Tie", Screen_width, Screen_Height)        


def GameMode3(Screen_width, Screen_Height):
    BoardLocation = RenderBoard(Screen_width, Screen_Height)

    Spaces: list[int] = [1,2,3,4,5,6,7,8,9]

    # players board state
    Player1: list[bool] = [False]*9
    Bot: list[bool] = [False]*9
    Round: int = 0
    
    # limits the game mode 2 logic to 6 rounds... 
    for x in range(6):
        if Round % 2 == 0:
            Choise = int(AskForMove("(q for quit) Please Pick a Space... ", Spaces, BoardLocation, Screen_width, Screen_Height))
        else:
            # move with a algo
            Scores: list[int] = []
            BestScore: int
            BestSpace: int
            for Space in Spaces:
                # Copy bot space to temp one...
                TempBotSpace: list[bool] = Bot.copy()
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
            Player = Bot
        Player[Choise-1] = True
        RenderSelection(Choise, Icon, BoardLocation)
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("You Won", Screen_width, Screen_Height)
            else:
                EndMessage("Bot Won", Screen_width, Screen_Height)
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
            Player = Bot
        
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
            if Player1[x] == False and Bot[x] == False:
                BoardLocationsTo.append(x + 1) # convert from index to real(index start from 0, not 1)

        if Round % 2 == 0:
            FromLocation = AskForMove("Please Pick a Space To Move From ", BoardLocationsFrom, BoardLocation, Screen_width, Screen_Height)
            ToLocation = AskForMove("Please Pick a Space To Move to ", BoardLocationsTo, BoardLocation, Screen_width, Screen_Height)
        else:
            ## need some random var to decide, where to move from and to...
            time = int(os.times().elapsed*100)
            ToLocation = Spaces[time % len(Spaces)]
            BotSpaces: list[int] = []
            for idx, space in enumerate(Player):
                if space == True:
                    BotSpaces.append(idx)
            FromLocation = BotSpaces[time**2 % len(Spaces)]
        Player[FromLocation-1] = False
        Player[ToLocation-1] = True

        RenderSwapSelection(FromLocation, ToLocation, Icon, BoardLocation)
        TeleportCursor(Screen_Height-1, Screen_width)
        win: bool = CheckWinner(Player)
        if win:
            if Icon == "x":
                EndMessage("You Won", Screen_width, Screen_Height)
            else:
                EndMessage("Bot Won", Screen_width, Screen_Height)
            exit()
        Round = Round + 1


def HighLightBoardSpace(Show: bool, BoardNumber: int, BoardLocations: list[list[list[int]]], Width: int, Height: int):
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
        if Show:
            print(COLOR_YELLOW, end="")
        else:
            print(COLOR_BLUE, end="")
        TeleportCursor(CornerLocationY + idx, CornerLocationX)
        print(string, end="")
        print(COLOR_BLUE)
    


def GameMode4(Screen_width, Screen_Height):
    BigO = ["     ____    ",
            "    / __ \   ",
            "   | |  | |  ",
            "   | |  | |  ",
            "   | |__| |  ",
            "    \____/   ",
            "             "]
    BigX = ["   __   __   ",
            "   \ \ / /   ",
            "    \ V /    ",
            "     > <     ",
            "    / . \    ",
            "   /_/ \_\   ",
            "             "]
    BTie = ["             ",
            "             ",
            "┌───────────┐",
            "└───────────┘",
            "             ",
            "             ",
            "             "]
    # Returns the terminal cursor locations, first list is alll board, then 9 spaces and a list with 2 times, x and y...
    BoardLocations: list[list[list[int]]] = RenderSuperBoard(Screen_width, Screen_Height)

    Boards: list[int] = [1,2,3,4,5,6,7,8,9]
    BoardSpaces: list[list[int]] = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] # makes list with 9 list with 1,2..9 in them

        # super players board state, info https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe
        # 3x3 for each 3x3 
    PlayerBoardWin1 = [False for _ in range(9)] # 9 False values
    Player1: list[list[int]] = [[False for _ in range(9)] for _ in range(9)] # list of 9 list with 9 False values in them
    PlayerBoardWin2 = [False for _ in range(9)] # 9 False values
    Player2: list[list[int]] = [[False for _ in range(9)] for _ in range(9)] # list of 9 list with 9 False values in them
    PlayerBoardTie = [False for _ in range(9)] # 9 False values
    CurrentSelectedBoard: int
    HaveNoBoardSlected: bool = False
    Round: int = 0
    Icon = "X"
    while True: # Cant be sure how many rounds it will take, to finish a game...
        if HaveNoBoardSlected == False:
            BoardChoise = AskForMove("(q for quit) '" + Icon  + "' Please Pick a Board... ", Boards, BoardLocations[0], Screen_width, Screen_Height)
            CurrentSelectedBoard = BoardChoise
        Spaces = BoardSpaces[CurrentSelectedBoard-1]
        SubBoardLocations = BoardLocations[CurrentSelectedBoard-1]
        HighLightBoardSpace(True, CurrentSelectedBoard, BoardLocations, Screen_width, Screen_Height)
        Choise = AskForMove("(q for quit) '" + Icon  + "' Please Pick a Space... ", Spaces, BoardLocations[0], Screen_width, Screen_Height)
        HighLightBoardSpace(False, CurrentSelectedBoard, BoardLocations, Screen_width, Screen_Height)
        BoardSpaces[CurrentSelectedBoard-1].remove(Choise)
        Player: list[bool]
        if Round % 2 == 0:
            LocationY = SubBoardLocations[Choise-1][0]
            LocationX = SubBoardLocations[Choise-1][1]
            TeleportCursor(LocationY, LocationX)
            Player = Player1[CurrentSelectedBoard-1]
            Icon = "X"
            print(COLOR_RED + Icon, end="")
            # Saves the player move, in the player which just got set to current board
            Player[Choise-1] = True
            win = CheckWinner(Player)
            if win:
                PlayerBoardWin1[CurrentSelectedBoard-1] = True
                # some way to render the win
                SubBoardLocationHeight = SubBoardLocations[0][0] - 1 # top left corner location of subboard
                SubBoardLocationWidth = SubBoardLocations[0][1] - 2 # top left corner location of subboard
                for idx, x in enumerate(BigX):
                    TeleportCursor(SubBoardLocationHeight + idx, SubBoardLocationWidth)
                    print(x, end="")
            else:
                if len(BoardSpaces[CurrentSelectedBoard-1]) == 0:
                    PlayerBoardWin1[CurrentSelectedBoard-1] = True
                    # some way to render the tie
                    SubBoardLocationHeight = SubBoardLocations[0][0] - 1 # top left corner location of subboard
                    SubBoardLocationWidth = SubBoardLocations[0][1] - 2 # top left corner location of subboard
                    for idx, x in enumerate(BTie):
                        print(COLOR_YELLOW, end="")
                        TeleportCursor(SubBoardLocationHeight + idx, SubBoardLocationWidth)
                        print(x, end="")
                    print(COLOR_LIGHT_BLUE, end="")
            win = CheckWinner(PlayerBoardWin1)
            if win:
                EndMessage("X Won", Screen_width, Screen_Height)
                break
            Icon = "O"
        else:
            LocationY = SubBoardLocations[Choise-1][0]
            LocationX = SubBoardLocations[Choise-1][1]
            TeleportCursor(LocationY, LocationX)
            Player = Player2[CurrentSelectedBoard-1]
            Icon = "O"
            print(COLOR_GREEN + Icon, end="")
            # Saves the player move, in the player which just got set to current board
            Player[Choise-1] = True
            win = CheckWinner(Player)
            if win:
                PlayerBoardWin2[CurrentSelectedBoard-1] = True
                # some way to render the win
                SubBoardLocationHeight = SubBoardLocations[0][0] - 1 # top left corner location of subboard
                SubBoardLocationWidth = SubBoardLocations[0][1] - 2 # top left corner location of subboard
                for idx, x in enumerate(BigO):
                    TeleportCursor(SubBoardLocationHeight + idx, SubBoardLocationWidth)
                    print(x, end="")
            else:
                if len(BoardSpaces[CurrentSelectedBoard-1]) == 0:
                    PlayerBoardWin2[CurrentSelectedBoard-1] = True
                    # some way to render the tie
                    SubBoardLocationHeight = SubBoardLocations[0][0] - 1 # top left corner location of subboard
                    SubBoardLocationWidth = SubBoardLocations[0][1] - 2 # top left corner location of subboard
                    for idx, x in enumerate(BTie):
                        TeleportCursor(SubBoardLocationHeight + idx, SubBoardLocationWidth)
                        print(x, end="")
            win = CheckWinner(PlayerBoardWin2) # need to add all the tie things idk.
            if win:
                EndMessage("O Won", Screen_width, Screen_Height)
                break
            Icon = "X"
        # gives palyer new board
        if PlayerBoardTie[Choise - 1] == True or PlayerBoardWin1[Choise - 1] == True or PlayerBoardWin2[Choise - 1] == True:
            HaveNoBoardSlected = False
        else:
            CurrentSelectedBoard = Choise
            HaveNoBoardSlected = True
        # incriment round

        Round = Round + 1



if __name__=="__main__":
    TicTacToe()
