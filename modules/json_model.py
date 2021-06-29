# JSON-MODEL

import markovify

# === INPUT VARIABLES ===

def main():
    modelName = "custom"  # put a descriptive name here
    textList = ["text1.txt", "text2.txt", "text3.txt"]  # put the titles of txt files here

    j = JsonModel(modelName, textList)
    j.make()


# === CLASS ===

# class JsonModel
# creates a json-file based on input-text(s) and a user-given model-name
#   the class is not included in the main program, because it only needs to run once
#   (when new models are created) this is useful due to performance-reasons
#   (it is faster to read in a pre-created json-file, than to do all the
#   computation operations for every request); however, it can be used
#   to generate new custom models to explore other literary / poetic genres
# attributes:
#   textList (list of text-files in directory), str modelName
# methods:
#   textClean (cleans texts from textList)
#   make (creates json-model out of all combined texts)
class JsonModel(object):
    def __init__(self, modelName, textList):
        self.__modelName = modelName
        self.__textList = textList

    # method textClean
    # cleans text and transforms it to one-line string
    # input: str inputFile
    # output: str text to outputFile (format: inputFile_new.txt)
    def textClean(self, inputFile):
        fileIn = open(inputFile, "r", encoding="latin-1")
        cleanText = ""
        for line in fileIn:
            cleanLine = ""
            for char in line:
                if char.lower() in "abcdefghijklmnopqrstuvwxyz ',\n-.":
                    cleanLine += char
            cleanText += cleanLine
        fileIn.close()
        return cleanText

    # method makeJsonModel
    # reads text and creates JSON markov-model-object
    # input: str inputText
    # output: markov-model-object
    def make(self):
        # clean texts in text list and add them to one str
        cleanText = ""
        for textFile in self.__textList:
            cleanText += self.textClean(textFile)
        # make jsonModel out of clean texts
        markovModel = markovify.Text(cleanText)
        jsonModel = markovModel.to_json()
        # write json-model to file
        fileOut = open(("../models/" + self.__modelName + "-model.json"), mode="w")
        print(jsonModel, file=fileOut)
        fileOut.close()


main()
