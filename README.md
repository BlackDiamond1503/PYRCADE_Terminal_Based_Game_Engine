# Pyrcade - Python Terminal Based "Game Engine"
### What is this?
This is a Python "Game Engine", it uses the terminal to output video and uses many libraries to make things like listen to the keyboard input, have good "video memory" management and other things. Started jut for fun ans to pass the time, all while I learned more about python and how it works
___
### 2 Engine versions on the repository
The .old.py engine is the prototype engine, not very good and I'm not very proud of it. The Pyrcade.py file is the new class based engine, the new and improved version of it.

#### *Arcade.old.py*
The Prototype engine, works with global variables and functions, is effective but hard to work in if implementing a new game. The mainloops are messy and confusing, the sprite implementation is hard to work with, the input is handled per game, not globally, and more problems

#### *Pyrcade.py*
The new class based engine, the class based tag is because I've never coded with classes (very easy to do, and I've never done it 'till now). Cleaner, easier to work in, more understandable, easier to debug in, there are just many advantages comparing it to the old one. 
___
### Features
#### Individual Arcade "Managment"
The `arcade` class is a "machine" that contains a "screen" (`screen` class object), an input listener system (managed by the `pynput` library) and a main code loop to run (a simple function with the "machine's code").

#### Logging System for Debuging
It will write to a log file on the `logs` folder, it will be a `.txt` that will have debug information that can be used to spot problems in the game loops or the engine itself. The system can be toggled ON and OFF in the global variable `DEBUG` at the top of the entire source code (The logging is being actively developed and improved)

#### Screen Managment
The `screen` class has many methods to modify it's memory, which is divided into `pixel_layers` and `color_layers` to separate color and pixel information for convinience. `screen.create_pixel` creates a single pixel on a determined `x`, `y` and `layer` on the screen, it will have 3 characters worth of information and two colors; foegroung and background. `screen.create_sprite` takes a `sprite` class object and it's data to be pasted in certain `x`, `y` and `layer` of the screen memory

#### Sprites
The `sprite` class is a calss that has some parameters attached to it; `height`, `width`, `pixel_data`, `color_data`, and other parameters. All these propieties manage how the sprite is drawn to the screen. The data itself is writen on a "Human Friendly" format, then is translated into engine raw data for it to process.
___
### Examples
The engine includes some example games to try out

#### Tetris (Python)
A recreation of __Tetris__ using the __Pyrcade Engine__ and __Python__, it is very similar to other Tetris versions and runs perfectly on within the temrinal, by importing `pyrcade_engine` into the __Tetris__ file we have the engine working as expected, and we separate the games from the engine (Unlike the `arcade.old.py` engine)