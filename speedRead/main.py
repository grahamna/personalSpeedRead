import time
import os
import re

def printToTerminal(inString:str, fileName:str):
    length = len(inString)
    count = 0
    global speedVar
    speedText = "lower is faster"
    progressText = "current / total"
    oldTerminalWidth:int = os.get_terminal_size()[0]
    neededWhiteSpace = oldTerminalWidth - len(speedText) - len(progressText)
    print(f'\r{progressText}{fileName.center(neededWhiteSpace -1 , " " )}{speedText}')
    for word in inString:
        count = count + 1
        progressString:str = f'{count}/{length}'
        newWord:str = f"> {word} <"
        terminalWidth:int = os.get_terminal_size()[0]
        if (oldTerminalWidth < terminalWidth):
            oldTerminalWidth = terminalWidth
            print(f'\r',end = '')
        elif (oldTerminalWidth > terminalWidth):
            oldTerminalWidth = terminalWidth
            print('\033[2K\033[1G\033[F\033[2K\033[1G',end='',flush=True)
        neededWhiteSpace = terminalWidth - (len(progressString) + len(f'Speed:{terminalWidth}'))
        wordSize = len(word)
        speed = (wordSize*0.0165) * speedVar
        print(f'\r{progressString}{newWord.center(neededWhiteSpace -1 , " " )}Speed:{speedVar}', end='')
        time.sleep(0.1 + speed)

def splitUltilString(strIn) -> str:
    if(strIn == ''): 
        return
    if(isinstance(strIn, str)):
        temp = strIn.strip()
        if temp != '':
            res = re.split('[\s\n\t]+', temp)
            return res
        return
    else:
        res = []
        for string in strIn:
            if string != '':
                res.extend(splitUltilString(string))
        return res

def main():
    
    global speedVar
    speedVar = 1
    
    fin = input("Name of file in the folder /input \n => ")
    
    dirname = os.path.dirname(__file__)
    myFile = os.path.join(dirname, f'../input/{fin}')
    with open(myFile, 'r', encoding="utf-8") as inputFile:
        buffer = inputFile.read()
        
        res = splitUltilString(buffer)
        printToTerminal(res, fin)
    
    # test1 = "this is a \ntest for a \tstring"
    # test2 = ["testing","for","an","array","of","strings with some variance             ","\t\\t \c\r","123\n321"]
    # test3 = {"this is a","map","""
    #         this is testing for a multi line paragraph
    #         within the paragraph may or may "not" be tabs and shit
    #             hello. \t provably want to trim these     
            
    #         with multiz
            
    #         asdfasdfasdfasdfasdfasdfsadfsadfsadfasdfdsafasdf
    #         """}
    # arrayOfTests = [test1, test2, test3]
    # for tests in arrayOfTests:
    #     res = splitUltilString(tests)
    #     length = len(res)
    #     count = 0
    #     for word in res:
    #         count = count + 1
    #         speed = (len(word)*0.01) * var
    #         print(f'\r{count}/{length}\t> {word.center(10," ")} <',end='')
    #         time.sleep(0.1 + speed)
    #     print()
        
if __name__ == '__main__':
    main()