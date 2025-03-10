# Quark
Quark is a super tiny compiled programming language, currently only supporting windows, but will migrate to other platforms very soon.
## Purpose
Quark is a DSL (Domain Specific Language), built specifically for basic automation, pranks and computer scripting.<br>
Quark is directly transpiled to x86-32 NASM syntax assembly, making it run blazingly fast.<br>
## Keep in mind
Quark is yet to support variables, functions or control loops. I am adding these as we speak, as of course, to be an actual programming language, they would need to be implemented.<br>

## Getting started
Make sure you have NASM and GCC installed, Quark is compiled to a 32 bit windows executable and used the NASM syntax during compilation.<br>

Once you have both NASM and GCC, you are ready to code. Clone the repo and we can start!

## Tutorial
Quark is currently a single line by line language, multiline statements are not supported, this will change once functions, variables and loops are implemented.<br>

### Hello World
Create a Quark file and write:<br>
`print("Hello, World!")` <br>
Thats it! Now, navigate to your console and type:<br>
`py main.py yourfile.qrk` <br>
After this you should see two files be outputted: A full executable and an assembly file, both with corresponding to your original Quark filename.<br>
You only need the executable, the assembly is just outputted for debugging and transparency.<br>

### Commands
Here is a list of all the commands in Quark: <br>

`print(value)` -> Prints a value to the console with a newline. <br>
`put(value)` -> Prints a value to the console without a newline. <br>
`beep(time, hz)` -> Plays a beep with the two arguments being time in ms and frequency. <br>
`cursorTo(x, y)` -> Moves the mouse cursor to a specified position<br>
`wait(time)` -> Halts the program for a specified time in ms.<br>
`msg(title, content)` -> Opens a windows system message popup on the users screen.<br>
`bell` -> Plays the windows bell notification sound<br>
`cursorClickL` -> Simulates a mouse left click.<br>
`cursorClickR` -> Simulates a mouse right click.<br>
`cursorHoldL` -> Holds the left mouse button.<br>
`cursorHoldR` -> Holds the right mouse button.<br>
`cursorUpL` -> Releases the left mouse button.<br>
`cursorUpR` -> Releases the right mouse button.<br>
`exec(program)` -> Starts the given program. <br>
`bgDisable` -> Clears the users wallpaper to a black screen <br>

## Example Program
```
print("Hello, User.")
wait(1000) 
bell
msg("Title", "Your about to be pranked")
wait(500)
cursorTo(100,100)
cursorHoldL
cursorTo(1000,1000)
cursorUpL
beep(500,1000)
```

## Thats all folks!
Thats it for now, however, any contributions are greatly appreciated. I will be updating this soon.