import os

import FileLoader
import SpeedReader


def main() -> None:
    
    fileLoader = FileLoader.fileLoader()

    if (fileLoader.inString is not None):
        speedRead = SpeedReader.speedReader(fileLoader.inString, fileLoader.fileName, fileLoader.bookMarkIndex, fileLoader)

        try:
            speedRead.printToTerminal()
        except KeyboardInterrupt:
            print("\nExiting via KeyboardInterrupt")
            fileLoader._insertBookmark(speedRead.count)
            os._exit(1)
    else:
        print(f"File {fileLoader.fileName} is empty, exiting")


if __name__ == '__main__':
    main()