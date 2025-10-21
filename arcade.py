from pyrcade_engine import *

# tetris example in python (full potential)
tetris_screen = Screen(20, 20)
tetris = Arcade("pyrcade_tetris", tetris_screen, "secondary")
def tetris_loop():
    #tetris pieces sprites
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

    sprites_data = ["nop", "nop", "███",
                    "███", "███", "███", 
                    "nop", "nop", "nop",
                    
                    "nop", "███", "nop",
                    "nop", "███", "nop", 
                    "nop", "███", "███",
                    
                    "nop", "nop", "nop",
                    "███", "███", "███", 
                    "███", "nop", "nop",
                    
                    "███", "███", "nop",
                    "nop", "███", "nop", 
                    "nop", "███", "nop",]
    colors_data = color.fg(20)
    tetromino3 = Sprite("tetromino2", 3, 3, sprites_data, "single_custom", colors_data, "multi", 4)

    sprites_data = ["nop", "███", "nop",
                    "███", "███", "███", 
                    "nop", "nop", "nop",
                    
                    "nop", "███", "nop",
                    "nop", "███", "███", 
                    "nop", "███", "nop",
                    
                    "nop", "nop", "nop",
                    "███", "███", "███", 
                    "nop", "███", "nop",
                    
                    "nop", "███", "nop",
                    "███", "███", "nop", 
                    "nop", "███", "nop",]
    colors_data = color.fg(162)
    tetromino4 = Sprite("tetromino2", 3, 3, sprites_data, "single_custom", colors_data, "multi", 4)

    sprites_data = ["nop", "███", "███", 
                    "███", "███", "nop",
                    "nop", "nop", "nop",
                    
                    "nop", "███", "nop",  
                    "nop", "███", "███",  
                    "nop", "nop", "███", 
                    
                    "nop", "nop", "nop",
                    "nop", "███", "███", 
                    "███", "███", "nop",

                    "███", "nop", "nop", 
                    "███", "███", "nop",  
                    "nop", "███", "nop",]
    colors_data = color.fg(196)
    tetromino5 = Sprite("tetromino2", 3, 3, sprites_data, "single_custom", colors_data, "multi", 4)

    sprites_data = ["███", "███", "nop", 
                    "nop", "███", "███",
                    "nop", "nop", "nop",
                    
                    "nop", "nop", "███",  
                    "nop", "███", "███",  
                    "nop", "███", "nop", 
                    
                    "nop", "nop", "nop",
                    "███", "███", "nop", 
                    "nop", "███", "███",

                    "nop", "███", "nop", 
                    "███", "███", "nop",  
                    "███", "nop", "nop",]
    colors_data = color.fg(40)
    tetromino6 = Sprite("tetromino2", 3, 3, sprites_data, "single_custom", colors_data, "multi", 4)

    sprites_data = ["nop", "nop", "nop", "nop",
                    "███", "███", "███", "███",
                    "nop", "nop", "nop", "nop",
                    "nop", "nop", "nop", "nop",
                    
                    "nop", "nop", "███", "nop",
                    "nop", "nop", "███", "nop", 
                    "nop", "nop", "███", "nop",
                    "nop", "nop", "███", "nop",
                    
                    "nop", "nop", "nop", "nop",
                    "nop", "nop", "nop", "nop",
                    "███", "███", "███", "███",
                    "nop", "nop", "nop", "nop",
                    
                    "nop", "███", "nop", "nop", 
                    "nop", "███", "nop", "nop", 
                    "nop", "███", "nop", "nop", 
                    "nop", "███", "nop", "nop", ]
    colors_data = color.fg(33)
    tetromino7 = Sprite("tetromino2", 4, 4, sprites_data, "single_custom", colors_data, "multi", 4)
    # tetris variables
    piece = False
    pieces = [tetromino1, tetromino2, tetromino3, tetromino4, tetromino5, tetromino6, tetromino7]
    tetris_screen.initialize(5, color.bg(236))
    piece = False
    layer_1_pixel = []
    layer_1_color = []
    draw_layer = 2
    rotation = 0
    new_rot = 0
    tetris_debug = False
    fall = True
    fallen = False
    full_fall = False
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
                        else:
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
        tetris_screen.set_bg(5, 0, 15, 20, color.bg(0))

        if layer_1_pixel != []:
            for row in range(len(layer_1_pixel)):
                for column in range(len(layer_1_pixel[row])):
                    tetris_screen.pixel_layers[row][column][1] = layer_1_pixel[row][column]
                    tetris_screen.color_layers[row][column][1] = layer_1_color[row][column]

        if fall:
            fall = False
        elif not fall:
            fall = True

        if "left" in tetris._actual_inputs:
            if not check_piece_collitions(random_piece, x, y, rotation, "L", -1):
                x -= 1
        if "right" in tetris._actual_inputs:
            if not check_piece_collitions(random_piece, x, y, rotation, "R", 1):
                x += 1
        if "down" in tetris._actual_inputs:
            fall = True
        if "space" in tetris._actual_inputs:
            new_rot = (rotation + 1) % random_piece._sprite_cuantity
            if not check_piece_collitions(random_piece, x, y, new_rot, "Rot", 1):
                rotation = new_rot
            tetris._actual_inputs.discard("space")

        if piece == False:
            rotation = 0
            draw_layer = 2
            piece = True
            fallen = False
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
                    if fallen:
                        piece = False
                    elif collision:
                        fallen = True
                        fall = False
                if collision == False:
                    if fall and not full_fall:
                        y += 1
            tetris_screen.create_sprite(x, y, draw_layer, random_piece.load_raw(rotation), 0, random_piece)
        elif piece == True and y <= 0:
            if fall and not full_fall:
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
        time.sleep(0.1)

        #log("info", f"layer 1 dump:\n{layer_1_pixel}")

tetris.start_input()
tetris.start_machine(tetris_loop)