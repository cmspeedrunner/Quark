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

`print` -> Prints a value to the console with a newline. <br>
`put` -> Prints a value to the console without a newline. <br>
`beep(time, hz)` -> Plays a beep with the two arguments being time and frequency. <br>
