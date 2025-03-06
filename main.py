import sys
import re
import subprocess
import os
import ast

sectionData = ["section .data"]
sectionText = ["", "section .text", "global _main", "extern _printf", "extern _ExitProcess@4"]
sectionMain = ["", "_main:"]




def ErrorRaise(type, subject = None):
    if type == "fname":
        print("Error:\nNo filename was supplied into the compiler.\nTry: 'py main.py file.qrk'")
        exit()
    if type == "exist":
        print(f"Error:\nFile '{subject}' does not exist. \nTry: check the directory and the command passed.")
        exit()
try:
    quarkFileName = sys.argv[1]
except IndexError:
    ErrorRaise("fname")

def find_between(line, start, end):
    start = re.escape(start)
    end = re.escape(end)

    pattern = f'{start}(.*?){end}'

    match = re.search(pattern, line)

    if match:
        return match.group(1)
    else:
        return None
def extract_arguments(s):
    
    try:
        arguments = ast.literal_eval(s)
        
        if isinstance(arguments, tuple):
            return list(arguments)
        else:
            return []
    except (SyntaxError, ValueError):
        return []

def printCall(line, arg):
    referenceLine = line
    
    if "print(" in line:
        line = str(line).removeprefix("print")
    elif "put(" in line:
        line = str(line).removeprefix("put")
    call = "print"+str(arg)
   
    value = find_between(line, "(", ")")
    
    if '"' in value or "'" in value:
    
        if "put(" in referenceLine:
            dataStatement = call+" db "+value+", 0"
        elif "print(" in referenceLine:
            dataStatement = call+" db "+value+", 10, 0"

        sectionData.append(dataStatement)
        mainStatment = "push "+call
        sectionMain.append(mainStatment)
        sectionMain.append("call _printf")
        sectionMain.append("add esp, 4")

    else: #Barebones Number support, will buff this out better.
        if "put(" in referenceLine:
            dataStatement = call+" db \"%d\", 0"
        elif "print(" in referenceLine:
            dataStatement = call+" db \"%d\", 10, 0"

        sectionData.append(dataStatement)
        mainStatment = "push "+value
        sectionMain.append(mainStatment)
        mainStatment = "push "+call
        sectionMain.append(mainStatment)
        
        sectionMain.append("call _printf")
        sectionMain.append("add esp, 4")
    
    
    

def msgCall(line, arg):

   
    line = str(line).removeprefix("msg")
    
    value = find_between(line, "(", ")")
    title = extract_arguments(line)[0]
    message = extract_arguments(line)[1]
    


    call = "msg"+str(arg)
    
    
    if "extern _MessageBoxA@16" not in sectionText:
        sectionText.append("extern _MessageBoxA@16")
    
    sectionMain.append("push 0")

    dataStatement = call+" db "+"'"+message+"', 0"
    sectionData.append(dataStatement)

    mainStatment = "push title"+str(arg)
    sectionMain.append(mainStatment)

    mainStatment = "push "+call
    sectionMain.append(mainStatment)



    dataStatement = "title"+str(arg)+" db "+"'"+title+"', 0"
    sectionData.append(dataStatement)

    
    sectionMain.append("push 0")
    sectionMain.append("call _MessageBoxA@16")

def beepCall(line, arg):

   
    line = str(line).removeprefix("beep")
    
    value = find_between(line, "(", ")")
    duration = value.split(",")[0].strip()
    freq = value.split(",")[1].strip()

    if "extern _Beep@8" not in sectionText:
        sectionText.append("extern _Beep@8")
    sectionMain.append("push "+str(duration))
    sectionMain.append("push "+str(freq))
    
    sectionMain.append("call _Beep@8")

def waitCall(line, arg):

   
    line = str(line).removeprefix("wait")
    
    value = find_between(line, "(", ")")
     

    if "extern _Sleep@4" not in sectionText:
        sectionText.append("extern _Sleep@4")
    sectionMain.append("push "+(value.strip()))
    
    
    sectionMain.append("call _Sleep@4")

def cursorCall(line, arg):

   
    line = str(line).removeprefix("cursorTo")
    
    value = find_between(line, "(", ")")
    x = value.split(",")[0].strip()
    y = value.split(",")[1].strip()

    if "extern _SetCursorPos@8" not in sectionText:
        sectionText.append("extern _SetCursorPos@8")
    sectionMain.append("push "+str(x))
    sectionMain.append("push "+str(y))
    
    sectionMain.append("call _SetCursorPos@8")
def cursorClick(line, arg):
    if "extern _mouse_event@20" not in sectionText:
        sectionText.append("extern _mouse_event@20")

    if "cursorClickL" in line:
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x02")
        sectionMain.append("call _mouse_event@20")
        
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x04")
        sectionMain.append("call _mouse_event@20")
    elif "cursorClickR" in line:
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x08")
        sectionMain.append("call _mouse_event@20")
        
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x10")
        sectionMain.append("call _mouse_event@20")
