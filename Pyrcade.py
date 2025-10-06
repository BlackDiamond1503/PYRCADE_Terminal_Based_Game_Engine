import time, sys, pynput, random, datetime
from typing import Literal, Tuple
from copy import deepcopy

DEBUG = True
initial_datetime = ""
def log(type: Literal["initial", "system", "warning", "info", "error", "arcade"], message = None):
    if DEBUG == True:
        global initial_datetime
        date_and_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        if type == "initial":
            with open(f"logs/{date_and_time} - pyrcade_log.txt", "w", encoding="utf-8") as log_file:
                log_file.write(f"{date_and_time} - pyrcade engine starting...\n")
                log_file.write(f"{date_and_time} - starting logging system...\n")
                initial_datetime = date_and_time
        else:
            with open(f"logs/{initial_datetime} - pyrcade_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{date_and_time} - {type} - {message}\n")

log("initial")
log("system", "loading foreground color ansi escape codes...")
fgcolor = {"black"          : "\u001b[38;5;0m", 
           "red"            : "\u001b[38;5;1m",
           "green"          : "\u001b[38;5;2m",
           "yellow"         : "\u001b[38;5;3m",
           "blue"           : "\u001b[38;5;4m",
           "purple"         : "\u001b[38;5;5m",
           "cyan"           : "\u001b[38;5;6m",
           "white"          : "\u001b[38;5;7m",
           "intense_black"  : "\u001b[38;5;8m", 
           "intense_red"    : "\u001b[38;5;9m",
           "intense_green"  : "\u001b[38;5;10m",
           "intense_yellow" : "\u001b[38;5;11m",
           "intense_blue"   : "\u001b[38;5;12m",
           "intense_purple" : "\u001b[38;5;13m",
           "intense_cyan"   : "\u001b[38;5;14m",
           "intense_white"  : "\u001b[38;5;15m"}

log("system", "loading background color ansi escape codes...")
bgcolor = {"black"          : "\u001b[48;5;0m", 
           "red"            : "\u001b[48;5;1m", 
           "green"          : "\u001b[48;5;2m",
           "yellow"         : "\u001b[48;5;3m",
           "blue"           : "\u001b[48;5;4m",
           "purple"         : "\u001b[48;5;5m",
           "cyan"           : "\u001b[48;5;6m",
           "white"          : "\u001b[48;5;7m",
           "intense_black"  : "\u001b[48;5;8m", 
           "intense_red"    : "\u001b[48;5;9m",
           "intense_green"  : "\u001b[48;5;10m",
           "intense_yellow" : "\u001b[48;5;11m",
           "intense_blue"   : "\u001b[48;5;12m",
           "intense_purple" : "\u001b[48;5;13m",
           "intense_cyan"   : "\u001b[48;5;14m",
           "intense_white"  : "\u001b[48;5;15m"}

class color: 
    def __init__(self, colorkey: str):
        self.fg = fgcolor[colorkey]
        self.bg = bgcolor[colorkey]

log("system", "loading color pallette with color module...")
black = color("black")  
intense_black = color("intense_black")  
red = color("red")
intense_red = color("intense_red")
green = color("green")
intense_green = color("intense_green")
yellow = color("yellow")
intense_yellow = color("intense_yellow")
blue = color("blue")
intense_blue = color("intense_blue")
purple = color("purple")
intense_purple = color("intense_purple")
cyan = color("cyan")
intense_cyan = color("intense_cyan")
white = color("white")
intense_white = color("intense_white")

sprite_color_codes = {"k" : black.fg, 
                      "K" : intense_black.fg, 
                      "r" : red.fg,
                      "R" : intense_red.fg,
                      "g" : green.fg,
                      "G" : intense_green.fg,
                      "y" : yellow.fg,
                      "Y" : intense_yellow.fg,
                      "b" : blue.fg,
                      "B" : intense_blue.fg,
                      "p" : purple.fg,
                      "P" : intense_purple.fg,
                      "c" : cyan.fg,
                      "C" : intense_cyan.fg,
                      "w" : white.fg,
                      "W" : intense_white.fg}

