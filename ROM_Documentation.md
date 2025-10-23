# **Pyrcade ROM Documentation**
This is a documentation for the making of games in the pyrcade engine without using python, but a custom script format for to engine and the included interpreter.

## **Sections**
+ [File Types](#file-types)
+ [File Syntax](#file-syntax)
  + [General Syntax](#general-syntax) 
  + [Pyrcade Game File (.pyrg)](#pyrcade-game-file-pyrg-1)

## **File Types**
A Pyrcade ROM is conformed by 3 different files, these are:
### **Pyrcade Game File (`.pyrg`)**
> This file is like a **Header** for the **ROM**. It contains general **metadata** of the game, like the name, logo image name, screen related things, and others.
### **Pyrcade Script File (`.pyrs`)**
> This file is the game's code, it will contain the instructions for the game in the language **Pyrcade Script**, this language is better detailed in the [Pyrcade Script]() section of this documentation.
### **Pyrcade Asset File (`.pyra`)**
> This file contains the graphical information if the game; sprites, text, logos, etc. This file is separated on "Data Blocks", each item has one data block with it's own metadata.
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
#### **Commands and Objects:**

> Indicates the use of a `command`, or to set a `metadata` or a `variable` object's `values`. A `command` or `metadata` name doesn't have spaces, if it does, or the name is not found, the object is treated as a custom `variable`. The `arguments` or `values` to use are declared right after the last `:`.

```
:command:
```
___
#### **Arguments and Values:**
> A command may need an argument, an argument is between `{}`, and it may need a value addoiated to it, so we use `:` and we put the value in `()`
```
:command: {argument: (value)}   #argument with value
:command: {argument}            #only argument
```
___
___
### **Pyrcade Game File (`.pyrg`)**
This file acts as the **header** of the ROM, it contains metadata for the game that the interpreter uses to create the game instance. The metadata that this file **MUST** contain is described bellow.
#### **Basic Command:**
> The command used to set the value of a variable, like the metadata on the header, is `:set:`. The only argument that the command needs is the name of the variable to set and the value to be used

Syntax:
```
:set: {name: (value)}
```
___
#### **Name:**
> The name of the game, used to dysplay the game in the launcher. **MUST** be text

Syntax:
```
:set: {name: (name)}
```
___
#### **Type:**
> [!NOTE]
> Not implemented yet

> The type of the game, it says if the game runs on the **Terminal** or on a separate **Window** 

Syntax:
```
:set: {type: (type)}
``` 

Posible Arguments:
```
{type: (terminal)}
{type: (windowed)}
```
___
#### **Engine Version:**