import re
import os


class fileLoader():

    _hasBookMark = False

    def __init__(self, *args):
        self.inString, self.fileName = self.__getFileToRead()
        assert self.inString is not None
        self.bookMarkIndex, self._hasBookMark = self.__searchForBookmarks(self.inString)

    def __splitUtilString(self, strIn:str|list[str]) -> list[str] | str | None:
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
                    temp = self.__splitUtilString(string)
                    assert temp is not None
                    res.extend(temp)
            return res


    def __getFileToRead(self) -> tuple[ list[str] | str | None,  str]:
        self.fileName = input("Name of file in the folder /input \n => ")
        dirName = os.path.dirname(__file__)
        myFile:str = os.path.join(dirName, f'../input/{self.fileName}')

        try:
            with open(myFile, 'r', encoding="utf-8") as inputFile:
                buffer = inputFile.read()
                fileContents = self.__splitUtilString(buffer)
            return fileContents, self.fileName
        except FileNotFoundError: 
            print(f"Failed to find file {self.fileName} in dir /input")
            return self.__getFileToRead()

    def __searchForBookmarks(self, fileContents:list[str] | str) -> tuple[int, bool]:
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

    def _insertBookmark(self, count:int) -> None:
        self._hasBookMark
        dirName = os.path.dirname(__file__)
        myFile:str = os.path.join(dirName, f'../input/{self.fileName}')
        try:
            with open(myFile, 'a+', encoding="utf-8") as inputFile:
                if self._hasBookMark:
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