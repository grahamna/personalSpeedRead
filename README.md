# personalSpeedRead

 > Dynamic Terminal via os to read utf-8 / text documents faster, such as for fanfiction or textbooks

## Dependencies

- keyboard - ( pip install keyboard )
  - using this package requires sudo in Linux

### Hotkeys

  | *key* | *function* |
  | ----------- | ----------- |
  | space | pause |
  | arrow key up | faster read speed |
  | arrow key down | slower read speed |
  | arrow keys L/R | word by word navigation
  | esc | exit [while  paused] |

## Bookmarks

  > When exiting the program, via esc or ctrl c, the program will modify the end of your input file with the index of the bookmark. This allows you to not loose progress in larger files.  
  > The special string inserted at the end of the file is "<<_BookMark_>>##", without the quotes and the ## is the index of where you are within the file.

# ToDo

  >  1. Separate current functions into classes via function outside of main.py. This will also get rid of the "global" vars and have them as class specific variables.  
  -  A class for File Reader / formatter (fileGetter)  
        -  class vars: hasBookMark, fileName  
    - splitUtilString(strIn:str|list[str]) -> list[str] | str | None:  
    - getFileToRead() -> tuple[ list[str] | str | None,  str]:  
    - searchForBookmarks(fileContents:list[str] | str) -> tuple[int, bool]:  
    - insertBookmark(fileName:str): [This is post SpeedRead, part of quitting]  
  -  A class for Actual Reader (SpeedReader)  
        - class vars: speedVar, going, count, inString[the content]  
    -  wordNav(direction:int) -> None:  
    -  speedMod(mod:float) -> None:  
    -  quitProgram(fileName:str) -> None:  
    -  printToTerminal(fileName:str) -> None:  
    -  terminalPrint(newCount:int) -> tuple[str, int]:  
    -  setKeybinds(fileName:str) -> None:  
  >  2. Clean up code and variable names  
  >  3. Possibly make a gui interface? I'm kinda happy with just the CLI...  