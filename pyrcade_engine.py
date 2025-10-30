import time, sys, pynput, random, datetime, threading, os, string
from typing import Literal, Tuple
from copy import deepcopy
import customtkinter as ctk

DEBUG = True
log_filename = ""
def log(level: Literal["initial", "system", "warning", "info", "error", "arcade", "debug"] , message = None):
    """
    Logs a messeage to the log file with a timestamp and a type for debugging.

    Arguments:
        level:      The level of the log message, only for organizational purposes.
        message:    The message to log, useful for debugging.
    """
    
    if not DEBUG:
        return
    try:
        os.makedirs("logs", exist_ok=True)
    except Exception as e:
        print(f"[LOG ERROR] could not create logs directory: {e}")
        return

    global log_filename
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    level_str = str(level).upper()
    if message is not None:
        log_message = f"[{timestamp}] [{level_str}] {message}\n"
        try:
            if log_filename == "":
                log_filename = f"logs/pyrcade_log_{timestamp}.txt"
            with open(log_filename, "a") as log_file:
                log_file.write(log_message)
                return
        except Exception as e:
            print(f"[LOG ERROR] could not write to log file: {e}")
            return
    else:  
        return
    log_filename = f"logs/pyrcade_log_{initial_datetime}.txt"
        
log("system", "logging system initialized")
log("system", "pyrcade engine initializing...")

class ColorManager:
    """
    Manages all the color codes for the engine.

    Methods:
    --------
        fg(code):   Returns the ANSI escape code for the given foreground color code.
        bg(code):   Returns the ANSI escape code for the given background color code.
    """ 
    def __init__(self):
        pass
    
    def fg(self, code):
        return f"\u001b[38;5;{code}m"
    
    def bg(self, code):
        return f"\u001b[48;5;{code}m"

log("system", "loading color manager")

color = ColorManager()

preset_color_codes = {"k" : color.fg(0), 
                      "K" : color.fg(8), 
                      "r" : color.fg(1),
                      "R" : color.fg(9),
                      "g" : color.fg(2),
                      "G" : color.fg(10),
                      "y" : color.fg(3),
                      "Y" : color.fg(11),
                      "b" : color.fg(4),
                      "B" : color.fg(12),
                      "p" : color.fg(5),
                      "P" : color.fg(13),
                      "c" : color.fg(6),
                      "C" : color.fg(14),
                      "w" : color.fg(7),
                      "W" : color.fg(15)}

def ANSII_to_HEX(color_str: str):
    """
    NOT FOR PUBLIC USE\n
    Converts a raw ANSI Escape Color code into a HEX color string

    Arguments:
        color_str:  The ANSI escape color code string to convert.
    """
    color_code = ""
    for i in range(len(color_str) - 7):
        if color_str[i + 7] == "m":
            color_code = int(color_code)
            break
        else:
            color_code += color_str[i + 7]
    if 0 <= color_code <= 15:
        basic_colors = ["#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
                        "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff"]
        return basic_colors[color_code]
    elif 16 <= color_code <= 231:
        coloridx = color_code - 16
        r = coloridx // 36
        gbidx = coloridx % 36
        g = gbidx // 6
        b = gbidx % 6
        rgb_steps = ["00", "5f", "87", "af", "d7", "ff"]
        hex_color = f"#{rgb_steps[r]}{rgb_steps[g]}{rgb_steps[b]}"
        return hex_color
    elif 232 <= color_code <= 255:
        shades = ["08", "12", "1c", "26", "30", "3a", "44", "4e", "58", "62", "6c", "76", "80", "8a", "94", "9e", "a8", "b2", "bc", "c6", "d0", "da", "e4", "ee"]
        grayidx = color_code - 232
        shadeid = 8 + grayidx * 10
        shade = shades[shadeid - 8]
        hex_grey = f"#{shade}{shade}{shade}"
        return hex_grey
    return "#000000"

