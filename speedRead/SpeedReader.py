import os
import time

import FileLoader

import keyboard

class speedReader():
    _speedVar =  1
    _going = False
    _initialTerminalWidth = 0
    def __init__(self, inString:str|list[str], fileName:str, bookMarkCount:int|None, fileLoader:FileLoader.fileLoader):
        if (bookMarkCount is None):
            self.count = 0
        else: self.count = bookMarkCount
        self._inString = inString
        self.fileName = fileName
        self._fileLoader = fileLoader
        self.__setKeybinds()
    
    def __wordNav(self, direction:int) -> None:
        if self._going: return
        self.count += direction
        self.__terminalPrint(self.count)

    def __speedMod(self, mod:float) -> None:
        global speedVar, going
        if mod != 0:
            self._speedVar += mod
            if (not self._going):
                self.__terminalPrint(self.count)
        else:
            self._going = not self._going

    def __quitProgram(self) -> None:
        if self._going: return
        else:
            assert self._fileLoader is not None
            self._fileLoader._insertBookmark(self.count)
            os._exit(1)

    def printToTerminal(self) -> None:

        assert self._inString is not None
        self._length = len(self._inString)

        speedText = "lower is faster"
        progressText = "current / total"
        self._initialTerminalWidth = os.get_terminal_size()[0]
        neededWhiteSpace = self._initialTerminalWidth - len(speedText) - len(progressText)
        print(f'\r{progressText}{self.fileName.center(neededWhiteSpace -1 , " " )}{speedText}')

        while self.count < self._length - 1:

            word, self.count = self.__terminalPrint(self.count)
            self.count+=1

            if (not self._going):
                self.count-=1
                keyboard.wait('space')
            
            wordSize = len(word)
            speed = (wordSize*0.0185) * self._speedVar

            if 0.1 + speed > 0:
                time.sleep(0.1 + speed)
            else:
                speed = 0.1
                self._speedVar = 0

    def __terminalPrint(self, newCount:int) -> tuple[str, int]:
            self.count = newCount
            if self.count < 0 : self.count = 0
            if self.count >= self._length: self.count = self._length -1

            assert self._inString is not None
            word = self._inString[self.count]
            progressString:str = f'{self.count + 1}/{self._length}'
            newWord:str = f"> {word} <"
            terminalWidth:int = os.get_terminal_size()[0]

            if (self._initialTerminalWidth < terminalWidth):
                self._initialTerminalWidth = terminalWidth
                print(f'\r',end = '')
            elif (self._initialTerminalWidth > terminalWidth):
                self._initialTerminalWidth = terminalWidth
                print('\033[2K\033[1G\033[F\033[2K\033[1G',end='',flush=True)

            neededWhiteSpace = terminalWidth - (len(progressString) + len(f'Speed:{self._speedVar:.2f}')) - 8
            print(f'\r{progressString}{newWord.center(neededWhiteSpace, " " )}Speed:{self._speedVar:.2f}', end='')

            return (word, self.count)

    def __setKeybinds(self) -> None:
            # setting up hotkeys, activate regardless of window focus
        keyboard.add_hotkey("LEFT", lambda: self.__wordNav(-1))
        keyboard.add_hotkey("RIGHT", lambda: self.__wordNav(1))
        keyboard.add_hotkey("DOWN", lambda: self.__speedMod(-0.05))
        keyboard.add_hotkey("UP", lambda: self.__speedMod(0.05))
        keyboard.add_hotkey("space", lambda: self.__speedMod(0))
        keyboard.add_hotkey("esc", lambda: self.__quitProgram())

        hotkeyHeader = "Hotkeys Activated:\n\t| space to play / pause | UP / DOWN arrow(s) to modify reading speed |\n\t| [while paused] LEFT / RIGHT arrow to navigate words  | esc to quit |"
        print(hotkeyHeader)