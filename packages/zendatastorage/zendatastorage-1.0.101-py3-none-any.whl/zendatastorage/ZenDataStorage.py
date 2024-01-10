import os
import sys
from colorama import Fore

vardict: dict = {}

hello: str = "Hello, World!"
# Symbols
EndLineSymbol: chr = ";"
Equal: chr = "="
VarNameDefinerStart: chr = "["
VarNameDefinerEnd: chr = "]"
TextEncapsulator: chr = '"'

class Error:
    def __init__(self, message: str):
        self.message = message
    def __str__(self):
        return f"Error: {self.message}"

def MergeIntoDict(keys: list[str], values: list[any]):
    keyslist: list[str] = []
    valueslist: list[any] = []
    ReturnedDict: dict = {}
    for key in keys:
        keyslist.append(key)
    for value in values:
        valueslist.append(value)
    for key in keys:
        ReturnedDict[key] = valueslist[keyslist.index(key)]
    return ReturnedDict
def Interpret(file: str):
    # Line Num
    LineNumber: int = 0
    #Main Line Checking
    for line in file:
        LineNumber += 1
        #Error Checking
        if "[" not in line and "]" in line:
            print(Fore.RED + str(Error(f"Missing '[' on line {LineNumber}")) + Fore.RESET)
            break
        if "]" not in line and "[" in line:
            print(Fore.RED + str(Error(f"Missing ']' on line {LineNumber}")) + Fore.RESET)
            break
        if "]" not in line and "[" not in line:
            print(Fore.RED + str(Error(f"Missing '[' and ']' on line {LineNumber}")) + Fore.RESET)
            break
        # Main Program
        if "[" in line:
            start_index = line.find(VarNameDefinerStart) + 1
            end_index = line.rfind(VarNameDefinerEnd)
            body = line[start_index:end_index]
            body = body.strip()
            if '"' in body:
                start_index = body.find(TextEncapsulator) + 1
                end_index = body.rfind(TextEncapsulator)
                body = body[start_index:end_index]
                body = body.strip()
            start_index = line.find(Equal) + 1
            end_index = line.rfind(EndLineSymbol)
            content = line[start_index:end_index].strip()
            if "{" in line:
                start_index = line.find("{") + 1
                end_index = line.rfind("}")
                CurlyContent = line[start_index:end_index].strip()
                if "list(" in CurlyContent:
                    start_index = CurlyContent.find("list(") + 5
                    end_index = CurlyContent.rfind(")")
                    listcontent = CurlyContent[start_index:end_index].strip()
                    listcontentList: list[str] = listcontent.split(",")
                    listcontentList = [x.strip() for x in listcontentList]
                    content = listcontentList
                if "loadlist(" in CurlyContent:
                    start_index = CurlyContent.find("loadlist(") + 9
                    end_index = CurlyContent.rfind(")")
                    ListFileName = CurlyContent[start_index:end_index].replace(" ", "").strip()
                    with open(ListFileName, "r") as f:
                        contentOfListFile = f.read()
                        listcontent = contentOfListFile.replace("\n", "").strip()
                        listcontentList: list[str] = listcontent.split(",")
                        listcontentList = [x.strip() for x in listcontentList]
                        content = listcontentList
                #if "loaddict(" in CurlyContent:
                    #start_index = CurlyContent.find("loaddict(") + 9
                    #end_index = CurlyContent.rfind(")")
                    #DictFileName = CurlyContent[start_index:end_index].replace(" ", "").strip()
                    #with open(DictFileName, "r") as f:
                        #contentOfDictFile = f.read()
                        #listcontent = contentOfDictFile.replace("\n", "").strip()
                        #listcontentList: list[str] = listcontent.split(",")
                        #listcontentList = [x.strip() for x in listcontentList]
                        #listcontentDict: dict = {}
                        #for item in listcontentList:
                            #key, value = item.split(":")
                            #listcontentDict[key] = value
                        #for key in listcontentDict:
                            #if key is str:
                                #key = key.strip()
                            #if listcontentDict[key] is str:
                                #listcontentDict[key] = listcontentDict[key].strip()
                        #content = dict(listcontentDict)

            #Assign value to dict
            vardict[body] = content
    return vardict

testfile = os.getcwd() + "\\ZenDataStorage\\" + "test.zenf"
if __name__ == "__main__":
    with open(testfile, "r") as f:
        newvardict = Interpret(f)
        NewMergedDict = MergeIntoDict(newvardict["PlayerStatsNames"], newvardict["PlayerStatsValues"])
        print(NewMergedDict)