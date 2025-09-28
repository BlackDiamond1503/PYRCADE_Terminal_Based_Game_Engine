import time, os, sys, pynput, random, datetime
from typing import Literal, Tuple
from copy import deepcopy

initial_datetime = ""
def log(type: Literal["initial", "system", "warning", "info", "error"], message = None):
    global initial_datetime
    date_and_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    if type == "initial":
        with open(f"logs/{date_and_time} - pynput_log", "w") as log_file:
            log_file.write(f"{date_and_time} - pyrcade engine starting...\n")
            log_file.write(f"{date_and_time} - starting logging system...\n")
            initial_datetime = date_and_time
    elif type == "system":
        with open(f"logs/{initial_datetime} - pynput_log", "a") as log_file:
            log_file.write(f"{date_and_time} - system - {message}\n")
    elif type == "warning":
        with open(f"logs/{initial_datetime} - pynput_log", "a") as log_file:
            log_file.write(f"{date_and_time} - warning - {message}\n")
    elif type == "info":
        with open(f"logs/{initial_datetime} - pynput_log", "a") as log_file:
            log_file.write(f"{date_and_time} - info - {message}\n")
    elif type == "error":
        with open(f"logs/{initial_datetime} - pynput_log", "a") as log_file:
            log_file.write(f"{date_and_time} - error - {message}\n")
    else:
        with open(f"logs/{initial_datetime} - pynput_log", "a") as log_file:
            log_file.write(f"{date_and_time} - error - invalid log message!\n")

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

log("system", "starting color module...")
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

log("system", "starting color codes translator dictionary...")
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

log("system", "starting sprite module...")
class sprite:
    def __init__(self, name, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel", "sub_pixel"] = "single", color_data: list[str] = None, fg_color: str = intense_cyan.fg):
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self.fg = fg_color
        self.valid_data = True
        if color_data != list:
            log("error", f"invalid color data! sprite:{name}, color_data.type:{type(color_data)}")
            if color_mode == "pixel":
                color_data = []
                for px in range(len(sprite_data)):
                    color_data.append(" ")
            elif color_mode == "single":
                color_data = " "
        self.readable_data = (sprite_data, color_data)
        if (len(sprite_data) != len(color_data)) or (len(sprite_data) != self.width * self.height):
            self.valid_data = False
            log("error", f"invalid sprite data! sprite:{name}, intended_data.size:{width*height}, sprite_data.size:{len(sprite_data)}, color_data.size:{len(color_data)}")
    
    def data(self):
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
                        color_raw_data.append(color_data)
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
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
                if bg != "":
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{bg}{fg}"
                else:
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{fg}"
            x += 1

    def create_sprite(self, x: int, y: int, layer: int, sprite: sprite):
        sprite_data = sprite.data()
        if sprite_data == None:
            return
        pixel_write_data, color_write_data = sprite_data
        for row in range(sprite.height):
            for column in range(sprite.width):
                if layer != 0:
                    if pixel_write_data[(row * sprite.width) + column] != "nop":
                        self.pixel_layers[y + row][x + column][layer] = pixel_write_data[(row * sprite.width) + column]
                        self.color_layers[y + row][x + column][layer] = color_write_data[(row * sprite.width) + column]
                    else:
                        self.pixel_layers[y + row][x + column][layer] = "   "
                        self.color_layers[y + row][x + column][layer] = ""

    def create_pixel(self, x: int, y: int, layer: int, pixel_data: Tuple[str, str, str]):
        px, fg, bg = pixel_data
        if layer != 0:
            if bg != "":
                self.pixel_layers[y][x][layer] = f"{px}"
                self.color_layers[y][x][layer] = f"{bg}{fg}"
            else:
                self.pixel_layers[y][x][layer] = f"{px}"
                self.color_layers[y][x][layer] = f"{fg}"

    def initialize(self, layers: int, bg_color: str):
        self.layers = layers
        self.bg_color = bg_color
        worklist = []
        for height_line in range(self.height):
            worklist.append([])
            for width_line in range(self.width):
                worklist[height_line].append([])
                for layer in range(self.layers):
                    if layer == 0:
                        worklist[height_line][width_line].append("nop")
                    else:
                        worklist[height_line][width_line].append("   ")
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
                foreground = False
                for pixel_data in layered_pixel:
                    if pixel_data != "   ":
                        pixel = pixel_data
                pixel_bake.append(pixel)
                last_color = ""
                foreground = False
                for color_data in layered_color:
                    if color_data != "":
                        if color_data.startswith("\u001b[38") and foreground == False:
                            color = color_data
                            foreground = True

                            last_color = color_data
                        elif color_data.startswith("\u001b[38") and foreground == True:
                            bg_remap = "\u001b[48" + last_color[4:]
                            color = bg_remap + color_data
                            last_color = color_data
                            foreground = True
                        elif color_data.startswith("\u001b[48"):
                            color += color_data
                        else:
                            color = ""
                color_bake.append(color)
                last_color = ""
                foreground = False
            for item in range(len(pixel_bake)):
                final_bake[height_line].append(color_bake[item] + pixel_bake[item])
        self.screen = final_bake
    
    def print_screen(self):
        sys.stdout.write("\033[H")
        screen_print = ""
        for height_line in self.screen:
            for width_line in height_line:
                screen_print += width_line
            screen_print += "\n"
        sys.stdout.write(screen_print)
        sys.stdout.flush()

class arcade:
    def __init__(self, arcade_name: str, screen: screen, type: str):
        self.arcade_name = arcade_name
        self.screen = screen
        self.type = type

    def start_machine(self, mainloop_code: callable):
        if self.type == "main":
            print(f"starting main machine {self.arcade_name}...")
        elif self.type == "secondary":
            print(f"starting secondary machine {self.arcade_name}...")
        print("entering mainloop...")
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        mainloop_code()