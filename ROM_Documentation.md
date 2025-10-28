# **Pyrcade ROM Documentation**
This is a documentation for the making of games in the pyrcade engine without using python, but a custom script format for to engine and the included interpreter.

## **Sections**
+ [File Types](#file-types)
+ [File Syntax](#file-syntax)
  + [General Syntax](#general-syntax) 
  + [Pyrcade Script File (.pyrs)](#pyrcade-script-file-pyrs-1)
  + [Pyrcade Game File (.pyrg)](#pyrcade-game-file-pyrg-1)
  + [Pyrcade Assets File (.pyra)](#pyrcade-asset-file-pyra-1)

## **File Types**
A Pyrcade ROM is conformed by 3 different files, these are:
### **Pyrcade Script File (`.pyrs`)**
> This file is the game's code, it will contain the instructions for the game in the language **Pyrcade Script**, this language is better detailed in the [Pyrcade Script]() section of this documentation.
### **Pyrcade Game File (`.pyrg`)**
> This file is like a **Header** for the **ROM**. It contains general **metadata** of the game, like the name, logo image name, screen related things, and others.
### **Pyrcade Asset File (`.pyra`)**
> This file contains the graphical information if the game; sprites, text, logos, etc. This file is separated on "Data Blocks", each item has one data block with it's own metadata.
### **Extra data (`.txt`)**
> For extra data, we use `.txt` files, these files can only contain 1 block of data, like the mutiple ones of `.pyra` files. The file has no **header**, so it is pure data.
___
___
## **File Syntax**
A game ROM is formed by 3 files; one `.pyrg`, one `.pyrs` and one `.pyra`. 
> [!IMPORTANT]
> These files **MUST** have the same name, so the launcher can recognize the ROM, if not, the launcher will refuse to see the ROM and raises an `IncompleteROMError`.
___
### **General Syntax**
#### **Spaces**:

> Spaces are ignored if they are not interfiering with an object's name / definition. So a space after a `:` is ignored, but makes the code more readable, just like python.
___
#### **Comments**:

> Using a `#` creates a single line comment, using a set of `'''` starts or ends a comment block.

```
# single line comment
```
```
'''
multi line comment / comment block
'''
```
___
#### **Commands:**

> The instructions are reffered as commands, to use a command we use `@` at the start of the name, and `:` at the end of the name. Then, we use `;` as a line terminator to indicate the interpreter to go to the next line, so everything after that is gonna be ignored.

Syntax:

```
@command_name:;
```
___
#### **Arguments and Values:**
> Some commands need an argument, an argument is declared by using `{}`, and an argument may need a value, so we use `:` and we put the value in `()`. To separate arguments when manny needed, we use `,`.
```
@command_name: {argument: (value)};     #argument with value
@command_name: {argument};              #only argument
@command_name: {argument}, {argument};  #mutli argument command
@command_name: (value);                 #value
@command_name: (value), (value);        #multi value command
```
___
___
### **Pyrcade Script File (.pyrs)**
This file contains all the game's mainloop or silgle run code, you can also make functions that you can `@call:` to use them, they need to go into the `functions` folder.
> [!NOTE]
> The file MUST have the command `@function:` at the start of it, if not, the interpreter will not read it as a function / single run code, but as an infinite loop.
___
#### **Pyrcade Script**
This is the language thet the `.pyrs` files use, it is conformed by **commands**, those commands can come in two types:  
+ Commands with no Arguments
+ Commands with Arguments
___
#### **Commands with no Arguments**
These tell the interpreter how to a file as, or how to use a block of data as. These commands are not used much in normal code, but they are used in functions or the other files (specified if so)  
The commands in this category are:
+ `@function:`
> This command tells the interpreter that the file it is in is a function, so is a "callable" and MUST be "imported" and "called" in another file to be used.
+ `@end:`
>This command declares the end of the primary code, everything after it gets ignored, and it is only accesable with a `@goto:` command.
+ `@data_block_start:`
>This command indicates the start of a data block. **(metadata + data)**  
> ***Used only in `.pyra` files***
+ `@data_block_end:`
>This command indicates the end of a data block. **(metadata + data)**  
> ***Used only in `.pyra` files***
+ `@sprite_data_start:`
>This command indicates the start of a sprite's data block. **(data only)**  
> ***Used only in `.pyra` files***
+ `@sprite_data_end:`
>This command indicates the end of a sprite's data block. **(data only)**  
> ***Used only in `.pyra` files***
___
#### **Commands with arguments**
These commands are the most common, the most used in code, some are also used in th metadata (specified if so). All of these commands MUST contain arguments, if not, they are gonna raise an `ArgumentError`.  
The commands in this category are:
+ `@set: {variable_name: (value)}`
> This command is used to set an specific variable to an specific value, whether it is a `number`, `string` or `object`.  
> **Syntax:**
>```
>@set: {name: (name)};                                  # single set example
>@set: {name: (name)}, {name: (name)}, {name: (name)};  # multi set example
>```
___
___
### **Pyrcade Game File (`.pyrg`)**
This file acts as the **header** of the ROM, it contains metadata for the game that the interpreter uses to create the game instance. The metadata that this file **MUST** contain is described bellow.
___
#### **Name:**
> The name of the game, used to dysplay the game in the launcher. **MUST** be text

Syntax:
```
@set: {name: (name)};
```
___
#### **Icon**
> The launcher also needs the name of the sprite that has the icon, said sprite has to be in the [Pyrcade Asset File]()

Syntax:
```
@set: {icon: (icon's_name)};
```
___
#### **Type:**
> [!NOTE]
> Not implemented yet

> The type of the game, it says if the game runs on the **Terminal** or on a separate **Window** 

Syntax:
```
@set: {type: (type)};
``` 

Posible Arguments:
```
{type: (terminal)}
{type: (windowed)}
```
___
#### **Engine Version:**
> The engine, as any other engine, has updates. This means that there are features that doesn't work on older versions of the engine / launcher, or that directly are not present, so the ROM needs a specific **MINIMUM** version to work.

Syntax:
```
@set: {min_version:(version)};
```
> [!NOTE]
> The minimum version that the game can have is `1.0.0`, but that doesn't mean is recommended to use it.
___
#### **Screen Dimentions:**
> The screen dimentions have to be declared, thats how the screen will output video. These have to be set individually.

Syntax:
```
@set: {screen_width: (width)}, {screen_height: (height)};
```
___
#### **Frame Rate (Frames per Seciond):**
> The cuantity of frames the game will show in one second, not recommended to set higer than 30

Syntax:
```
@set: {FPS: (Frame_Rate)};
```
___
#### **Background Color:**
> The color of the background. It must be a number from 0 to 255, the equivalent colors are in the [color-codes.png](/color-codes.png) file, inclused in the repository.

Syntax:
```
@set: {BG: (bg_color)};
```
___
#### **Header Example:**
```
@set: {name: (Header Example)};
@set: {type: (terminal)};
@set: {icon: (Icon Example)};
@set: {min_version: (1.0)};
@set: {screen_width: (10)}, {screen_height: (10)};
@set: {FPS: (10)};
@set: {BG: (11)};
```
___
#### **Header Code**
> You can also set some things before running the main loop, aka the [Pyrcade Script File](). You can set up constants, default variables, etc. All the commands that can or cannot be used here are discribed into the [Pyrcade Script]() section.
___
___


### **Pyrcade Asset File (`.pyra`)**