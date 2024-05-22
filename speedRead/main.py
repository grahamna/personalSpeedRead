import time
import os
import re
import keyboard


def wordNav(direction:int):
    global going, count
    if going: return
    else:
        if direction ==  1:
            count+=1
            terminalPrint(count)
        elif direction == -1:
            count-=1
            terminalPrint(count)


def speedMod(mod:int):
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
        
def printToTerminal(fileName:str):
    
    global count, speedVar, going, neededWhiteSpace, oldTerminalWidth, length, inString

    length = len(inString)

    speedText = "lower is faster"
    progressText = "current / total"
    oldTerminalWidth = os.get_terminal_size()[0]
    neededWhiteSpace = oldTerminalWidth - len(speedText) - len(progressText)
    print(f'\r{progressText}{fileName.center(neededWhiteSpace -1 , " " )}{speedText}')

    while count != length:
        if (not going):
            keyboard.wait('space')
        speed, count = terminalPrint(count)
        if 0.1 + speed > 0:
            time.sleep(0.1 + speed)
            count+=1
        else: 
            speed = 0.1
            speedVar = 0

def terminalPrint(newCount) -> (int, int):
        global oldTerminalWidth, neededWhiteSpace, count, speedVar, inString
        count = newCount
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
        wordSize = len(word)
        speed = (wordSize*0.02) * speedVar 
        print(f'\r{progressString}{newWord.center(neededWhiteSpace, " " )}Speed:{speedVar:.2f}', end='')
        return speed, count

def splitUtilString(strIn) -> str:
    if(strIn == ''): 
        return
    if(isinstance(strIn, str)):
        temp = strIn.strip()
        if temp != '':
            res = re.split(r'\s+', temp)
            return res
        return
    else:
        res = []
        for string in strIn:
            if string != '':
                res.extend(splitUtilString(string))
        return res

def main():
    
    global speedVar, going, count, inString
    count = 0
    speedVar = 1
    going = False

    fin = input("Name of file in the folder /input \n => ")
    
    keyboard.add_hotkey("LEFT", lambda: wordNav(-1))
    keyboard.add_hotkey("RIGHT", lambda: wordNav(1))
    keyboard.add_hotkey("DOWN", lambda: speedMod(1))
    keyboard.add_hotkey("UP", lambda: speedMod(0))
    keyboard.add_hotkey("space", lambda: speedMod(-1))
    
    dirname = os.path.dirname(__file__)
    myFile:str = os.path.join(dirname, f'../input/{fin}')
    with open(myFile, 'r', encoding="utf-8") as inputFile:
        buffer = inputFile.read()
        
        inString = splitUtilString(buffer)
    
    try:
        printToTerminal(fin)
    except KeyboardInterrupt:
        print("\nExiting via keyboardInterrupt")
    
if __name__ == '__main__':
    main()