def cursorUp(line, arg):
    if "extern _mouse_event@20" not in sectionText:
        sectionText.append("extern _mouse_event@20")

    if "cursorUpL" in line:
       
        
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x04")
        sectionMain.append("call _mouse_event@20")
    elif "cursorUpR" in line:
        
        
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x10")
        sectionMain.append("call _mouse_event@20")

def cursorHold(line, arg):
    if "extern _mouse_event@20" not in sectionText:
        sectionText.append("extern _mouse_event@20")

    if "cursorHoldL" in line:
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x02")
        sectionMain.append("call _mouse_event@20")
        
       
    elif "cursorHoldR" in line:
        for i in range(0,3):
            sectionMain.append("push 0")
        sectionMain.append("push 0x08")
        sectionMain.append("call _mouse_event@20")
        

def passCommandCall(line, arg):
    line = str(line).removeprefix("exec")
    value = find_between(line, "(", ")")
    

    if "extern _ShellExecuteA@24" not in sectionText:
        sectionText.append("extern _ShellExecuteA@24")

    dataStatement = "exec"+str(arg)+" db "+value+", 0"
    sectionData.append(dataStatement)
    
    sectionMain.append("push 1")
    sectionMain.append("push 0")
    sectionMain.append("push 0")

    sectionMain.append("push exec"+str(arg))
    sectionMain.append("push 0")
    sectionMain.append("push 0")

    sectionMain.append("call _ShellExecuteA@24")

def passBell(line, arg):
    if "bell db 7, 0" not in sectionData:
        dataStatement = "bell db 7, 0"
        sectionData.append(dataStatement)

    sectionMain.append("push bell")
    sectionMain.append("call _printf")
    sectionMain.append("add esp, 4")

def passBg(line, arg):

    

    if "extern _SystemParametersInfoA@16" not in sectionText:
        sectionText.append("extern _SystemParametersInfoA@16")
    sectionData.append("uflag"+str(arg)+" dd 1")
    sectionData.append("null"+str(arg)+" db 'null/void', 0")

    sectionMain.append("push 0")
    sectionMain.append("push uflag"+str(arg))
    sectionMain.append("push null"+str(arg))
    sectionMain.append("push 0x0014")
    sectionMain.append("call _SystemParametersInfoA@16")


      



def exitCall():
    sectionMain.append("push 0")
    sectionMain.append("call _ExitProcess@4")
    

def Parse(line, arg):
    if "print(" in line:
        if line[0:6] == "print(":
            printCall(line, arg)

    elif "put(" in line:
        if line[0:4] == "put(":
            printCall(line, arg)
    elif "msg(" in line:
        if line[0:4] == "msg(":
            msgCall(line, arg)
    elif "beep(" in line:
        if line[0:5] == "beep(":
            beepCall(line, arg)
    elif "cursorTo(" in line:
        if line[0:9] == "cursorTo(":
            cursorCall(line, arg)

    elif "cursorClickL" in line:
        if line[0:12] == "cursorClickL":
            cursorClick(line, arg)
    elif "cursorClickR" in line:
        if line[0:12] == "cursorClickR":
            cursorClick(line, arg)
    elif "cursorHoldL" in line:
        if line[0:11] == "cursorHoldL":
            cursorHold(line, arg)
    elif "cursorHoldR" in line:
        if line[0:11] == "cursorHoldR":
            cursorHold(line, arg)
    elif "cursorUp" in line:
        if line[0:8] == "cursorUp":
            cursorUp(line, arg)

    elif "wait(" in line:
        if line[0:5] == "wait(":
            waitCall(line, arg)
    elif "exec(" in line:
        if line[0:5] == "exec(":
            passCommandCall(line, arg)
    elif "bell" in line:
        if line[0:4] == "bell":
            passBell(line, arg)
    elif "BgDisable" in line:
        if line[0:9] == "BgDisable":
            passBg(line, arg)
    
    elif str(line).startswith("\\\\"):
        pass
    if arg == len(quarkLines)-1:
        exitCall()
    


try:
    with open(quarkFileName) as f:
        quarkContent = f.read()
        f.close()
except FileNotFoundError:
    ErrorRaise("exist", quarkFileName)

quarkLines = quarkContent.splitlines()
for i, line in enumerate(quarkLines):
    Parse(line, i)

fullCode = "\n".join(sectionData + sectionText + sectionMain)

def Compile():
    with open("a.asm", "w") as file:
        file.write(fullCode)

    subprocess.run(["nasm", "-f", "win32", "a.asm", "-o", "a.obj"])

    subprocess.run(["gcc", "a.obj", "-o", "a.exe"])
    os.remove("a.obj")

def Debug():
    print(fullCode)

Compile()