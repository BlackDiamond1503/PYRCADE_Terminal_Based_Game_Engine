import time
import sys
import pynput
import random
from typing import Literal, Tuple
from copy import deepcopy

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

sprite_color_codes = {"k" : black.fg(), 
                      "K" : intense_black.fg(), 
                      "r" : red.fg(),
                      "R" : intense_red.fg(),
                      "g" : green.fg(),
                      "G" : intense_green.fg(),
                      "y" : yellow.fg(),
                      "Y" : intense_yellow.fg(),
                      "b" : blue.fg(),
                      "B" : intense_blue.fg(),
                      "p" : purple.fg(),
                      "P" : intense_purple.fg(),
                      "c" : cyan.fg(),
                      "C" : intense_cyan.fg(),
                      "w" : white.fg(),
                      "W" : intense_white.fg()}

class sprite:
    def __init__(self, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel", "sub_pixel"] = "single", color_data: list[str] = None, fg_color: str = intense_cyan.fg()):
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self.fg = fg_color
        if color_data == None:
            if color_mode == "sub_pixel":
                color_data = []
                for px in range(len(sprite_data)):
                    color_data.append(["   "])
            elif color_mode == "pixel":
                color_data = []
                for px in range(len(sprite_data)):
                    color_data.append([" "])
            elif color_mode == "single":
                color_data = " "
        self.readable_data = (sprite_data, color_data)
    
    def data(self):
        pixel_data = self.readable_data[0]                                                 
        color_data = self.readable_data[1]                                                 
        pixel_raw_data = []
        color_raw_data = []                                                    
        for row in range(self.height):                                                                                                                                        
            for pixel in range(self.width):
                index = (row * self.width) + pixel
                if self.color_mode == "sub_pixel":                                     
                    if pixel_data[index] != "nop":                                                                                          
                        engine_pixel_data = ""
                        engine_color_data = ""                                                 
                        for sub_pixel in range(len(pixel_data[index])):
                            if color_data[index][sub_pixel] == " ":
                                engine_color_data += ""
                                engine_pixel_data += str(pixel_data[index][sub_pixel])
                            else:
                                engine_color_data += str(sprite_color_codes.get(color_data[index][sub_pixel], ""))
                                engine_pixel_data += str(pixel_data[index][sub_pixel])
                        pixel_raw_data.append(engine_pixel_data)
                        color_raw_data.append(engine_color_data)
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")  
                elif self.color_mode == "pixel":
                    if pixel_data[index] != "nop":
                        if color_data[index] == " ":
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append("")
                        else:
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append(str(sprite_color_codes.get(color_data[index], "")))
                    else:
                        pixel_raw_data.append("nop")
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
        self.pixel_memory = []
        self.color_memory = []
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
                    self.pixel_memory[y][x][layer] = f"{pixel}"
                    self.color_memory[y][x][layer] = f"{bg}{fg}"
                else:
                    self.pixel_memory[y][x][layer] = f"{pixel}"
                    self.color_memory[y][x][layer] = f"{self.color_memory[y][x][0]}{fg}"
            x += 1

    def create_sprite(self, x: int, y: int, layer: int, sprite: sprite):
        pixel_write_data, color_write_data = sprite.data()
        for row in range(sprite.height):
            for column in range(sprite.width):
                if layer != 0:
                    if pixel_write_data[(row * sprite.width) + column] != "nop":
                        self.pixel_memory[y + row][x + column][layer] = pixel_write_data[(row * sprite.width) + column]
                    else:
                        self.pixel_memory[y + row][x + column][layer] = "   "
                        self.color_memory[y + row][x + column][layer] = ""

    def create_pixel(self, x: int, y: int, layer: int, pixel_data: Tuple[str, str, str]):
        px, fg, bg = pixel_data
        if layer != 0:
            if bg != "":
                self.pixel_memory[y][x][layer] = f"{px}"
            else:
                self.pixel_memory[y][x][layer] = f"{px}"

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
        self.pixel_memory = deepcopy(self.pixel_blank)

    def bake_screen(self):
        final_bake = []
        for height_line in range(self.height):
            final_bake.append([])
            layered_pixel = ""
            layered_color = ""
            for width_line in range(self.width):
                pixel = self.pixel_memory[height_line][width_line][0]
                color = self.color_memory[height_line][width_line][0]
                layered_pixel = self.pixel_memory[height_line][width_line]
                layered_color = self.color_memory[height_line][width_line]
                for pixel_data in layered_pixel:
                    if pixel_data != "   ":
                        pixel = pixel_data
                final_bake[height_line].append(pixel)
                for color_data in layered_color:
                    if color_data != "":
                        if color_data[2] == "3":
                            color = color_data
                        elif color_data[2] == "4":
                            color += color_data
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