class sprite:
    def __init__(self, name, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel"] = "single", color_data: list[str] = None, sprite_mode: Literal["single", "multi"] = "single", sprite_cuantity: int = 1):
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self.valid_data = True
        self.name = name
        self.sprite_mode = sprite_mode
        self.sprite_cuantity = sprite_cuantity
        if type(color_data) != list and color_mode == "pixel":
            log("warning", f"empty color data! color data will be initialized.\n    extra data:\n    sprite_name:{name}\n    color_data_type:{type(color_data)}")
            color_data = []
            for px in range(len(sprite_data)):
                color_data.append(" ")
        elif type(color_data) != str and color_mode == "single":
            log("warning", f"empty color data! color data will be initialized.\n    extra data:\n    sprite_name:{name}\n    color_data_type:{type(color_data)}")
            color_data = " "
        elif  (len(sprite_data) != self.width * self.height) and self.sprite_mode == "single":
            self.valid_data = False
            log("error", f"invalid sprite data!\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif (len(sprite_data) != self.width * self.height * self.sprite_cuantity) and self.sprite_mode == "multi":
            self.valid_data = False
            log("error", f"invalid sprite data!\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height*self.sprite_cuantity}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif len(sprite_data) != len(color_data) and color_mode == "pixel":
            self.valid_data = False
            log("error", f"invalid sprite data!\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        self.readable_data = (sprite_data, color_data)
        if self.color_mode == "pixel":
            for idx, entry in enumerate(color_data):
                if sprite_color_codes.get(entry, "") == "":
                    log("error", f"invalid color code!\n    extra data:\n    sprite_name:{self.name}\n    color_mode: {self.color_mode}\n    invalid_entry:{entry}\n    invalid_index:{idx}")
                    break
        elif self.color_mode == "single":
            if sprite_color_codes.get(color_data, "") == "":
                log("error", f"invalid color code!\n    extra data:\n    sprite_name:{self.name}\n    color_mode: {self.color_mode}\n    color_data:{color_data}")

    def load_raw(self):
        if self.valid_data == False:
            return
        pixel_data = self.readable_data[0]                                                 
        color_data = self.readable_data[1]                                                 
        pixel_raw_data = []
        color_raw_data = []                                                    
        for row in range(self.height):                                                                                                                                        
            for pixel in range(self.width):
                index = (row * self.width) + pixel
                if self.color_mode == "pixel":
                    if pixel_data[index] != "nop":
                        if color_data[index] == " ":
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append("")
                        else:
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append(str(sprite_color_codes.get(color_data[index], "")))
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
                elif self.color_mode == "single":
                    if pixel_data[index] != "nop":
                        pixel_raw_data.append(pixel_data[index])
                        color_raw_data.append(sprite_color_codes.get(color_data, ""))
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
        #log("info", f"sprite_raw_data dump\n    sprite_name: {self.name}\n    pixel_raw_data: {pixel_raw_data}\n    color_raw_data: {color_raw_data}\n ")
        return (pixel_raw_data, color_raw_data)   

class screen:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.screen = []
        self.pixel_layers = []
        self.color_layers = []
        self.pixel_blank = []
        self.color_blank = []

    def create_text(self, x: int, y: int, layer: int, text_data: Tuple[str, str, str]):
        text, fg, bg = text_data
        workvar = ""
        text_pixel_data = []
        for character in text:
            workvar += character
            if len(workvar) == 3:
                text_pixel_data.append(workvar)
                workvar = ""
        for pixel in text_pixel_data:
            if layer != 0:
                if (0 <= x < self.width) and (0 <= y < self.height):
                    continue
                elif bg != "":
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{bg}{fg}"
                else:
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{fg}"
            x += 1

    def create_sprite(self, x: int, y: int, layer: int, sprite_data_raw: tuple, sprite_num: int = 0, sprite: sprite = None):
        sprite_data = sprite_data_raw
        offset = (sprite.height * sprite.width) * sprite_num
        if sprite_data == None or sprite == None:
            return
        pixel_write_data, color_write_data = sprite_data
        for row in range(sprite.height):
            for column in range(sprite.width):
                if (layer != 0) and ((0 <= x + column < self.width) and (0 <= y + row < self.height)):
                    if pixel_write_data[offset + (row * sprite.width) + column] != "nop":
                        self.pixel_layers[y + row][x + column][layer] = pixel_write_data[offset + (row * sprite.width) + column]
                        self.color_layers[y + row][x + column][layer] = color_write_data[offset + (row * sprite.width) + column]
                    else:
                        self.pixel_layers[y + row][x + column][layer] = "   "
                        self.color_layers[y + row][x + column][layer] = ""

    def create_pixel(self, x: int, y: int, layer: int, pixel_data: Tuple[str, str, str]):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        px, fg, bg = pixel_data
        if layer != 0:
            if bg != "":
                self.pixel_layers[y][x][layer] = f"{px}"
                self.color_layers[y][x][layer] = f"{bg}{fg}"
            else:
                self.pixel_layers[y][x][layer] = f"{px}"
                self.color_layers[y][x][layer] = f"{fg}"

    def initialize(self, layers: int, bg_color: str):
        log("system", "initializing screen...")
        self.layers = layers
        self.bg_color = bg_color
        worklist = []
        for height_line in range(self.height):
            worklist.append([])
            for width_line in range(self.width):
                worklist[height_line].append([])
                for layer in range(self.layers):
                    worklist[height_line][width_line].append("nop")
        self.pixel_blank = worklist 
        worklist = []
        for height_line in range(self.height):
            worklist.append([])
            for width_line in range(self.width):
                worklist[height_line].append([])
                for layer in range(self.layers):
                    if layer == 0:
                        worklist[height_line][width_line].append(self.bg_color)
                    else:
                        worklist[height_line][width_line].append("")
        self.color_blank = worklist 

    def memory_reset(self):
        self.pixel_layers = deepcopy(self.pixel_blank)
        self.color_layers = deepcopy(self.color_blank)

    def bake_screen(self):
        final_bake = []
        for height_line in range(self.height):
            final_bake.append([])
            pixel_bake = []
            color_bake = []
            layered_pixel = ""
            layered_color = ""
            for width_line in range(self.width):
                pixel = self.pixel_layers[height_line][width_line][0]
                color = self.color_layers[height_line][width_line][0]
                layered_pixel = self.pixel_layers[height_line][width_line]
                layered_color = self.color_layers[height_line][width_line]
                found = False
                for layer in range(len(layered_pixel)):
                    if layered_pixel[layer] != "nop" and layered_color[layer] != "nop":
                        pixel = layered_pixel[layer]
                        color = layered_color[layer]
                        found = True
                if found == False:
                    pixel = "   "
                    color = layered_color[0]
                pixel_bake.append(pixel)
                color_bake.append(color)
            for item in range(len(pixel_bake)):
                final_bake[height_line].append(color_bake[item] + pixel_bake[item] + "\033[0m")
        self.screen = final_bake
    
    def print_screen(self):
        screen_print = ""
        for height_line in self.screen:
            for width_line in height_line:
                screen_print += width_line
            screen_print += "\n\033[0m"
        sys.stdout.write("\033[2J\033[H\n" + screen_print)
        sys.stdout.flush()

default_keymap = {"up"          : pynput.keyboard.Key.up, 
                  "down"        : pynput.keyboard.Key.down,
                  "left"        : pynput.keyboard.Key.left,
                  "right"       : pynput.keyboard.Key.right,
                  "space"       : pynput.keyboard.Key.space,
                  "esc"         : pynput.keyboard.Key.esc,
                  "enter"       : pynput.keyboard.Key.enter,
                  "backspace"   : pynput.keyboard.Key.backspace}

class arcade:
    def __init__(self, arcade_name: str, screen: screen, type: Literal["main", "secondary"], key_map: dict = default_keymap):
        self.arcade_name = arcade_name
        self.screen = screen
        self.type = type
        self.input = ""
        self.key_map = key_map

    def start_machine(self, mainloop_code: callable):
        log("arcade", f"starting arcade machine {self.arcade_name}...\n    arcade info:\n    name: {self.arcade_name}\n    type: {self.type}")
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        mainloop_code()
    
    def start_input(self, keys: list = ["up", "down", "left", "right", "space", "esc"]):
        log("arcade", f"arcade {self.arcade_name} started input logger")
        self.input = ""
        self.keys = keys
        def input_logger(keypressed):
            last_input = None
            for key in self.keys:
                if self.key_map[key] == keypressed:
                    self.input = key
                    last_input = key
            if last_input == None:
                self.input == "none"
        listener = pynput.keyboard.Listener(on_press = input_logger)
        listener.start()
                
#Tetris
tetris_screen = screen(20, 20)
tetris = arcade("pyrcade_tetris", tetris_screen, "secondary")
def tetris_loop():
    #tetris pieces sprites
    sprites_data = ["███", "███", 
                    "███", "███"]
    colors_data = "y"
    tetromino1_1 = sprite("tetromino1", 2, 2, sprites_data, "single", colors_data, intense_yellow.fg)
    piece = False
    pieces = [tetromino1_1]
    tetris_screen.initialize(5, intense_cyan.bg)
    bgpieces= []
    piece
    game_field = []
    #game loop
    def check_pieces(y, row):
        screen_line = game_field[y + row]
        if screen_line == (["███"] * 10):
            return True
    while True:
        gravity = 1
        tetris_screen.memory_reset()
        if tetris.input == "left":
            if (x > 5) and not (tetris.screen.pixel_layers[y][x - 1][1] == "███" or tetris.screen.pixel_layers[y + 1][x - 1][1] == "███"):
                x -= 1
                tetris.input = ""
        elif tetris.input == "right":
            if (x < 15 - random_piece.width) and not (tetris.screen.pixel_layers[y][x + random_piece.width][1] == "███" or tetris.screen.pixel_layers[y + 1][x + random_piece.width][1] == "███"):
                x += 1
                tetris.input = ""
        elif tetris.input == "down":
            gravity = 3
            tetris.input = ""
        if piece == False:
            piece = True
            random_piece = random.choice(pieces)
            x = 10
            y = 0
        for bg in bgpieces:
            tetris_screen.create_sprite(bg[0], bg[1]-1, 1, bg[2].load_raw(), 0, bg[2])
        piece_found = False
        if piece == True:
            for i in range(gravity):
                for px in range(random_piece.width):
                    tetris_screen.create_pixel(x + px, y + random_piece.height + 1, 3, ("███", "", intense_red.fg)) #debug draw
                    if ((y + random_piece.height) >= tetris_screen.height) or (tetris_screen.pixel_layers[y + random_piece.height][x + px][1] == "███") or (y > tetris_screen.height - random_piece.height):
                        piece_found = True
                        piece = False
                        bgpieces.append((x, y + 1, random_piece))
                if piece_found == False:
                    y += 1
            tetris_screen.create_sprite(x, y, 2, random_piece.load_raw(), 0, random_piece)
        if piece_found == True:
            for row in range(random_piece.height):
                if check_pieces(y, row):
                    for xp in range(tetris_screen.width):
                        tetris_screen.pixel_layers[y + row][xp][1] = "nop"
                        tetris_screen.color_layers[y + row][xp][1] = ""
        for row_line in range(len(tetris_screen.pixel_layers)):
            row_data = []
            for width in range(tetris_screen.width):
                if width > 4 and width < 15:
                    row_data.append(tetris_screen.pixel_layers[row_line][width][1])
            game_field.append(row_data)
        log("arcade", f"game_field dump:\n{game_field}")
        tetris_screen.bake_screen()
        tetris_screen.print_screen()
        time.sleep(0.2)
tetris.start_input()
tetris.start_machine(tetris_loop)