class Sprite:
    """
    Main sprite class for handling sprite graphic data.
    Arguments:
        name:           The name of the sprite.
        width:          The width of the sprite in pixels.
        height:         The height of the sprite in pixels.
        sprite_data:    A list of strings representing the pixel data of the sprite.
        color_mode:     The color mode of the sprite ("single", "pixel", "single_custom", "pixel_custom").
        color_data:     A list of strings representing the color data of the sprite.
        sprite_mode:    The sprite mode ("single" for single-frame sprites, "multi" for multi-frame sprites).
        sprite_cuantity:The number of frames in the sprite (only for multi-frame sprites).
    """
    def __init__(self, name: str, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel", "single_custom", "pixel_custom"] = "single", color_data: list[str] = None, sprite_mode: Literal["single", "multi"] = "single", sprite_cuantity: int = 1, extra_val_1 = None, extra_val_2 = None, extra_val_3 = None):
        """
        DO NOT USE THIS YOU ABSOLUTE MORON, IT AUTOMATICALLY INITIALIZES WHEN CREATING A Sprite OBJECT.
        """
        self.width = width
        self.height = height
        self._color_mode = color_mode
        self._valid_data = True
        self.name = name
        self.sprite_mode = sprite_mode
        self._sprite_cuantity = sprite_cuantity
        self.extra1 = extra_val_1
        self.extra2 = extra_val_2
        self.extra3 = extra_val_3

        # data type validator
        if type(color_data) != list and color_mode == "pixel":
            log("warning", f"empty color data detected; initializing default color data.\n    sprite_name: {name}\n    color_data_type: {type(color_data)}")
            color_data = []
            for px in range(len(sprite_data)):
                color_data.append(" ")
        elif type(color_data) != str and color_mode == "single":
            log("warning", f"empty color data detected; initializing default color data.\n    sprite_name: {name}\n    color_data_type: {type(color_data)}")
            color_data = " "

        # data size validator
        if  (len(sprite_data) != self.width * self.height) and self.sprite_mode == "single":
            self._valid_data = False
            log("error", f"invalid sprite data: single-frame size mismatch.\n    sprite_name: {self.name}\n    expected_pixels: {width*height}\n    provided_pixels: {len(sprite_data)}\n    provided_color_entries: {len(color_data)}")
        elif (len(sprite_data) != self.width * self.height * sprite_cuantity) and self.sprite_mode == "multi":
            self._valid_data = False
            log("error", f"invalid sprite data: multi-frame size mismatch.\n    sprite_name: {self.name}\n    expected_pixels: {width*height*self._sprite_cuantity}\n    provided_pixels: {len(sprite_data)}\n    provided_color_entries: {len(color_data)}")
        elif len(sprite_data) != len(color_data) and color_mode == "pixel":
            self._valid_data = False
            log("error", f"invalid sprite data: color and pixel arrays differ in length.\n    sprite_name: {self.name}\n    expected_pixels: {width*height}\n    sprite_data_size: {len(sprite_data)}\n    color_data_size: {len(color_data)}")
        
        # data content validator
        if self._color_mode == "pixel":
            for idx in range(len(color_data)):
                if preset_color_codes.get(color_data[idx], "") == "":
                    log("error", f"invalid color code: entry not in preset palette.\n    sprite_name: {self.name}\n    color_mode: {self._color_mode}\n    invalid_entry: {color_data[idx]}\n    invalid_index: {idx}")
                    break
        elif self._color_mode == "single":
            if preset_color_codes.get(color_data, "") == "":
                log("error", f"invalid color code: preset lookup failed.\n    sprite_name: {self.name}\n    color_mode: {self._color_mode}\n    color_data: {color_data}")
        
        self.readable_data = (sprite_data, color_data)

    def load_raw(self, frame = 0):
        """
        Loads the raw pixel and color data for the specified frame.\n
        Returns a tuple containing two lists: pixel_raw_data and color_raw_data.
        Arguments:
            frame:  The frame number to load (for multi-frame sprites).
        """
        if self._valid_data == False:
            return
        pixel_data = self.readable_data[0]                                                 
        color_data = self.readable_data[1]                                                 
        pixel_raw_data = []
        color_raw_data = []
        offset = self.height * self.width * frame                                                    
        for row in range(self.height):                                                                                                                                        
            for pixel in range(self.width):
                index = (row * self.width) + pixel + offset
                if self._color_mode == "pixel":
                    if pixel_data[index] != "nop":
                        if color_data[index] == " ":
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append("")
                        else:
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append(str(preset_color_codes.get(color_data[index], "")))
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
                elif self._color_mode == "single":
                    if pixel_data[index] != "nop":
                        pixel_raw_data.append(pixel_data[index])
                        color_raw_data.append(preset_color_codes.get(color_data, ""))
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
                elif self._color_mode == "single_custom":
                    if pixel_data[index] != "nop":
                        pixel_raw_data.append(pixel_data[index])
                        color_raw_data.append(color_data)
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
                elif self._color_mode == "pixel_custom":
                    if pixel_data[index] != "nop":
                        if color_data[index] == " ":
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append("")
                        else:
                            pixel_raw_data.append(str(pixel_data[index]))
                            color_raw_data.append(color_data[index])
                    else:
                        pixel_raw_data.append("nop")
                        color_raw_data.append("")
        #log("info", f"sprite_raw_data dump\n    sprite_name: {self.name}\n    pixel_raw_data: {pixel_raw_data}\n    color_raw_data: {color_raw_data}\n ")
        return (pixel_raw_data, color_raw_data)   
    
class MemoryBank:
    """
    NOT FINISHED NOR TESTED
    1D, 2D and 3D memory bank class for data storage and retrieval.
    Arguments:
        type:           The type of memory bank ("1d", "2d", "3d").
        read_only:      If true, the memory bank is read-only.
        dimentions:     A string representing the dimensions of the memory bank (e.g., "10", "10x10", "10x10x10").
        default_value:  The default value to initialize the memory bank with.
    """
    def __init__(self, type: Literal["1d", "2d", "3d"] = "1d", read_only: bool = False, dimentions: str = "10", default_value: Literal[0, ""] = 0):
        """
        DO NOT USE THIS YOU ABSOLUTE MORON, IT AUTOMATICALLY INITIALIZES WHEN CREATING A MemoryBank OBJECT.
        """
        self._type = type
        self._writable = not read_only
        self._default = default_value
        self._memory = []
        dimentions_str = dimentions.split(sep = "x")
        dimentions_int = []
        for val in dimentions_str:
            dimentions_int.append(int(val))
        self._x = 0
        self._y = 0
        self._z = 0
        self._valid_dimentions = True
        if len(dimentions_int) >= 1 and dimentions_int[0] != 0:
            self._x = dimentions_int[0]
        elif len(dimentions_int) >= 1 and dimentions_int[0] == 0:
            log("error", f"invalid memory size: x dimension cannot be 0.\n    dimensions: {dimentions}\n    memory_type: {self._type}")
            self._valid_dimentions = False
        if len(dimentions_int) >= 2:
            self._y = dimentions_int[1]
        if len(dimentions_int) >= 3:
            self._z = dimentions_int[2]

    def initialize(self):
        """
        The memory bank initializer. Ensures that the memory bank is usable.        
        """
        if self._valid_dimentions == False:
            log("error", f"memory initialization failed: invalid dimensions declared.\n    memory: {str(self)}")
            return
        if self._type == "1d":
            for column in range(self._x):
                self._memory.append(self._default)
        elif self._type == "2d":
            for row in range(self._y):
                self._memory.append([])
                for column in range(self._x):
                    self._memory[row].append(self._default)
        elif self._type == "3d":
            for row in range(self._y):
                self._memory.append([])
                for column in range(self._x):
                    self._memory[row].append([])
                    for layer in range(self._z):
                        self._memory[row][column].append(self._default)
        
    def get(self, memory_pointer: tuple = (0,)):
        """
        Retrieves data from the memory bank at the specified memory pointer.
        Arguments:
            memory_pointer:    A tuple representing the memory address to retrieve data from.
        """
        if type(memory_pointer) != tuple:
            log("error", f"could not retrieve data: invalid memory pointer type.\n    pointer_type: {type(memory_pointer)}")
            return 0
        try:
            if len(memory_pointer) == 1:
                return self._memory[memory_pointer[0]]
            if len(memory_pointer) == 2:
                return self._memory[memory_pointer[0]][memory_pointer[1]]
            if len(memory_pointer) == 3:
                return self._memory[memory_pointer[0]][memory_pointer[1]][memory_pointer[2]]
        except IndexError:
            log("error", f"could not retrieve data: pointer out of bounds.\n    pointer: {memory_pointer}")
            return 0
    
    def write(self, memory_pointer: tuple = (0,), data: any = ""):
        """
        Writes data to the memory bank at the specified memory pointer.
        Arguments:
            memory_pointer:    A tuple representing the memory address to write data to.
            data:              The data to write to the specified memory address.
        """
        if type(memory_pointer) != tuple:
            log("error", f"could not write data: invalid memory pointer type.\n    pointer_type: {type(memory_pointer)}")
            return
        try:
            if len(memory_pointer) == 1:
                self._memory[memory_pointer[0]] = data
            if len(memory_pointer) == 2:
                self._memory[memory_pointer[0]][memory_pointer[1]] = data
            if len(memory_pointer) == 3:
                self._memory[memory_pointer[0]][memory_pointer[1]][memory_pointer[2]] = data
        except IndexError:
            log("error", f"could not write data: pointer out of bounds.\n    pointer: {memory_pointer}")
            return
        
    def write_bank(self, start_pointer: tuple = (0, 0, 0), information_bank: list = [[[""]]], bank_dimentions: tuple = (1, 1, 1)):
        """
        Writes a block of data to the memory bank at the specified starting pointer.
        Arguments:
            start_pointer:     A tuple representing the starting memory address to write data to.
            information_bank:  A list containing the data block to write.
            bank_dimentions:   A tuple representing the dimensions of the data block.
        """
        x, y, z = bank_dimentions
        sx, sy, sz = start_pointer
        if len(bank_dimentions) == 1:
            for row in range(y):
                self._memory[row + sy] = information_bank[row]
        elif len(bank_dimentions) == 2:
            for row in range(y):
                for column in range(x):
                    self._memory[row + sy][column + sx] = information_bank[row][column]
        elif len(bank_dimentions) == 3:
            for row in range(y):
                for column in range(x):
                    for layer in range(z):
                        self._memory[row + sy][column + sx][layer + sz] = information_bank[row][column][layer]

class Screen:
    """
    Class that manages everything related to graphic rendering
    Arguments:
        height:     The height of the screen in characters.
        width:      The width of the screen in characters.
    """
    def __init__(self, height: int, width: int):
        """
        DO NOT USE THIS YOU ABSOLUTE MORON, IT AUTOMATICALLY INITIALIZES WHEN CREATING A Screen OBJECT.
        """
        self.height = height
        self.width = width
        self._screen = []
        self.pixel_layers = []
        self.color_layers = []
        self.pixel_blank = []
        self.color_blank = []

    def create_text(self, x: int, y: int, layer: int, text_data: Tuple[str, str, str]):
        """
        Creates a text element on the screen.
        Arguments:
            x:          The x position to start drawing the text.
            y:          The y position to start drawing the text.
            layer:      The layer to draw the text on.
            text_data:  A tuple containing the text string, foreground color code, and background color code.
        """
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
                if (0 <= x < self.width) and (0 <= y < self.height) and bg != "":
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{bg}{fg}"
                elif (0 <= x < self.width) and (0 <= y < self.height) and bg == "":
                    self.pixel_layers[y][x][layer] = f"{pixel}"
                    self.color_layers[y][x][layer] = f"{fg}"
                else:
                    continue
            x += 1

    def create_sprite(self, x: int, y: int, layer: int, sprite_data_raw: tuple, sprite_num: int = 0, Sprite: Sprite = None):
        """
        Creates a sprite element on the screen.
        Arguments:
            x:                  The x position to start drawing the sprite.
            y:                  The y position to start drawing the sprite.
            layer:              The layer to draw the sprite on.
            sprite_data_raw:    A tuple containing the raw pixel and color data of the sprite.
            sprite_num:         The frame number of the sprite to draw (for multi-frame sprites).
            Sprite:             The Sprite object containing the sprite's properties.
        """
        sprite_data = sprite_data_raw
        offset = (Sprite.height * Sprite.width) * sprite_num
        if sprite_data == None or Sprite == None:
            return
        pixel_write_data, color_write_data = sprite_data
        for row in range(Sprite.height):
            for column in range(Sprite.width):
                if (layer != 0) and ((0 <= x + column < self.width) and (0 <= y + row < self.height)):
                    if pixel_write_data[offset + (row * Sprite.width) + column] != "nop":
                        self.pixel_layers[y + row][x + column][layer] = pixel_write_data[offset + (row * Sprite.width) + column]
                        self.color_layers[y + row][x + column][layer] = color_write_data[offset + (row * Sprite.width) + column]
                    elif self.pixel_layers[y + row][x + column][layer] == "nop":
                        self.pixel_layers[y + row][x + column][layer] = "nop"
                        self.color_layers[y + row][x + column][layer] = "nop"

    def create_pixel(self, x: int, y: int, layer: int, pixel_data: Tuple[str, str, str]):
        """
        Creates a pixel element on the screen.
        Arguments:
            x:          The x position to draw the pixel.
            y:          The y position to draw the pixel.
            layer:      The layer to draw the pixel on.
            pixel_data: A tuple containing the pixel string, foreground color code, and background color code.
        """
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
    
    def set_bg(self, initx: int, inity: int, finx: int, finy: int, color: str):
        """
        Sets the background color for a specified area of the screen.
        Arguments:
            initx:  The initial x position of the area.
            inity:  The initial y position of the area.
            finx:   The final x position of the area.
            finy:   The final y position of the area.
            color:  The background color code to set.
        """
        sizex = finx - initx
        sizey = finy - inity
        for row in range(sizey):
            for column in range(sizex):
                if not(column + initx < 0 or column + initx >= self.width or row + inity < 0 or row + inity >= self.height):
                    self.color_layers[row + inity][column + initx][0] = f"{color}"

    def initialize(self, layers: int, bg_color: str):
        """
        Initializes the screen with the specified number of layers and background color.
        Arguments:
            layers:    The number of layers to create.
            bg_color:  The background color code to use.
        """
        log("system", f"initializing Screen (w={self.width} h={self.height}, layers={layers})")
        self._layers = layers
        self._bg_color = bg_color
        worklist = []
        for height_line in range(self.height):
            worklist.append([])
            for width_line in range(self.width):
                worklist[height_line].append([])
                for layer in range(self._layers):
                    worklist[height_line][width_line].append("nop")
        self.pixel_blank = worklist 
        worklist = []
        for height_line in range(self.height):
            worklist.append([])
            for width_line in range(self.width):
                worklist[height_line].append([])
                for layer in range(self._layers):
                    if layer == 0:
                        worklist[height_line][width_line].append(self._bg_color)
                    else:
                        worklist[height_line][width_line].append("")
        self.color_blank = worklist 

    def memory_reset(self):
        """
        Resets the screen memory to the blank state.
        """
        self.pixel_layers = deepcopy(self.pixel_blank)
        self.color_layers = deepcopy(self.color_blank)

    def bake_screen(self):
        """
        Bakes the current screen state into a final renderable format.
        """
        final_bake = []
        for height_line in range(self.height):
            final_bake.append([])
            pixel_bake = []
            color_bake = []
            layered_pixel = ""
            layered_color = ""
            for width_line in range(self.width):
                bg = False
                pixel = "   "
                fgcolor = "nop"
                bgcolor = self.color_layers[height_line][width_line][0]
                layered_pixel = self.pixel_layers[height_line][width_line]
                layered_color = self.color_layers[height_line][width_line]
                reversed_pixel_layers = reversed(layered_pixel)
                reversed_color_layers = reversed(layered_color)
                for pixel_layer, color_layer in zip(reversed_pixel_layers, reversed_color_layers):
                    if not bg:
                        if pixel_layer != "nop":
                            pixel = pixel_layer
                            fgcolor = color_layer
                            bg = True
                        else:
                            pixel = "   "
                            fgcolor = ""
                    else:
                        if pixel_layer != "nop":
                            bgcolor = color_layer
                            break
                        else:
                            bgcolor = ""
                pixel_bake.append(pixel)
                color_bake.append(bgcolor + fgcolor)
            #log("debug", f"color bake: {color_bake}\n pixel bake: {pixel_bake}")
            for item in range(len(pixel_bake)):
                final_bake[height_line].append(color_bake[item] + pixel_bake[item] + "\033[0m")
        self._screen = final_bake
    
    def print_screen(self):
        """
        Prints the baked screen to the terminal.
        """
        screen_print = ""
        for height_line in self._screen:
            for width_line in height_line:
                screen_print += width_line
            screen_print += "\n\033[0m"
        sys.stdout.write("\033[2J\033[H\n" + screen_print)
        sys.stdout.flush()

class CTkScreen:
    """
    Class that manages a CustomTkinter window for graphical rendering.
    Arguments:
        width:          The width of the window in characters.
        height:         The height of the window in characters.
        pixel_size:    The size of each pixel in the window.
        core_screen:    The Screen object to render in the window.
    """
    def __init__(self, width: int = 10, height: int = 10, pixel_size: int = 20, core_screen: Screen = None):
        """
        DO NOT USE THIS YOU ABSOLUTE MORON, IT AUTOMATICALLY INITIALIZES WHEN CREATING A CTkScreen OBJECT.
        """
        self.width = width
        self.height = height
        self.font_size = pixel_size
        self.pixels = []
        self.thread = None
        self.running = False
        self.font = ctk.CTkFont(family = "Consolas", size = self.font_size)
        if core_screen != None:
            self.core_screen = core_screen
        else:
            raise Exception("CTkScreen error! - core_screen cannot be None")

    def _initialize_window(self, game_title: str = "PYRcade Engine Window"):
        """
        NOT FOR PUBLIC USE\n
        Initializes the CustomTkinter window and its pixel grid.
        """
        self.root = ctk.CTk(game_title)
        self.root.title(game_title)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.pixel_space = ctk.CTkFrame(self.root, fg_color = "#000000")
        for i in range(self.width):
            self.pixel_space.grid_columnconfigure(i, weight = 1)
        for i in range(self.height):    
            self.pixel_space.grid_rowconfigure(i, weight = 1)
        for row in range(self.height):
            self.pixels.append([])
            for column in range(self.width):
                pixel = ctk.CTkLabel(self.pixel_space, bg_color = "#000000", font = self.font, text = "   ")
                pixel.grid(row = row, column = column, padx = 0, pady = 0, sticky = "nsew")
                self.pixels[row].append(pixel)
        self.pixel_space.pack(padx = 0, pady = 0)
    
    def _start_window(self, game_title: str = "PYRcade Engine Window"):
        """
        NOT FOR PUBLIC USE\n
        Starts the CustomTkinter window in a separate thread.
        """
        self.running = True
        try:
            self._initialize_window(game_title)
            self.running = True
            self.root.mainloop()
            log("system", "CTk window closed.")
        except Exception as e:
            log("error", f"Error initializing window: {e}")
            self.running = False
            self._close()
            return
        finally:
            self.running = False
            log("system", "CTk window closed.")

    def _close(self):
        """
        NOT FOR PUBLIC USE\n
        Closes the CustomTkinter window and stops the thread.
        """
        if self.running:
            self.running = False
            self.root.destroy()
            log("system", "CTk thread stopped.")

    def start(self):
        """
        Starts the CTk window thread.
        """
        if self.thread is None:
            log("system", "starting CTk window thread...")
            self.thread = threading.Thread(target = self._start_window, daemon = True)
            self.thread.start()
            log("system", "CTk window thread started.")
        else:
            log("warning", "CTk window thread already running!")
    
    def update(self):
        """
        Updates the CTk window with the current screen data.
        """
        bg = False
        if self.running:
            for row in range(self.height):
                for column in range(self.width):
                    layered_pixel = self.core_screen.pixel_layers[row][column]
                    layered_color = self.core_screen.color_layers[row][column]
                    reversed_pixel_layers = reversed(layered_pixel)
                    reversed_color_layers = reversed(layered_color)
                    pixel_data = "   "
                    pixel_color = "#ffffff"
                    pixel_bg = "#000000"
                    bg = False
                    for pixel_layer, color_layer in zip(reversed_pixel_layers, reversed_color_layers):
                        if pixel_layer != "nop" and not bg:
                            pixel_data = pixel_layer
                            if color_layer != "":
                                pixel_color = ANSII_to_HEX(color_layer)
                            bg = True
                        elif pixel_layer != "nop" and bg:
                            if color_layer != "":
                                pixel_bg = ANSII_to_HEX(color_layer)
                            break
                    self.pixels[row][column].configure(text = pixel_data, fg_color = pixel_bg, text_color = pixel_color)

default_keymap = {"up"          : pynput.keyboard.Key.up, 
                  "down"        : pynput.keyboard.Key.down,
                  "left"        : pynput.keyboard.Key.left,
                  "right"       : pynput.keyboard.Key.right,
                  "space"       : pynput.keyboard.Key.space,
                  "esc"         : pynput.keyboard.Key.esc,
                  "enter"       : pynput.keyboard.Key.enter,
                  "backspace"   : pynput.keyboard.Key.backspace}

class Arcade:
    """
    Class that represents an arcade machine.
    Arguments:
        arcade_name:    The name of the arcade machine.
        Screen:         The Screen object to use for rendering.
        type:           The type of arcade machine ("python_game" or "pyrcade_script_game").
        mode:           The mode of the arcade machine ("Terminal" or "Windowed").
        key_map:       A dictionary mapping input keys to pynput keyboard keys.
    """
    def __init__(self, arcade_name: str, Screen: Screen, type: Literal["python_game", "pyrcade_script_game"], mode: Literal["Terminal", "Windowed"] = "Terminal", key_map: dict = default_keymap):
        """
        DO NOT USE THIS YOU ABSOLUTE MORON, IT AUTOMATICALLY INITIALIZES WHEN CREATING AN Arcade OBJECT.
        """
        self.arcade_name = arcade_name
        self._screen = Screen
        self._type = type
        self._mode = mode
        self.input = ""
        self._key_map = key_map
        self._engine_ver = "1.0.1"

    def start_machine(self, game_code = None):
        """
        Starts the arcade machine with the provided game code function.
        Arguments:
            game_code: The game code function to run. MUST BE A FUNCTION THAT TAKES NO ARGUMENTS.
        """
        log("Arcade", f"starting Arcade machine {self.arcade_name}...\n    Arcade info:\n    name: {self.arcade_name}\n    type: {self._type}")
        if self._mode == "Terminal":
            if self._type == "python_game":
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.flush()
                game_code()
        elif self._mode == "Windowed":
            pass
    
    def start_input(self, keys: list = ["up", "down", "left", "right", "space", "esc"]):
        """
        MUST RUN BEFORE STARTING THE ARCADE MACHINE!\n
        Starts the input listener for the arcade machine.
        Arguments:
            keys: A list of keys to listen for.
        """
        log("Arcade", f"Arcade {self.arcade_name} started input listener")
        self._actual_inputs = set()
        self._keys = keys
        self._input_events_buffer = []
        def input_listener_press(keypressed):
            for key in self._keys:
                if self._key_map[key] == keypressed:
                    self._actual_inputs.add(key)
        def input_listener_release(keyrelease):
            for key in self._keys:
                if self._key_map[key] == keyrelease:
                    self._actual_inputs.discard(key)
        listener = pynput.keyboard.Listener(on_press = input_listener_press, on_release = input_listener_release)
        listener.start()