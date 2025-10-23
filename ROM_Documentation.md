# Pyrcade ROM Documentation
This is a documentation for the making of games in the pyrcade engine without using python, but a custom script format for to engine and the included interpreter.

## File Types
A Pyrcade ROM is conformed by 3 different files, these are:
### Pyrcade Game File (`.pyrg`)
> This file is like a **Header** for the **ROM**. It contains general **metadata** of the game, like the name, logo image name, screen related things, and others.
### Pyrcade Script File (`.pyrs`)
> This file is the game's code, it will contain the instructions for the game in the language **Pyrcade Script**, this language is better detailed in the [Pyrcade Script]() section of this documentation.
### Pyrcade Asset File (`.pyra`)
> This file contains the graphical information if the game; sprites, text, logos, etc. This file is separated on "Data Blocks", each item has one data block with it's own metadata.
___
___
## File Syntax
A game ROM is formed by 3 files; one `.pyrg`, one `.pyrs` and one `.pyra`. These files **MUST** have the same name, so the launcher can recognize the ROM, if not, the launcher will refuse to see the ROM and raises an `IncompleteROMError`.
___
### General Syntax
#### Spaces:

> Spaces are ignored if they are not interacting directly with an object's name. Aka, if the space is not inside `{}`, `()` or `::`, the interpreter ignores them.

#### Comments:

```
# single line comment
```
```
'''
multi line comment / comment block
'''
```

> Using a `#` creates a single line comment, using a set of `'''` starts or ends a comment block.

#### Commands and Objects:
```
:name: (argument){value}; (argument){value}
```
> Indicates the use of a `command`, or to set a `metadata` or a `variable` object's `values`. A `command` or `metadata` name doesn't have spaces, if it does, or the name is not found, the object is treated as a custom `variable`. The `arguments` or `values` to use are declared right after the last `:`.

#### Arguments and Values:
```
{argument}(value); ...
```
> An argument can be given via `{}`, every `command` / `function` has their own arguments, they are greatly explained in the [Pyrcade Script]() section.
> A value can be given via `()`, some commands requiere a value after an argument, or only a value. The value has to go right after the argument, if not, the interpreter will raise an `ArgumentError`
___
### Pyrcade Game File (`.pyrg`)
This file acts as the **header** of the ROM, it contains metadata for the game that the interpreter uses to create the game instance. The metadata that this file **MUST** contain is described bellow.

#### Name:
```
:name: {name}
```
#### Type:
> [!CAUTION]
> Not Finished Yet
```
:type: {type}
```
> The type of the game, it says if the game runs on the **Terminal** or on a **Window**