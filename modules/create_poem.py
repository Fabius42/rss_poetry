# === MODULE CREATE_POEM ===

import markovify
import random
import time
from modules.create_img import poem_visualization

# initialize local time
LOCALTIME = time.localtime(time.time())

# === FUNCTIONS ===

# function readFile
# reads text file line by line
# input: str inputFile name
# output: str text
def readFile(inputFile):
    fileIn = open(inputFile, "r", encoding="utf-8")
    text = ""
    for line in fileIn:
        text += line
    return text

# function readJsonModel(modelChoice)
# reads pre-created JSON-model based on user-choice
#   0 = vanilla (no fiction, only news)
#   1 = dystopic (1984, Brave New World, Neuromancer)
#   2 = intellectual (Ulysses, Naked Lunch)
#   3 = abrahamic (Tora, Bible, Coran)
#   4 = erotic (Memoirs of Fanny Hill, 120 Days of Sodom, Tropical Cancer)
# input: int modelChoice(0-4) indicating desired model
# output: markov-model-object
def readJsonModel(modelChoice):
    if int(modelChoice) == 0:  # vanilla
        pass
        # return vanillaChoice
    if int(modelChoice) == 1:  # dystopic
        return readFile("models/dystopic-model.json")
    if int(modelChoice) == 2:  # intellectual
        return readFile("models/intellectual-model.json")
    if int(modelChoice) == 3:  # abrahamic
        return readFile("models/abrahamic-model.json")
    if int(modelChoice) == 4:  # erotic
        return readFile("models/erotic-model.json")

# function makeModel(inputText)
# creates markov-model-object based on text
# input: str inputText
# output: markov-model-object
def makeModel(inputText):
    markovModel = markovify.Text(inputText, state_size=2)
    return markovModel

# function makeModelFromJson(modelChoice)
# creates markov-model-object based on preprocessed json-model
# input: int modelChoice
# output: markov-model-object
def makeModelFromJson(modelChoice):
    markovModel = markovify.Text.from_json(readJsonModel(modelChoice))
    return markovModel

# function combineModels(model1, model2, weightFactor1, weightFactor2)
# combines two markov models with custom weight factors
# input: 2 markov-model-objects, 2 weight factor ints
# output: markov-model-object
def combineModels(model1, model2, weightFactor1, weightFactor2):
    modelCombo = markovify.combine([model1, model2], [weightFactor1, weightFactor2])
    return modelCombo

# function autoWeightFactor
# computes equal weight factor for models based on their str size
# this is necessary to balance the markovify algorithm between
# the big volume of the fiction texts and the small amount of news text
# input: int modelChoice, str newsText
# output: int weightRatio
def autoWeightFactor(modelChoice, newsText):
    if modelChoice in range(1, 5):
        fictionModelSize = len(readJsonModel(modelChoice))
    else:  # vanilla option
        fictionModelSize = len(newsText)
    newsModelSize = len(newsText)
    weightRatio = round(int(fictionModelSize) / int(newsModelSize))
    return weightRatio


# === CLASS ===

# class Poem
# creates unique poem object based on model(s) and weight factor(s)
# attributes:
#   2 model-objects, 2 int weight-factor, int modelChoice, str poemHeader, str poemText, str creationTime
# methods:
#   makePoemText (creates poem text with varying length based on models and weights)
#   makePoemHeader (creates poem header with varying length based on models and weights)
#   __str__ (prints formatted poem information containing header, text and creation time)
#   save (writes poem text to csv with timestamp and indication of fiction model used)
class Poem(object):
    def __init__(self, modelObject1, modelObject2, modelChoice, fictionWeightFactor, newsWeightFactor):
        self.__modelObject1 = modelObject1
        self.__modelObject2 = modelObject2
        self.__fictionWeightFactor = fictionWeightFactor
        self.__newsWeightFactor = newsWeightFactor
        self.__poemHeader = self.makePoemHeader()
        self.__poemText = self.makePoemText()
        self.__creationTime = str(LOCALTIME[0]) + "-" + str(LOCALTIME[1]) + "-" + str(LOCALTIME[2])
        self.__modelChoice = modelChoice

    def makePoemText(self):
        comboModel = combineModels(self.__modelObject1, self.__modelObject2,
                                   self.__fictionWeightFactor, self.__newsWeightFactor)
        # random poem length (3-5 units)
        poemLength = random.randrange(3, 6)
        # make poem text with varying length and formatting
        poemText = ""
        for i in range(poemLength):
            createdText = comboModel.make_short_sentence(80)
            # checking for AttributeError
            while createdText is None:
                createdText = comboModel.make_sentence()
            poemText += createdText
        # introduces line breaks depending on punctuation
        formattedPoemText = poemText.replace(",", "\n").replace(".", "\n").replace("\n\n", "\n")
        # introduces line breaks depending on line-length
        poemLineList = formattedPoemText.split("\n")
        poemWordLineList = []
        for line in poemLineList:
            poemWordLineList.append(line.split(" "))
        formattedPoemText = ""
        for line in poemWordLineList:
            i = 0
            for word in line:
                if i > 10:  # max amount of words in any line of poem
                    word += "\n"
                    formattedPoemText += word
                else:
                    word += " "
                    formattedPoemText += word
                i += 1
            formattedPoemText += "\n"
        return formattedPoemText

    def makePoemHeader(self):
        comboModel = combineModels(self.__modelObject1, self.__modelObject2,
                                   self.__fictionWeightFactor, self.__newsWeightFactor)
        # make poem header
        headerText = ""
        for i in range(5):  # creates solid amount of text to avoid IndexError
            createdHeader = comboModel.make_sentence()
            # checking for AttributeError
            while createdHeader is None:
                createdHeader = comboModel.make_sentence()
            headerText += createdHeader
        # varying length with random (2-6 words)
        headerText = headerText.replace(",", "").replace(".", "")
        listOfHeaderWords = headerText.split()
        poemHeader = ""
        poemLength = random.randrange(2, 7)
        for i in range(poemLength):
            poemHeader += listOfHeaderWords[i] + " "
        return poemHeader

    def read(self):
        # formatting poem header
        poemHeader = self.__poemHeader
        underscore = ""
        for char in poemHeader:
            underscore += "-"
        poemHeader = poemHeader + "\n" + underscore + "\n"
        # putting poem together
        formattedPoem = "\n" + poemHeader + "\n" + self.__poemText + "\ncreated " + self.__creationTime + "\n"
        return formattedPoem

    def __str__(self):
        msg = Poem.read(self)
        return msg

    def save(self, csvFileName):
        fileOut = open(csvFileName, mode="a")
        poemCsvLine = self.__creationTime + "," + str(self.__modelChoice) + "," +\
                      self.__poemHeader + "," + self.__poemText
        poemCsvLine = repr(poemCsvLine).strip("'\"")
        print(poemCsvLine, file=fileOut)
        print("--- poem successfully saved. ---")
        fileOut.close()

    def make_img(self, save_path):
        poem_visualization(self.__poemHeader, self.__poemText, save_path)

    def getCreationTime(self):
        return self.__creationTime
