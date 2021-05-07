import json
import os

INDEX_PATH = ".idx/"
INDEX_EXTENSION = "idx"
ACCEPTED_EXTENSIONS = ["jpg", "png", "gif", "jpeg",
                       "mp3", "ogg", "wmc", "mp4", "mkv", "avi"]


def addIndex(params):
    if params[0] == ".":
        listDir = os.listdir()
        if (INDEX_PATH[:-1] not in listDir):
            os.mkdir(INDEX_PATH)

        for path in listDir:
            if (path[-3:] in ACCEPTED_EXTENSIONS):
                os.startfile(path)
                jsonMap = {"tags": [], "relationships": []}
                while True:
                    print("Insira uma tag para '" + path +
                          "'. ('ignore' para ignorar esse arquivo, 'stop' para parar)")
                    tag = input(">>> ")
                    if (tag == "ignore"):
                        file = open(".idxignore", "a+")
                        file.write(path+"\n")
                        file.close
                        break
                    elif (tag == "stop"):
                        break
                    else:
                        jsonMap["tags"].append(tag)

                file = open(INDEX_PATH + path + INDEX_EXTENSION, "a+")
                file.write("\n"+json.dumps(jsonMap))
                file.close()
                input("Próximo arquivo?")
    else:
        print("Indexação por diretório ainda não implementada.")


class FileInfo:
    def __init__(self, name_path):
        self.name_path = name_path
        self.tags = []

    def toString(self):
        return "--\n" + self.name_path + "\n" + str(self.tags) + "\n--"

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

# TODO - Implementar busca!


def searchTerms(params):
    listFileInfo = _internalSearch(None)
    print(listFileInfo)


def _internalSearch(path):
    internalList = []
    listDirs = os.listdir(path)

    for inDir in listDirs:
        if (inDir == INDEX_PATH[:-1]):
            if path == None:
                internalList = _readIdxFolder(inDir)
            else:
                internalList = _readIdxFolder(path + "/" + inDir)
        elif (os.path.isdir(inDir)):
            if path == None:
                internalList = internalList + _internalSearch(inDir)
            else:
                internalList = internalList + \
                    _internalSearch(path + "/" + inDir)

    return internalList


def _readIdxFolder(path):
    internalList = []
    listDirs = os.listdir(path)
    for inDir in listDirs:
        if (inDir[-3:] == INDEX_EXTENSION):
            file = open(path + "/" + inDir, "r")
            lines = file.readlines()
            file.close()

            fileInfo = FileInfo(path + "/" + inDir)

            for line in lines:
                if line != "\n":
                    mapData = json.loads(line)
                    fileInfo.tags += mapData["tags"]

            internalList.append(fileInfo)
    return internalList


def main():
    while True:
        rootCMD = input(">>> ")
        listCMD = rootCMD.split()

        if(len(listCMD) < 2):
            print("Esse comando é muito pequeno.")
        else:
            mainCMD = listCMD[0]
            cmd = listCMD[1]
            params = listCMD[2:]

            if (mainCMD == "idx"):

                if (cmd == "add"):
                    addIndex(params)
                elif (cmd == "search"):
                    searchTerms(params)
                else:
                    print("O subcomando '" + cmd + "' é inválido.")
            elif (mainCMD in ["exit", "quit"]):
                input("Programa encerrado.")
                break
            else:
                print("O comando '" + mainCMD + "' é inválido.")


if __name__ == '__main__':
    main()
