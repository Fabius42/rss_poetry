# === RSS_POETRY JSON MODEL ===

# This file contains the class JsonModel that uses the module Markovify
# to create custom markov models. I used this file to assemble my different
# fiction text models out of several .txt files, and saved them as .json files.
# You just need to specify the two variables in the main function, and run the file.

import markovify


def main():
    # Set model name, and provide one or more text files with their paths
    modelName = "custom"
    textList = ["text1.txt", "text2.txt", "text3.txt"]
    # Create a combined markov model out of them and save it as .json
    j = JsonModel(modelName, textList)
    j.make()


# Class JsonModel
# Creates a json-file based on input-text(s) and a user-given model-name.
# The class is not included in the main program, because it only needs to run once
# (when new models are created). This is useful due to performance-reasons. This
# class can be used by advanced users to generate new custom models to explore
# other literary or poetic genres.
# Attributes:
# - list of text-file paths
# - str modelName (name of the resulting model)
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
