import time, sys, pynput, random, datetime
from typing import Literal, Tuple, NewType
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

class color_manager: 
    def __init__(self):
        pass
    
    def fg(self, code):
        return f"\u001b[38;5;{code}m"
    
    def bg(self, code):
        return f"\u001b[48;5;{code}m"

log("system", "loading color manager...")
color = color_manager()

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

class sprite:
    def __init__(self, name: str, width: int, height: int, sprite_data: list[str], color_mode: Literal["single", "pixel"] = "single", color_data: list[str] = None, sprite_mode: Literal["single", "multi"] = "single", sprite_cuantity: int = 1):
        '''
        :param sprite_data: Is a list with "pixel" data of the sprite. Every pixel MUST be 3 characters long
        :type sprite_data:  list[str, str, str, ...]
        :param color_mode:  The color mode of the sprite. "single": all the sprite is the same color, "pixel": every pixel has it's own color
        :type color_mode:   str - "single", "pixel"
        :param color_data:  Is a list with "color" data of the sprite. Every entry MUST be 1 characters long, the character MUST be part of the color_codes dictionary
        :type color_data:   list[str, str, str, ...]
        :param sprite_mode: A flag that enables or disables the multi frame support for sprite animation or variation.
        :type sprite_mode:  str - "single", "multi"
        :param sprite_cuantity: This tells the engine how many frames / different sprites the sprite data holds. MUST be 1 if the sprite_mode id "single"
        :type sprite_cuantity: int
        '''
        self.width = width
        self.height = height
        self._color_mode = color_mode
        self._valid_data = True
        self.name = name
        self.sprite_mode = sprite_mode
        self._sprite_cuantity = sprite_cuantity

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
            log("error", f"invalid sprite data! - single frame sprite incorrect data size.\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif (len(sprite_data) != self.width * self.height * sprite_cuantity) and self.sprite_mode == "multi":
            self._valid_data = False
            log("error", f"invalid sprite data! - multi frame sprite incorrect data size.\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height*self._sprite_cuantity}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        elif len(sprite_data) != len(color_data) and color_mode == "pixel":
            self._valid_data = False
            log("error", f"invalid sprite data! - inconsistent color-pixel data size.\n    sprite info:\n    sprite_name:{self.name}\n    intended_data_size:{width*height}\n    sprite_data_size:{len(sprite_data)}\n    color_data_size:{len(color_data)}")
        
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
        #log("info", f"sprite_raw_data dump\n    sprite_name: {self.name}\n    pixel_raw_data: {pixel_raw_data}\n    color_raw_data: {color_raw_data}\n ")
        return (pixel_raw_data, color_raw_data)   

dimention_vector = NewType("dimention_vector", str)

class memory_bank:
    def __init__(self, type: Literal["1d", "2d", "3d"] = "1d", read_only: bool = False, dimentions: dimention_vector = "10", default_value: Literal[0, ""] = 0):
        '''
        :param dimentions:  Is the size of the memory bank on a string. The format is an XYZ type and is separated by an "x", X, Y and Z MUST be integers.The format would look like: "XxYxZ".
        :type dimentions: dimention_vector
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
            for row in range(self._x):
                self._memory.append(self._default)
        elif self._type == "2d":
            for row in range(self._x):
                self._memory.append([])
                for column in range(self._y):
                    self._memory[row].append(self._default)
        elif self._type == "3d":
            for row in range(self._x):
                self._memory.append([])
                for column in range(self._y):
                    self._memory[row].append([])
                    for layer in range(self._z):
                        self._memory[row][column].append(self._default)
        

class screen:
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

class arcade:
    def __init__(self, arcade_name: str, screen: screen, type: Literal["main", "secondary"], key_map: dict = default_keymap):
        self.arcade_name = arcade_name
        self._screen = screen
        self._type = type
        self.input = ""
        self._key_map = key_map

    def start_machine(self, mainloop_code: callable):
        log("arcade", f"starting arcade machine {self.arcade_name}...\n    arcade info:\n    name: {self.arcade_name}\n    type: {self._type}")
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        mainloop_code()
    
    def start_input(self, keys: list = ["up", "down", "left", "right", "space", "esc"]):
        log("arcade", f"arcade {self.arcade_name} started input logger")
        self.input = ""
        self.actual_input = None
        self._keys = keys
        def input_logger(keypressed):
            self.actual_input = keypressed
            for key in self._keys:
                if self._key_map[key] == keypressed:
                    self.input = key
            if self.actual_input == None:
                self.input = "none"
        listener = pynput.keyboard.Listener(on_press = input_logger)
        listener.start()
                
# tetris
tetris_screen = screen(20, 20)
tetris = arcade("pyrcade_tetris", tetris_screen, "secondary")
def tetris_loop():
    #t etris pieces sprites
    sprites_data = ["███", "███", 
                    "███", "███"]
    colors_data = "y"
    tetromino1_1 = sprite("tetromino1", 2, 2, sprites_data, "single", colors_data, "single", 1)
    sprites_data = ["nop", "nop", "nop",
                    "███", "nop", "nop", 
                    "███", "███", "███",
                    
                    "███", "███", "nop",
                    "███", "nop", "nop", 
                    "███", "nop", "nop",
                    
                    "nop", "nop", "nop",
                    "███", "███", "███", 
                    "nop", "nop", "███",
                    
                    "███", "███", "nop",
                    "nop", "███", "nop", 
                    "nop", "███", "nop",]
    colors_data = "r"
    # tetris variables
    piece = False
    pieces = [tetromino1_1]
    tetris_screen.initialize(5, color.bg(14))
    piece = False
    layer_1_pixel = []
    layer_1_color = []
    draw_layer = 2
    # debug on / off
    tetris_debug = False
    # game loop
    while True:
        draw_layer = 2
        gravity = 1
        tetris_screen.memory_reset()

        # layer 1 restore
        if layer_1_pixel != []:
            for row in range(len(layer_1_pixel)):
                for column in range(len(layer_1_pixel[row])):
                    if layer_1_pixel[row][column] != "nop":
                        tetris_screen.pixel_layers[row][column][1] = layer_1_pixel[row][column]
                        tetris_screen.color_layers[row][column][1] = layer_1_color[row][column]

        if tetris.input == "left":
            if (x > 5) and not (tetris._screen.pixel_layers[y][x - 1][1] == "███" or tetris._screen.pixel_layers[y + 1][x - 1][1] == "███"):
                x -= 1
        elif tetris.input == "right":
            if (x < 15 - random_piece.width) and not (tetris._screen.pixel_layers[y][x + random_piece.width][1] == "███" or tetris._screen.pixel_layers[y + 1][x + random_piece.width][1] == "███"):
                x += 1
        elif tetris.input == "down":
            gravity = 3

        if piece == False:
            draw_layer = 2
            piece = True
            random_piece = random.choice(pieces)
            x = 9
            y = 0

        collision = False
        if piece == True:
            for i in range(gravity):
                for px in range(random_piece.width):
                    if tetris_debug == True:
                        tetris_screen.create_pixel(x + px, y + random_piece.height + 1, 3, ("███", "", color.fg(9))) # debug draw for collisión
                    if ((y + random_piece.height) >= tetris_screen.height) or (tetris_screen.pixel_layers[y + random_piece.height][x + px][1] == "███") or (y > tetris_screen.height - random_piece.height):
                        collision = True
                        draw_layer = 1
                        piece = False
                if collision == False:
                    y += 1
            tetris_screen.create_sprite(x, y, draw_layer, random_piece.load_raw(), 0, random_piece)

        clear_lines = []
        for row_line in range(len(layer_1_pixel)): # single row building
            row_data = []
            for width in range(tetris_screen.width):
                if width > 4 and width < 15:
                    row_data.append(layer_1_pixel[row_line][width])
            if row_data == ["███"] * 10:
                clear_lines.append(row_line)

        clear_lines.sort(reverse = True)
        pixel_line_blank = tetris_screen.pixel_blank[0]
        color_line_blank = tetris_screen.color_blank[0]
        for index in clear_lines:
            tetris_screen.pixel_layers.pop(index)
            tetris_screen.color_layers.pop(index)
        for _ in range(len(clear_lines)):
            tetris_screen.pixel_layers.insert(0, deepcopy(pixel_line_blank))
            tetris_screen.color_layers.insert(0, deepcopy(color_line_blank))
        
        layer_1_pixel = []
        layer_1_color = []
        for row in range(len(tetris_screen.pixel_layers)):
            layer_1_pixel.append([])
            layer_1_color.append([])
            for column in range(len(tetris_screen.pixel_layers[row])):
                layer_1_pixel[row].append(tetris_screen.pixel_layers[row][column][1])
                layer_1_color[row].append(tetris_screen.color_layers[row][column][1])

        tetris_screen.bake_screen()
        tetris_screen.print_screen()
        print(tetris.actual_input)
        time.sleep(0.2)

        log("info", f"layer 1 dump:\n{layer_1_pixel}")

tetris.start_input()
tetris.start_machine(tetris_loop)