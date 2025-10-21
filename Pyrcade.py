import time, sys, pynput, random, datetime
from typing import Literal, Tuple
from copy import deepcopy

DEBUG = True
initial_datetime = ""
def log(type: Literal["initial", "system", "warning", "info", "error", "Arcade"], message = None):
    if DEBUG == True:
        global initial_datetime
        date_and_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        if type == "initial":
            with open(f"logs/{date_and_time} - pyrcade_log.txt", "w", encoding="utf-8") as log_file:
                log_file.write(f"{date_and_time} - pyrcade engine starting...\n\n")
                log_file.write(f"{date_and_time} - starting logging system...\n\n")
                initial_datetime = date_and_time
        else:
            with open(f"logs/{initial_datetime} - pyrcade_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{date_and_time} - {type} - {message}\n\n")

log("initial")

class ColorManager: 
    def __init__(self):
        pass
    
    def fg(self, code):
        return f"\u001b[38;5;{code}m"
    
    def bg(self, code):
        return f"\u001b[48;5;{code}m"

log("system", "loading color manager...")

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

class Sprite:
    def __init__(self, name: str, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel", "single_custom"] = "single", color_data: list[str] = None, sprite_mode: Literal["single", "multi"] = "single", sprite_cuantity: int = 1, extra_val_1 = None, extra_val_2 = None, extra_val_3 = None):
        '''
        :param sprite_data: Is a list with "pixel" data of the Sprite. Every pixel MUST be 3 characters long
        :type sprite_data:  list[str, str, str, ...]
        :param color_mode:  The color mode of the Sprite. "single": all the Sprite is the same color, "pixel": every pixel has it's own color
        :type color_mode:   str - "single", "pixel"
        :param color_data:  Is a list with "color" data of the Sprite. Every entry MUST be 1 characters long, the character MUST be part of the color_codes dictionary
        :type color_data:   list[str, str, str, ...]
        :param sprite_mode: A flag that enables or disables the multi frame support for Sprite animation or variation.
        :type sprite_mode:  str - "single", "multi"
        :param sprite_cuantity: This tells the engine how many frames / different sprites the Sprite data holds. MUST be 1 if the sprite_mode id "single"
        :type sprite_cuantity: int
        '''
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
            log("warning", f"empty color data! - color data will be initialized.\n    extra data:\n    sprite_name:{name}\n    color_data_type:{type(color_data)}")
            color_data = []
            for px in range(len(sprite_data)):
                color_data.append(" ")
        elif type(color_data) != str and color_mode == "single":
            log("warning", f"empty color data! - color data will be initialized.\n    extra data:\n    sprite_name:{name}\n    color_data_type:{type(color_data)}")
            color_data = " "

        # data size validator
        if  (len(sprite_data) != self.width * self.height) and self.sprite_mode == "single":
            self._valid_data = False
            log("error", f"invalid Sprite data! - single frame Sprite incorrect data size.\n    Sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif (len(sprite_data) != self.width * self.height * sprite_cuantity) and self.sprite_mode == "multi":
            self._valid_data = False
            log("error", f"invalid Sprite data! - multi frame Sprite incorrect data size.\n    Sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height*self._sprite_cuantity}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif len(sprite_data) != len(color_data) and color_mode == "pixel":
            self._valid_data = False
            log("error", f"invalid Sprite data! - inconsistent color-pixel data size.\n    Sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        
        # data content validator
        if self._color_mode == "pixel":
            for idx in range(len(color_data)):
                if preset_color_codes.get(color_data[idx], "") == "":
                    log("error", f"invalid color code! - color code not found.\n    extra data:\n    sprite_name:{self.name}\n    color_mode: {self._color_mode}\n    invalid_entry:{color_data[idx]}\n    invalid_index:{idx}")
                    break
        elif self._color_mode == "single":
            if preset_color_codes.get(color_data, "") == "":
                log("error", f"invalid color code! - color code not found.\n    extra data:\n    sprite_name:{self.name}\n    color_mode: {self._color_mode}\n    color_data:{color_data}")
        
        self.readable_data = (sprite_data, color_data)

    def load_raw(self, frame = 0):
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
        #log("info", f"sprite_raw_data dump\n    sprite_name: {self.name}\n    pixel_raw_data: {pixel_raw_data}\n    color_raw_data: {color_raw_data}\n ")
        return (pixel_raw_data, color_raw_data)   
    
class MemoryBank:
    def __init__(self, type: Literal["1d", "2d", "3d"] = "1d", read_only: bool = False, dimentions: str = "10", default_value: Literal[0, ""] = 0):
        '''
        :param dimentions:  Is the size of the memory bank on a string. The format is an XYZ type and is separated by an "x". X, Y and Z MUST be integers. The format would look like: "XxYxZ".
        :type dimentions: str - 3 int in a str separated by an "x"
        :param default_value:   The default state of the memory when initialized. Can be either 0 or ""
        :param type:    The dimention depth / complexity of the memory bank. 1d = [a, b], 2d = [[a1, b1], [a2, b2]], 3d = [[[a11, b11], [a12, b12]], [[a21, b21], [a22, b22]]]
        :type type: str
        :param read_only:  A flag that tells if the memory is a read_only memory or a read-write memory. Pretty self explainatory
        '''
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
            log("error", f'invalid memory size! - memory "x" dimention cannot be 0\n    extra data:\n    memory_dimentions: {dimentions}\n    memory_type: {self._type}')
            self._valid_dimentions = False
        if len(dimentions_int) >= 2:
            self._y = dimentions_int[1]
        if len(dimentions_int) >= 3:
            self._z = dimentions_int[2]

    def initialize(self):
        if self._valid_dimentions == False:
            log("error", f'memory initialization failed! - invalid memory_size declared\n    extra data:\n    memory_dimentions: {str(self)}')
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
        '''
        :param memory_pointer: Cordinates of the data to retrieve. MUST be a tuple. If a one item tuple then (x,)
        '''
        if type(memory_pointer) != tuple:
            log("error", f"could not retrive data! - invalid pointer\n    extra data:\n    pointer_type: {type(memory_pointer)}")
            return 0
        try:
            if len(memory_pointer) == 1:
                return self._memory[memory_pointer[0]]
            if len(memory_pointer) == 2:
                return self._memory[memory_pointer[0]][memory_pointer[1]]
            if len(memory_pointer) == 3:
                return self._memory[memory_pointer[0]][memory_pointer[1]][memory_pointer[2]]
        except IndexError:
            log("error", f"could not retrive data! - out of bounds memory pointer\n    extra data:\n    pointer: {memory_pointer}")
            return 0
    
    def set(self, memory_pointer: tuple = (0,), data: any = ""):
        '''
        :param memory_pointer: Cordinates of the data to write. MUST be a tuple. If a one item tuple then (x,)
        '''
        if type(memory_pointer) != tuple:
            log("error", f"could not write data! - invalid pointer\n    extra data:\n    pointer_type: {type(memory_pointer)}")
            return
        try:
            if len(memory_pointer) == 1:
                self._memory[memory_pointer[0]] = data
            if len(memory_pointer) == 2:
                self._memory[memory_pointer[0]][memory_pointer[1]] = data
            if len(memory_pointer) == 3:
                self._memory[memory_pointer[0]][memory_pointer[1]][memory_pointer[2]] = data
        except IndexError:
            log("error", f"could not write data! - out of bounds memory pointer\n    extra data:\n    pointer: {memory_pointer}")
            return
        
    def write_bank(self, start_pointer: tuple = (0, 0, 0), information_bank: list = [[[""]]], bank_dimentions: tuple = (1, 1, 1)):
        '''
        :param start_pointer: Cordinates of the data to write. MUST be a tuple. If a one item tuple then (x,)
        :param bank_dimentions: Size of the data bank. MUST be a tuple. The tuple should have the same cuantity of entries as dimentions on the memory bank, (1d = 1, 2d = 2, 3d = 3). Dimentions come in order: (X, Y, Z)
        '''
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
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self._screen = []
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

    def create_sprite(self, x: int, y: int, layer: int, sprite_data_raw: tuple, sprite_num: int = 0, Sprite: Sprite = None):
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
        '''
        :param pixel_data: A tuple of 3 entries. 1st entry: Pixel - 2nd Entry: Foreground Color - 3rd Entry: Background Color
        '''
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
        sizex = finx - initx
        sizey = finy - inity
        for row in range(sizey):
            for column in range(sizex):
                if not(column + initx < 0 or column + initx >= self.width or row + inity < 0 or row + inity >= self.height):
                    self.color_layers[row + inity][column + initx][0] = f"{color}"

    def initialize(self, layers: int, bg_color: str):
        log("system", "initializing Screen...")
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
            #log("info", f"color bake dump: {color_bake}\n pixel bake dump: {pixel_bake}")
            for item in range(len(pixel_bake)):
                final_bake[height_line].append(color_bake[item] + pixel_bake[item] + "\033[0m")
        self._screen = final_bake
    
    def print_screen(self):
        screen_print = ""
        for height_line in self._screen:
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

class Arcade:
    def __init__(self, arcade_name: str, Screen: Screen, type: Literal["main", "secondary"], key_map: dict = default_keymap):
        self.arcade_name = arcade_name
        self._screen = Screen
        self._type = type
        self.input = ""
        self._key_map = key_map

    def start_machine(self, mainloop_code: callable):
        log("Arcade", f"starting Arcade machine {self.arcade_name}...\n    Arcade info:\n    name: {self.arcade_name}\n    type: {self._type}")
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        mainloop_code()
    
    def start_input(self, keys: list = ["up", "down", "left", "right", "space", "esc"]):
        log("Arcade", f"Arcade {self.arcade_name} started input logger")
        self._actual_inputs = set()
        self._keys = keys
        self._input_events_buffer = []
        def input_logger_press(keypressed):
            for key in self._keys:
                if self._key_map[key] == keypressed:
                    self._actual_inputs.add(key)
        def input_logger_release(keyrelease):
            for key in self._keys:
                if self._key_map[key] == keyrelease:
                    self._actual_inputs.discard(key)
        listener = pynput.keyboard.Listener(on_press = input_logger_press, on_release = input_logger_release)
        listener.start()
                
# tetris
tetris_screen = Screen(20, 20)
tetris = Arcade("pyrcade_tetris", tetris_screen, "secondary")
def tetris_loop():
    #t etris pieces sprites
    sprites_data = ["███", "███", 
                    "███", "███"]
    colors_data = "y"
    tetromino1 = Sprite("tetromino1", 2, 2, sprites_data, "single", colors_data, "single", 1)
    
    sprites_data = ["███", "nop", "nop",
                    "███", "███", "███", 
                    "nop", "nop", "nop",
                    
                    "nop", "███", "███",
                    "nop", "███", "nop", 
                    "nop", "███", "nop",
                    
                    "nop", "nop", "nop",
                    "███", "███", "███", 
                    "nop", "nop", "███",
                    
                    "nop", "███", "nop",
                    "nop", "███", "nop", 
                    "███", "███", "nop",]
    
    colors_data = color.fg(202)
    tetromino2 = Sprite("tetromino2", 3, 3, sprites_data, "single_custom", colors_data, "multi", 4)
    # tetris variables
    piece = False
    pieces = [tetromino1, tetromino2]
    tetris_screen.initialize(5, color.bg(14))
    piece = False
    layer_1_pixel = []
    layer_1_color = []
    draw_layer = 2
    rotation = 0
    new_rot = 0
    tetris_debug = False
    # tetris funtions
    def check_piece_collitions(piece: Sprite, x, y, piece_rotation, direction: Literal["R", "L", "D", "Rot"], cuantity: int = 1):
        piece_data, piece_color = piece.load_raw(piece_rotation)
        for i in range(len(piece_data)):
            for row in range(piece.height):
                for column in  range(piece.width):
                    index = row * piece.width + column
                    if piece_data[index] == "███":
                        new_x = x + column
                        new_y = y + row
                        if direction == "L" or direction == "R":
                            new_x += cuantity
                        elif direction == "D":
                            new_y += cuantity
                        if new_x < 5:
                            return True
                        if new_x > 14:
                            return True
                        if new_y >= tetris_screen.height:
                            return True
                        if new_y >= 0:
                            try:
                                if layer_1_pixel[new_y][new_x] != "nop":
                                    return True
                            except IndexError:
                                continue
        return False
    # game loop
    while True:
        draw_layer = 2
        gravity = 1
        tetris_screen.memory_reset()
        tetris_screen.set_bg(5, 0, 15, 20, color.bg(6))

        if layer_1_pixel != []:
            for row in range(len(layer_1_pixel)):
                for column in range(len(layer_1_pixel[row])):
                    tetris_screen.pixel_layers[row][column][1] = layer_1_pixel[row][column]
                    tetris_screen.color_layers[row][column][1] = layer_1_color[row][column]

        if "left" in tetris._actual_inputs:
            if not check_piece_collitions(random_piece, x, y, rotation, "L", -1):
                x -= 1
        if "right" in tetris._actual_inputs:
            if not check_piece_collitions(random_piece, x, y, rotation, "R", 1):
                x += 1
        if "down" in tetris._actual_inputs:
            gravity = 3
        if "space" in tetris._actual_inputs:
            new_rot = (rotation + 1) % random_piece._sprite_cuantity
            if not check_piece_collitions(random_piece, x, y, new_rot, "Rot", 1):
                rotation = new_rot
            tetris._actual_inputs.discard("space")

        if piece == False:
            rotation = 0
            draw_layer = 2
            piece = True
            random_piece = random.choice(pieces)
            x = 9
            y = -2

        collision = False
        if piece == True and y > 0:
            for i in range(gravity):
                for px in range(random_piece.width):
                    if tetris_debug == True:
                        tetris_screen.create_pixel(x + px, y + random_piece.height + 1, 3, ("███", "", color.fg(9))) # debug draw for collisión
                    if check_piece_collitions(random_piece, x, y, rotation, "D", 1):
                        collision = True
                        draw_layer = 1
                        piece = False
                if collision == False:
                    y += 1
            tetris_screen.create_sprite(x, y, draw_layer, random_piece.load_raw(rotation), 0, random_piece)
        elif piece == True and y <= 0:
            y += 1
            tetris_screen.create_sprite(x, y, draw_layer, random_piece.load_raw(rotation), 0, random_piece)

        clear_lines = []
        for row_line in range(len(layer_1_pixel)): # single row building
            row_data = []
            for width in range(tetris_screen.width):
                if width > 4 and width < 15:
                    row_data.append(layer_1_pixel[row_line][width])
            if row_data == ["███"] * 10:
                clear_lines.append(row_line)

        layer_1_pixel = []
        layer_1_color = []
        for row in range(len(tetris_screen.pixel_layers)):
            layer_1_pixel.append([])
            layer_1_color.append([])
            for column in range(len(tetris_screen.pixel_layers[row])):
                layer_1_pixel[row].append(tetris_screen.pixel_layers[row][column][1])
                layer_1_color[row].append(tetris_screen.color_layers[row][column][1])

        clear_lines.sort(reverse = True)
        pixel_line_blank = tetris_screen.pixel_blank[0]
        color_line_blank = tetris_screen.color_blank[0]
        for index in clear_lines:
            layer_1_pixel.pop(index)
            layer_1_color.pop(index)
        for row in range(len(clear_lines)):
            layer_1_pixel.insert(0, [])
            layer_1_color.insert(0, [])
            for column in range(tetris_screen.width):
                layer_1_pixel[0].append(deepcopy(pixel_line_blank[column][0]))
                layer_1_color[0].append(deepcopy(color_line_blank[column][0]))
        
        if layer_1_pixel != []:
            for row in range(len(layer_1_pixel)):
                for column in range(len(layer_1_pixel[row])):
                    if layer_1_pixel[row][column] != "nop":
                        tetris_screen.pixel_layers[row][column][1] = layer_1_pixel[row][column]
                        tetris_screen.color_layers[row][column][1] = layer_1_color[row][column]

        tetris_screen.bake_screen()
        tetris_screen.print_screen()
        print(tetris._actual_inputs, x, y, piece, rotation)
        time.sleep(0.2)

        #log("info", f"layer 1 dump:\n{layer_1_pixel}")

tetris.start_input()
tetris.start_machine(tetris_loop)