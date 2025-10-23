from pyrcade_engine import *

# tetris example in python (full potential)
tetris_screen = Screen(20, 20)
frame_counter = 0
tetris = Arcade("pyrcade_tetris", tetris_screen, "python_game", "Terminal")
def tetris_loop():
    global frame_counter
    #tetris pieces sprites
    sprites_data = ["███", "███", 
                    "███", "███"]
    colors_data = "Y"
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
    colors_data = color.fg(208)
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
    colors_data = "B"
    tetromino3 = Sprite("tetromino3", 3, 3, sprites_data, "single", colors_data, "multi", 4)

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
    colors_data = "P"
    tetromino4 = Sprite("tetromino4", 3, 3, sprites_data, "single", colors_data, "multi", 4)

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
    colors_data = "R"
    tetromino5 = Sprite("tetromino5", 3, 3, sprites_data, "single", colors_data, "multi", 4)

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
    colors_data = "G"
    tetromino6 = Sprite("tetromino6", 3, 3, sprites_data, "single", colors_data, "multi", 4)

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
    colors_data = "C"
    tetromino7 = Sprite("tetromino7", 4, 4, sprites_data, "single", colors_data, "multi", 4)

    # Smol pieces
    sprites_data = ["  ▄", "▄  ",
                    "  ▀", "▀  ",
                    
                    "  ▄", "   ",
                    "  ▀", "▀▀ ",

                    "   ", "▄  ",
                    " ▀▀", "▀  ",
                    
                    "   ", "▄  ",
                    "  ▀", "▀▀ ",
                    
                    "   ", "▄▄ ",
                    "  ▀", "▀  ",
                    
                    " ▄▄", "   ",
                    "  ▀", "▀  ",
                    
                    "   ", "   ",
                    " ▀▀", "▀▀ "]
    colors_data =  [color.fg(11), color.fg(11),
                    color.fg(11), color.fg(11),
                    
                    color.fg(208), color.fg(208),
                    color.fg(208), color.fg(208),

                    color.fg(12), color.fg(12),
                    color.fg(12), color.fg(12),
                    
                    color.fg(13), color.fg(13),
                    color.fg(13), color.fg(13),
                    
                    color.fg(9), color.fg(9),
                    color.fg(9), color.fg(9),
                    
                    color.fg(10), color.fg(10),
                    color.fg(10), color.fg(10),
                    
                    color.fg(14), color.fg(14),
                    color.fg(14), color.fg(14)]
    smol_pieces = Sprite("smol_pieces", 2, 2, sprites_data, "pixel_custom", colors_data, "multi", 7)
    # tetris variables
    piece = False
    pieces = [tetromino1, tetromino2, tetromino3, tetromino4, tetromino5, tetromino6, tetromino7]
    tetris_screen.initialize(5, color.bg(236))
    layer_1_pixel = []
    layer_1_color = []
    pieces_preview = []
    draw_layer = 2
    rotation = 0
    new_rot = 0
    tetris_debug = False
    fall = True
    gameover = False
    y = -2
    x = 9
    collision = False
    saved_piece = None
    saved = False
    saved_this_piece = False
    random_piece: Sprite
    score = 0
    # tetris funtions
    def check_piece_collitions(piece: Sprite, x, y, piece_rotation, direction: Literal["R", "L", "D", "Rot"], cuantity: int = 1):
        piece_data, _ = piece.load_raw(piece_rotation)
        for _ in range(len(piece_data)):
            for row in range(piece.height):
                for column in  range(piece.width):
                    index = row * piece.width + column
                    if piece_data[index] == "███":
                        new_x = x + column
                        new_y = y + row
                        if direction == "L" or direction == "R":
                            new_x += cuantity
                        if direction == "D":
                            new_y += cuantity
                        if new_x < 4:
                            return True
                        if new_x > 13:
                            return True
                        if new_y >= tetris_screen.height:
                            return True
                        try:
                            if layer_1_pixel[new_y][new_x] != "nop" and new_y > 0:
                                #log("info", f"collided!\n    extra info:\n    frame: {frame_counter}")
                                return True
                        except IndexError:
                            continue
                        
        return False
    # pre game loop code
    while len(pieces_preview) != 4:
        new_piece = random.choice(pieces)
        if not new_piece in pieces_preview:
            pieces_preview.append(new_piece)
        else:
            pass
    # game loop
    while True:
        frame_counter += 1
        draw_layer = 2
        gravity = 1
        tetris_screen.memory_reset()
        tetris_screen.set_bg(4, 0, 14, 20, color.bg(0))

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
        if "up" in tetris._actual_inputs and not saved_this_piece:
            if not saved:
                saved_piece = deepcopy(random_piece)
                random_piece = None
                piece = False
                fall = False
            elif saved:
                dummy = deepcopy(saved_piece)
                saved_piece = deepcopy(random_piece)
                random_piece = deepcopy(dummy)
                y = -2
                x = 8
                rotation = 0
                draw_layer = 2
            saved = True
            saved_this_piece = True
            tetris._actual_inputs.discard("up")
        if "space" in tetris._actual_inputs:
            new_rot = (rotation + 1) % random_piece._sprite_cuantity
            if not check_piece_collitions(random_piece, x, y, new_rot, "Rot", 1):
                rotation = new_rot
            tetris._actual_inputs.discard("space")

        if piece == False:
            rotation = 0
            draw_layer = 2
            piece = True
            random_piece = pieces_preview.pop(0)
            if collision:
                score += 40
            while len(pieces_preview) != 4:
                new_piece = random.choice(pieces)
                if not new_piece in pieces_preview:
                    pieces_preview.append(new_piece)
                else:
                    pass
            if check_piece_collitions(random_piece, x, y, rotation, "D", 1) and y <= 0:
                gameover = True
            log("info", f"selected {random_piece.name} at frame {frame_counter}")
            x = 8
            y = -2

        collision = False
        if piece == True:
            for _ in range(gravity):
                for px in range(random_piece.width):
                    if tetris_debug == True:
                        tetris_screen.create_pixel(x + px, y + random_piece.height + 1, 3, ("███", "", color.fg(9))) # debug draw for collisión
                    if check_piece_collitions(random_piece, x, y, rotation, "D", 1):
                        collision = True
                        piece = False
                        saved_this_piece = False
                        draw_layer = 1
                    elif collision:
                        fall = False
                if not collision and fall:
                    y += 1
            # Fall Preview
            my_y = y
            while not check_piece_collitions(random_piece, x, my_y, rotation, "D", 1):
                my_y += 1
            graphic = random_piece.load_raw(rotation)[0]
            tetris_screen.create_sprite(x, my_y, 2, (graphic, [color.fg(15)] * len(graphic)), 0, Sprite(random_piece.name, random_piece.width, random_piece.height, random_piece.readable_data[0], "single_custom", color.fg(15), random_piece.sprite_mode, random_piece._sprite_cuantity))
            tetris_screen.create_sprite(x, y, draw_layer, random_piece.load_raw(rotation), 0, random_piece) # Normal Piece

        clear_lines = []
        for row_line in range(len(layer_1_pixel)): # single row building
            row_data = []
            for width in range(tetris_screen.width):
                if width > 3 and width < 14:
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
            score += 100
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

        # UI
        slot_idxs = {"tetromino1" : 0,
                     "tetromino2" : 1,
                     "tetromino3" : 2,
                     "tetromino4" : 3,
                     "tetromino5" : 4,
                     "tetromino6" : 5,
                     "tetromino7" : 6}
        
        for slot in range(len(pieces_preview)):
            tetris_screen.create_sprite(1, 2 + (3 * slot), 2, smol_pieces.load_raw(slot_idxs.get(pieces_preview[slot].name)), 0, smol_pieces)
        tetris_screen.create_text(1, 1, 2, (" NEXT ", color.fg(15), ""))
        tetris_screen.create_text(1, 15, 2, (" SAVE ", color.fg(15), ""))
        tetris_screen.set_bg(1, 16, 3, 18, "")
        if saved_piece != None:
            tetris_screen.create_sprite(1, 16, 2, smol_pieces.load_raw(slot_idxs.get(saved_piece.name)), 0, smol_pieces)
        tetris_screen.create_text(15, 1, 2, ("   POINTS   ", color.fg(15), ""))
        scorestr = str(score)
        workvar = ""
        if len(scorestr) % 3 != 0:
            for _ in range(3 - (len(scorestr) % 3)):
                workvar = workvar + " "
        scorestr = workvar + scorestr
        cells = len(scorestr) // 3
        for _ in range(4 - cells):
            scorestr = "   " + scorestr
        tetris_screen.create_text(15, 2, 2, (scorestr, color.fg(15), ""))


        tetris_screen.bake_screen()
        tetris_screen.print_screen()
        #print(tetris._actual_inputs, x, y, piece, rotation, random_piece.name)
        #log("info", f"random piece is: {random_piece.name} at frame {frame_counter}\npiece is active?: {piece}")
        time.sleep(0.1)
        if gameover:
            break

        #log("info", f"layer 1 dump:\n{layer_1_pixel}")

tetris.start_input()
tetris.start_machine(tetris_loop)