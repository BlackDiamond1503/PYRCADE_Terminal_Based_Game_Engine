import time
import os
import pynput
import random
import sys

#Basic Functions

#   Basic Input per Game
Game_Input = ""
movementVec = [0, 0]
def MovementKeys(keypressed):
    global Game_Input
    global movementVec
    if game == 1:
        if (keypressed == pynput.keyboard.Key.up) and not (lasdir == [0, 1]):
            movementVec = [0, -1]
        elif (keypressed == pynput.keyboard.Key.down) and not (lasdir == [0, -1]):
            movementVec = [0, 1]
        elif (keypressed == pynput.keyboard.Key.left) and not (lasdir == [1, 0]):
            movementVec = [-1, 0]
        elif (keypressed == pynput.keyboard.Key.right) and not (lasdir == [-1, 0]):
            movementVec = [1, 0]
        elif keypressed == pynput.keyboard.Key.esc:
            movementVec = [0, 0]
    elif game == 0:
        if (keypressed == pynput.keyboard.Key.up):
            Game_Input = "change"
        elif (keypressed == pynput.keyboard.Key.down):
            Game_Input = "change"
        elif (keypressed == pynput.keyboard.Key.left):
            Game_Input = "left"
        elif (keypressed == pynput.keyboard.Key.right):
            Game_Input = "right"
        elif (keypressed == pynput.keyboard.Key.enter):
            Game_Input = "select"
    elif game == 2:
        if (keypressed == pynput.keyboard.Key.up) or (keypressed == pynput.keyboard.Key.space):
            Game_Input = "jump"

input = pynput.keyboard.Listener(on_press = MovementKeys)
input.start()

#   Create Pixel
def cpixel(y = 0, x = 0, color = "\u001b[38;5;15m", pixel = "███", fondo = "\033[48;5;0m"):
    global screen
    if (x >= 0 and x < screenwid) and (y >= 0 and y < screenhei) and (pixel != "nop"):
        screen[y][x][0] = f"{color}{fondo}{pixel}"
    else:
        pass

