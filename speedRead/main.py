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

def quitProgram(fileName:str) -> None:
    global going, count
    if going: return
    else:
        insertBookmark(fileName)
        os._exit(1)

def printToTerminal(fileName:str) -> None:
    global count, speedVar, going, neededWhiteSpace, oldTerminalWidth, length, inString

    assert inString is not None
    length = len(inString)

    speedText = "lower is faster"
    progressText = "current / total"
    oldTerminalWidth = os.get_terminal_size()[0]
    neededWhiteSpace = oldTerminalWidth - len(speedText) - len(progressText)
    print(f'\r{progressText}{fileName.center(neededWhiteSpace -1 , " " )}{speedText}')

    while count < length - 1:

        word, count = terminalPrint(count)
        count+=1

        if (not going):
            count-=1
            keyboard.wait('space')
        
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
        if count < 0 : count = 0
        if count >= length: count = length -1

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
    global count, hasBookMark
    fileName = input("Name of file in the folder /input \n => ")
    dirName = os.path.dirname(__file__)
    myFile:str = os.path.join(dirName, f'../input/{fileName}')

    try:
        with open(myFile, 'r', encoding="utf-8") as inputFile:
            buffer = inputFile.read()
            fileContents = splitUtilString(buffer)
            assert fileContents is not None
            count, hasBookMark = searchForBookmarks(fileContents)
        return fileContents, fileName
    except FileNotFoundError: 
        print(f"Failed to find file {fileName} in dir /input")
        return getFileToRead()

def searchForBookmarks(fileContents:list[str] | str) -> tuple[int, bool]:
    mark:str = fileContents[-1]
    if '<<_BookMark_>>' in mark:
        hasBookMark = True
        bookmarkParse = re.findall(r'\d+', mark)[-1]
        assert bookmarkParse is not None
        bookmarkCount = int(bookmarkParse)
            
        length = len(fileContents)
        if bookmarkCount <= length:
            print(f"Found BookMark Ref for index {bookmarkCount}/{len(fileContents)}")
            answer = input("Resume from Bookmark?  (Y/n)\n => ")
            if answer == '' or answer.startswith('y') or answer.startswith('Y'):
                return bookmarkCount, hasBookMark
            else: 
                print("Bookmark Ref not used")
        else:
            print("Bookmark ref not valid (larger than the total length of file)")
    else:
        print("Bookmark Ref not found")
        hasBookMark = False
    return 0, hasBookMark

def insertBookmark(fileName:str):
    global count, hasBookMark
    dirName = os.path.dirname(__file__)
    myFile:str = os.path.join(dirName, f'../input/{fileName}')
    try:
        with open(myFile, 'a+', encoding="utf-8") as inputFile:
            if hasBookMark:
                inputFile.seek(0,os.SEEK_END)
                cur = inputFile.tell() -1
                while inputFile.read(1) != '\n' and cur > 0:
                    cur = cur - 1
                    inputFile.seek(cur, os.SEEK_SET)
                if cur > 0:
                    inputFile.seek(cur, os.SEEK_SET)
                    inputFile.truncate()
                    inputFile.flush()
                    inputFile.write(f"\n<<_BookMark_>>{count}")
            else:
                inputFile.write(f"<<_BookMark_>>{count}")
            print(f"\nBookmark made at index {count+1}")
    except:
        print("Saving bookmark failed. Bookmark not created")

def setKeybinds(fileName:str):
        # setting up hotkeys, activate regardless of window focus
    keyboard.add_hotkey("LEFT", lambda: wordNav(-1))
    keyboard.add_hotkey("RIGHT", lambda: wordNav(1))
    keyboard.add_hotkey("DOWN", lambda: speedMod(1))
    keyboard.add_hotkey("UP", lambda: speedMod(0))
    keyboard.add_hotkey("space", lambda: speedMod(-1))
    keyboard.add_hotkey("esc", lambda: quitProgram(fileName))

    hotkeyHeader = "Hotkeys Activated:\n\t| space to play / pause | UP / DOWN arrow(s) to modify reading speed |\n\t| [while paused] LEFT / RIGHT arrow to navigate words  | esc to quit |"
    print(hotkeyHeader)

def main() -> None:
    
    global speedVar, going, count, inString, hasBookMark
    speedVar = 1
    going = False
    
    
    inString,fileName = getFileToRead()

    if (inString is not None):
        try:
            setKeybinds(fileName)

            printToTerminal(fileName)
        except KeyboardInterrupt:
            print("\nExiting via KeyboardInterrupt")
            insertBookmark(fileName)
            os._exit(1)
    else:
        print(f"File {fileName} is empty, exiting")


if __name__ == '__main__':
    main()