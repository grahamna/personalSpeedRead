import time, os, re

import keyboard


def wordNav(direction:int) -> None:
    global going, count
    if going: return
    else:
        if direction ==  1:
            count+=1
            terminalPrint(count)
        elif direction == -1:
            count-=1
            terminalPrint(count)
        else:
            # bookmark function
            os._exit(1)


def speedMod(mod:int) -> None:
    global speedVar, going
    if mod == 0:
        speedVar = speedVar + 0.05
        if (not going):
            terminalPrint(count)
    elif mod == 1:
        speedVar = speedVar - 0.05
        if (not going):
            terminalPrint(count)
    else:
        going = not going
        
def printToTerminal(fileName:str) -> None:
    global count, speedVar, going, neededWhiteSpace, oldTerminalWidth, length, inString

    assert inString is not None
    length = len(inString)

    speedText = "lower is faster"
    progressText = "current / total"
    oldTerminalWidth = os.get_terminal_size()[0]
    neededWhiteSpace = oldTerminalWidth - len(speedText) - len(progressText)
    print(f'\r{progressText}{fileName.center(neededWhiteSpace -1 , " " )}{speedText}')

    while count < length:
        if (not going):
            count-=1
            keyboard.wait('space')

        count+=1
        word, count = terminalPrint(count)
        
        wordSize = len(word)
        speed = (wordSize*0.0185) * speedVar

        if 0.1 + speed > 0:
            time.sleep(0.1 + speed)
        else: 
            speed = 0.1
            speedVar = 0

def terminalPrint(newCount:int) -> tuple[str, int]:
        global oldTerminalWidth, neededWhiteSpace, count, speedVar, inString
        count = newCount

        assert inString is not None
        word = inString[count]
        progressString:str = f'{count + 1}/{length}'
        newWord:str = f"> {word} <"
        terminalWidth:int = os.get_terminal_size()[0]

        if (oldTerminalWidth < terminalWidth):
            oldTerminalWidth = terminalWidth
            print(f'\r',end = '')
        elif (oldTerminalWidth > terminalWidth):
            oldTerminalWidth = terminalWidth
            print('\033[2K\033[1G\033[F\033[2K\033[1G',end='',flush=True)

        neededWhiteSpace = terminalWidth - (len(progressString) + len(f'Speed:{speedVar:.2f}')) - 8
        print(f'\r{progressString}{newWord.center(neededWhiteSpace, " " )}Speed:{speedVar:.2f}', end='')

        return (word, count)

def splitUtilString(strIn:str|list[str]) -> list[str] | str | None:
    if(strIn == ''): 
        return
    if(isinstance(strIn, str)):
        temp = strIn.strip()
        if temp != '':
            res = re.split(r'\s+', temp)
            return res
        return
    else:
        res:list[str] = []
        for string in strIn:
            if string != '':
                temp = splitUtilString(string)
                assert temp is not None
                res.extend(temp)
        return res

def getFileToRead() -> tuple[ list[str] | str | None,  str]:

    fileName = input("Name of file in the folder /input \n => ")
    dirName = os.path.dirname(__file__)
    myFile:str = os.path.join(dirName, f'../input/{fileName}')

    try:
        with open(myFile, 'r', encoding="utf-8") as inputFile:
            buffer = inputFile.read()
            fileContents = splitUtilString(buffer)
        return fileContents, fileName
    except FileNotFoundError: 
        print(f"Failed to find file {fileName} in dir /input")
        return getFileToRead()


def main() -> None:
    
    global speedVar, going, count, inString
    count = 0
    speedVar = 1
    going = False
    
    
    inString,fileName = getFileToRead()

    if (inString is not None):
        try:
                # setting up hotkeys, activate regardless of window focus
            keyboard.add_hotkey("LEFT", lambda: wordNav(-1))
            keyboard.add_hotkey("RIGHT", lambda: wordNav(1))
            keyboard.add_hotkey("DOWN", lambda: speedMod(1))
            keyboard.add_hotkey("UP", lambda: speedMod(0))
            keyboard.add_hotkey("space", lambda: speedMod(-1))
            keyboard.add_hotkey("esc", lambda: wordNav(0))

            hotkeyHeader = "Hotkeys Activated:\n\t| space to play / pause | UP / DOWN arrow(s) to modify reading speed |\n\t| [while paused] LEFT / RIGHT arrow to navigate words  | esc to quit |"
            print(hotkeyHeader)

            printToTerminal(fileName)
        except KeyboardInterrupt:
            print("\nExiting via KeyboardInterrupt")
            # bookmark function
            os._exit(1)
    else:
        print(f"File {fileName} is empty, exiting")


if __name__ == '__main__':
    main()