#   Sprite Printing
def pntsprite(parameters, x = 0, y = 0):
    for spritepx in range(len(parameters[0])):
        if (int(x + ((spritepx) % parameters[2])) >= 0 and int(x + ((spritepx) % parameters[2])) < screenwid) and (int(y + ((spritepx) // parameters[2])) >= 0 and int(y + ((spritepx) // parameters[2])) < screenhei) and (parameters[0][spritepx] != "nop"):
            if (parameters[3] == "single"):
                screen[int(y + ((spritepx) // parameters[2]))][int(x + ((spritepx) % parameters[2]))][0] = f"{parameters[5]}{parameters[4]}{parameters[0][spritepx]}"
            if (parameters[3] == "pixel"):
                screen[int(y + ((spritepx) // parameters[2]))][int(x + ((spritepx) % parameters[2]))][0] = f"{parameters[5]}{parameters[0][spritepx]}"
            if (parameters[3] == "full"):
                screen[int(y + ((spritepx) // parameters[2]))][int(x + ((spritepx) % parameters[2]))][0] = f"{parameters[0][spritepx]}"

#   Sprites XD
def sprite(name = ""):
    #   logo
    if name == "logo":
        sprite = ["\u001b[38;5;21m█▀▀", "▀▄ ", "\u001b[38;5;11m█  ", " █ ", "\u001b[38;5;255m█▀▀", "▀▄ ", "▄▀▀", "▀▀▀", " ▄▀", "▀▀▄", " █▀", "▀▀▄", " █▀", "▀▀▀", 
                  "\u001b[38;5;21m█▄▄", "▄▀ ", "\u001b[38;5;11m ▀▄", "▀  ", "\u001b[38;5;255m█▄▄", "▄▀ ", "█  ", "   ", " █▄", "▄▄█", " █ ", "  █", " █▄", "▄▄▄",
                  "\u001b[38;5;21m█  ", "   ", "\u001b[38;5;11m  █", "   ", "\u001b[38;5;255m█  ", " █ ", "▀▄▄", "▄▄▄", " █ ", "  █", " █▄", "▄▄▀", " █▄", "▄▄▄"]
        hei = 3
        wid = 14
        colormode = "pixel"
        color = "\u001b[38;5;14m"
        background = "\u001b[48;5;17m"
    elif name == "menu1":
        sprite = ["Sel", "ect", "  G", "ame",
                  "   ", " Ex", "it ", "   "]
        hei = 2
        wid = 4
        colormode = "single"
        color = "\u001b[38;5;255m"
        background = "\u001b[48;5;17m"
    elif name == "menu2":
        sprite = ["\u001b[48;5;40m\u001b[38;5;255m█▀▀", "\u001b[48;5;40m▀▀▀", "\u001b[48;5;40m▀▀█", "\u001b[48;5;17m   ",                                                   "\u001b[48;5;14m█▀▀", "\u001b[48;5;14m▀\u001b[48;5;40m▀\u001b[48;5;14m▀", "\u001b[48;5;14m▀▀█", "\u001b[48;5;17m   ", "   ",                    "█▀▀", "▀▀▀", "▀▀█", "   ", "█▀▀", "▀▀▀", "▀▀█", 
                  "\u001b[48;5;40m\u001b[38;5;255m█\u001b[38;5;21m▀▀", "\u001b[48;5;40m▀█▄", "\u001b[48;5;40m \u001b[38;5;160m▄\u001b[38;5;255m█", "\u001b[48;5;17m   ",    "\u001b[48;5;14m█\u001b[38;5;11m▄ ", "\u001b[48;5;14m   ", "\u001b[48;5;14m\u001b[38;5;40m▄\u001b[38;5;255m █", "\u001b[48;5;17m   ", "   ",    "█  ", "   ", "  █", "   ", "█  ", "   ", "  █",
                  "\u001b[48;5;40m\u001b[38;5;255m█▄▄", "\u001b[48;5;40m▄▄▄", "\u001b[48;5;40m▄▄█", "\u001b[48;5;17m   ",                                                   "\u001b[48;5;14m█▄▄", "\u001b[48;5;14m▄\u001b[48;5;40m▄\u001b[48;5;14m▄", "\u001b[48;5;40m▄\u001b[48;5;14m▄█", "\u001b[48;5;17m   ", "   ",     "█▄▄", "▄▄▄", "▄▄█", "   ", "█▄▄", "▄▄▄", "▄▄█",
                  "\u001b[48;5;17m  S", "\u001b[48;5;17mnak", "\u001b[48;5;17me  ", "\u001b[48;5;17m   ",                                                                   "\u001b[48;5;17m  F", "\u001b[48;5;17mlap", "\u001b[48;5;17my  ", "\u001b[48;5;17m   ", "   ",                                                  "   ", "   ", "   ", "   ", "   ", "   ", "   ",
                  "\u001b[48;5;17m   ", "\u001b[48;5;17m   ", "\u001b[48;5;17m   ", "\u001b[48;5;17m   ",                                                                   "\u001b[48;5;17m  P", "\u001b[48;5;17mixe", "\u001b[48;5;17ml  "]
        hei = 5
        wid = 16
        colormode = "full"
        color = "\u001b[38;5;255m"
        background = "\u001b[48;5;17m"
    elif name == "menuselect":
        sprite = ["▲ ▲", " ▲ ", "▲ ▲"]
        hei = 1
        wid = 3
        colormode = "single"
        color = "\u001b[38;5;11m"
        background = "\u001b[48;5;17m"
    elif name == "tube":
        sprite = ["\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m██\u001b[38;5;22m█\033[0m",
                  "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m██\u001b[38;5;22m█\033[0m",
                  "nop", "nop", "nop",
                  "nop", "nop", "nop",
                  "nop", "nop", "nop",
                  "nop", "nop", "nop",
                  "nop", "nop", "nop",
                  "nop", "nop", "nop",
                  "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m██\u001b[38;5;22m█\033[0m",
                  "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m██\u001b[38;5;22m█\033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",
                  "\u001b[38;5;40m ██\033[0m", "\u001b[38;5;40m███\033[0m", "\u001b[38;5;40m█\u001b[38;5;22m█ \033[0m",]
        hei = 28
        wid = 3
        colormode = "pixel"
        color = "\u001b[38;5;46m"
        background = "\u001b[48;5;14m"
    #   Info Return
    return [sprite, hei, wid, colormode, color, background]

#   Sprite Animator


#   Text Printer
def pnttext(y = 0, x = 0, color = "\u001b[38;5;15m", text = "███", fondo = "\033[48;5;0m"):
    worklist = []
    workvar = ""
    pntlist = []
    for i in text:
        worklist.append(i)
        if len(worklist) == 3:
            for e in worklist:
                workvar = workvar + e
            worklist = []
            pntlist.append(workvar)
            workvar = ""
    for i in range(len(pntlist)):
        screen[y][x + i][0] = f"{color}{fondo}{pntlist[i]}"

#   Screen Clearing / Memory Updating
def CLS(fondo = "\033[0m", fondo2 = "\033[38;5;0m", mode = "single"):
    global screen
    global screenhei
    global screenwid
    flag = 0
    screen = []
    color = fondo
    if mode == "single":
        for hl in range(screenhei):
            screen.append([])
            for wl in range(screenwid):
                screen[hl].append([f"{fondo}   {"\033[0m"}", 0])
    elif mode == "chekers":
        for hl in range(screenhei):
            screen.append([])
            if flag == 0:
                flag = 1
            elif flag == 1:
                flag = 0
            for wl in range(screenwid):
                if flag == 0:
                    flag = 1
                    color = fondo2
                elif flag == 1:
                    flag = 0
                    color = fondo
                screen[hl].append([f"{color}   {"\033[0m"}", 0])

#   Screen Printing
def PRS():
    global screen
    global screenhei
    global screenwid
    screenpnt = ""
    #os.system("cls")
    sys.stdout.write("\033[2J\033[H")
    for hl in range(screenhei):
        line = ""
        for wl in range(screenwid):
            line += str(screen[hl][wl][0])
        screenpnt += f"{line}\n"
    #print(line)
    #os.system(f"echo {line}")
    sys.stdout.write(screenpnt)
    sys.stdout.flush()

#General Variables
screenhei = 18
screenwid = 18
game = 0

#Variables Snake
screen = []

while game != -1:
    #Main Games Loop
    if game == 1:
        CLS(fondo = "\u001b[48;5;232m")
        pnttext(y = screenhei // 2, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = "Loading..", fondo = "\u001b[48;5;232m")
        PRS()
        time.sleep(1)
        #Snake
        death = 0
        screenhei = 18
        screenwid = 18
        x = (screenwid // 2) + 1
        y = (screenhei // 2) + 1
        fondo = "\u001b[48;5;34m"
        tailpos = []
        size = 1
        ax = random.randint(0, 16)
        ay = random.randint(0, 16)
        while True:
            lasdir = movementVec
            breackpoint = 0
            skipdel = 0
            CLS(fondo = fondo)
            if (x == ax) and (y == ay):
                size = size + 1
                ax = random.randint(0, screenwid - 1)
                ay = random.randint(0, screenhei - 1)
            if x == screenwid - 1 and movementVec == [1, 0]:
                death = 1
            elif x == 0 and movementVec == [-1, 0]:
                death = 1
            if y == screenhei - 1 and movementVec == [0, 1]:
                death = 1
            elif y == 0 and movementVec == [0, -1]:
                death = 1
            if size > len(tailpos) and death == 0:
                skipdel = 1
            tailpos.append([x, y])
            if skipdel == 0 and death == 0:
                tailpos.pop(0)
            for cord in tailpos:
                if [ax, ay] == cord:
                    ax = random.randint(0, screenwid - 1)
                    ay = random.randint(0, screenhei - 1)
                    break
                else:
                    pass
            if death == 0:
                x = x + movementVec[0]
                y = y + movementVec[1]
            cpixel(x = abs(ax), y = abs(ay), color = "\u001b[38;5;160m")
            for piece in tailpos:
                cpixel(x = abs(piece[0]), y = abs(piece[1]), color = "\u001b[38;5;18m")
            for piece in tailpos:
                if ((x == piece[0]) and (y == piece[1])) and size > 3:
                    death = 1
            if death == 1:
                fondo = "\u001b[48;5;240m"
                CLS(fondo = fondo)
                pnttext(y = screenhei // 2, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = " Game  Over ", fondo = "\u001b[48;5;240m")
                pnttext(y = screenhei // 2 + 1, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = "Press  Enter", fondo = "\u001b[48;5;240m")
                game = 0
                if Game_Input == "select":
                    Game_Input == "none"
                    break
            cpixel(x =abs(x),y=abs(y),color="\u001b[38;5;20m")
            PRS()
            print("Points:", size - 1)
            time.sleep(0.2)
    elif game == 0:
        CLS(fondo = "\u001b[48;5;232m")
        pnttext(y = screenhei // 2, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = "Loading..", fondo = "\u001b[48;5;232m")
        PRS()
        time.sleep(1)
        Game_Input = "none"
        option = 0
        menu = 0
        gameoption = 0
        gamepositions = [1, 5, 10, 14]
        while True:
            CLS(fondo = "\u001b[48;5;17m")

            if menu == 0:
                pntsprite(parameters = sprite(name = "logo"), x = 2, y = 1)
                pntsprite(parameters = sprite(name = "menu1"), x = 7, y = 10)

                if Game_Input == "change":
                    if option == 1:
                        option = 0
                    else: 
                        option = 1
                elif Game_Input == "select":
                    if option == 0:
                        menu = 1
                    if option == 1:
                        game = -1
                        break
                Game_Input = "none"

                cpixel(y = 10 + option, x = 6, color = "\u001b[38;5;11m", pixel = " ► ", fondo = "\u001b[48;5;17m")
                cpixel(y = 10 + option, x = 11, color = "\u001b[38;5;11m", pixel = " ◄ ", fondo = "\u001b[48;5;17m")
            elif menu == 1:
                if Game_Input == "left":
                    gameoption = gameoption - 1
                    if gameoption < 0:
                        gameoption = 0
                elif Game_Input == "right":
                    gameoption = gameoption + 1
                    if gameoption > 3:
                        gameoption = 3
                elif Game_Input == "select":
                    game = gameoption + 1
                    Game_Input = "none"
                    break
                Game_Input = "none"
                pntsprite(parameters = sprite(name = "menu2"), x = 1, y = 1)
                pntsprite(parameters = sprite(name = "menuselect"), x = gamepositions[gameoption], y = 6)

            PRS()

            time.sleep(0.2)
    elif game == 2:
        CLS(fondo = "\u001b[48;5;232m")
        pnttext(y = screenhei // 2, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = "Loading..", fondo = "\u001b[48;5;232m")
        PRS()
        time.sleep(1)
        jumped = 0
        jumping = 0
        jumpcool = 0
        jumpingcool = 0
        stay_air = 0
        y = 4     
        lastjumpingcool = 0
        tubecool = 6
        ty = 0
        tubelist = []
        worklist = []
        death = 0
        points = int(0)
        while True:
            CLS(fondo = "\u001b[48;5;14m")
            lastjumpingcool = jumpingcool - 1

            if (Game_Input == "jump") and (jumping == 0) and (jumpcool == 0) and death == 0:
                jumped = 1
                jumping = 1
                jumpcool = 3
                stay_air = 0
                Game_Input = "none"
            elif (Game_Input == "jump") and jumping == 1 and death == 0:
                jumped = 0
                jumping = 1
                Game_Input = "none"
            elif (not Game_Input == "jump") and jumping == 1 and death == 0:
                jumped = 0
                jumping = 0
                Game_Input = "none"

            if jumped == 1 and death == 0:
                jumpingcool = 3
            if jumpingcool != 0 and death == 0:
                y = y - 1
                jumpingcool = jumpingcool - 1
            elif (jumpingcool == 0) and not (lastjumpingcool == 0) and (stay_air == 0) and death == 0:
                stay_air = 1
            elif death == 0:
                y = y + 1
                stay_air = 1
            if jumpcool != 0 and death == 0:
                jumpcool = jumpcool - 1

            if tubecool == 0 and death == 0:
                tubecool = 8
                ty = random.randint(-6, 0)
                tubelist.append([screenwid + 1, ty])
            elif death == 0:
                tubecool = tubecool - 1

            worklist = []
            w = 0
            for i in tubelist:
                pntsprite(parameters = sprite(name = "tube"), x = i[0], y = i[1])   
                if death == 0:
                    w = [i[0] - 1, i[1]]
                    if i[0] > -2:
                        worklist.append(w)
                    if i[0] == 1:
                        points = points + 1
                    tubelist = []
                    tubelist = worklist
            

            if (screen[y][2][0] != "\u001b[48;5;14m   \033[0m") and death == 0:
                death = 1
            
            if y >= screenhei - 1:
                death = 1

            if death == 1:
                fondo = "\u001b[48;5;240m"
                CLS(fondo = fondo)
                pnttext(y = screenhei // 2, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = " Game  Over ", fondo = "\u001b[48;5;240m")
                pnttext(y = screenhei // 2 + 1, x = screenwid // 2 - 2, color = "\u001b[38;5;255m", text = "Press  Enter", fondo = "\u001b[48;5;240m")
                game = 0
                if Game_Input == "select":
                    Game_Input == "none"
                    break

            cpixel(y = y, x = 2, color = "\u001b[38;5;11m")

            PRS()
            print("Points:", points)
            #print("Debug:", jumped, jumpcool, jumping, jumpingcool)
            #print("Debug:\n",points, "\n", tubelist, "\n", worklist)
            time.sleep(0.2)
os.system("cls")