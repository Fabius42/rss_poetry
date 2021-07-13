# === RSS_POETRY POEM CREATION ===

# This file contains the Poem class that creates poems out of RSS texts
# and different fiction texts with the module Markovify. The recursive
# breakLine function fits the arbitrary-length lines of the generated
# poems to the layout requirements of the resulting image dimensions.

import markovify
import random
import time
from modules.create_img import make_image, save_image, show_image

# Initialize local time
LOCALTIME = time.localtime(time.time())


# Function readJsonModel(modelChoice)
# Reads pre-created JSON-model based on user-choice
#   0 = Vanilla (no fiction, only news)
#   1 = Dystopic (1984, Brave New World, Neuromancer)
#   2 = Intellectual (Ulysses, Naked Lunch)
#   3 = Abrahamic (Tora, Bible, Coran)
#   4 = Erotic (Memoirs of Fanny Hill, 120 Days of Sodom, Tropical Cancer)
# Input: int modelChoice(0-4) indicating desired model
# Output: markov-model-object
def readJsonModel(modelChoice):
    if int(modelChoice) == 1:  # Vanilla
        pass
    if int(modelChoice) == 2:  # Dystopic
        return readFile("models/dystopic-model.json")
    if int(modelChoice) == 3:  # Intellectual
        return readFile("models/intellectual-model.json")
    if int(modelChoice) == 4:  # Abrahamic
        return readFile("models/abrahamic-model.json")
    if int(modelChoice) == 5:  # Erotic
        return readFile("models/erotic-model.json")


# Function makeModel(inputText)
# Creates markov-model-object based on text
# Input: str inputText
# Output: markov-model-object
def makeModel(inputText):
    markovModel = markovify.Text(inputText, state_size=2)
    return markovModel


# Function makeModelFromJson(modelChoice)
# Creates markov-model-object based on preprocessed json-model
# Input: int modelChoice
# Output: markov-model-object
def makeModelFromJson(modelChoice):
    markovModel = markovify.Text.from_json(readJsonModel(modelChoice))
    return markovModel


# Function combineModels(model1, model2, weightFactor1, weightFactor2)
# Combines two markov models with custom weight factors
# Input: 2 markov-model-objects, 2 weight factor ints
# Output: markov-model-object
def combineModels(model1, model2, weightFactor1, weightFactor2):
    modelCombo = markovify.combine([model1, model2], [weightFactor1, weightFactor2])
    return modelCombo


# Function autoWeightFactor
# Computes equal weight factor for models based on their str size
# This is necessary to balance the markovify algorithm between
# the big volume of the fiction texts and the small amount of news text
# Input: int modelChoice, str newsText
# Output: int weightRatio
def autoWeightFactor(modelChoice, newsText):
    if modelChoice in range(2, 6):
        fictionModelSize = len(readJsonModel(modelChoice))
    else:  # Vanilla option
        fictionModelSize = len(newsText)
    newsModelSize = len(newsText)
    weightRatio = round(int(fictionModelSize) / int(newsModelSize))
    return weightRatio


# Function readFile
# Reads text file line by line
# Input: str inputFile name
# Output: str text
def readFile(inputFile):
    fileIn = open(inputFile, "r", encoding="utf-8")
    text = ""
    for line in fileIn:
        text += line
    return text


# Function breakLine
# Breaks up a line into segments that are shorter than a given char count
# Input: str line consisting of words and spaces
# Output: str short_lines holding shortened lines separated by newlines
def breakLine(line, max_length):

    # Initialize variables
    short_line = ""
    remainder = ""
    char_counter = 0
    short_lines = ""

    # Break up the line into a short line, and a remainder
    word_list = line.split(" ")
    for word in word_list:
        char_counter += len(word)
        # Before adding a word, check whether the line would get too long
        if char_counter <= max_length:
            short_line += word
            short_line += " "
            char_counter += 1 # account for white space
        else:
            # Otherwise, add the word to the remainder portion
            remainder += word
            remainder += " "
    short_lines += short_line + "\n"

    # If the remainder is still too long, break it down recursively
    if len(remainder) > max_length:
        remainderLines = breakLine(remainder, max_length)
        short_lines += breakLine(remainder, max_length)
    # Otherwise, if the remainder is less than the maximum length, just add it
    else:
        short_lines += remainder + "\n"

    return short_lines
    

# Class Poem
# Creates unique poem object based on markov model(s) and weight factor(s)
# Attributes:
# - Two model objects (json files containing markov associations)
# - Two int weight-factors (determine how much of each model influences the poem)
# - int modelChoice (which model 0-4 the user chose)
# - str poemHeader (the headline of the poem)
# - str poemText (the body of the poem)
# - str creationTime (the time when the poem was created)
class Poem(object):
    def __init__(self, modelObject1, modelObject2, modelChoice, 
                fictionWeightFactor, newsWeightFactor):
        self.__modelObject1 = modelObject1
        self.__modelObject2 = modelObject2
        self.__fictionWeightFactor = fictionWeightFactor
        self.__newsWeightFactor = newsWeightFactor
        self.__poemHeader = self.makePoemHeader()
        self.__poemText = self.makePoemText()
        self.__poemImage = self.make_poem_image()
        self.__modelChoice = modelChoice


    # Method makePoemText
    # Creates poem text with varying length based on models and weights
    def makePoemText(self):
        comboModel = combineModels(self.__modelObject1, self.__modelObject2,
                                   self.__fictionWeightFactor, self.__newsWeightFactor)

        # Make poem text with varying length (3-5 units)
        poemLength = random.randrange(3, 6)
        poemText = ""
        for i in range(poemLength):
            createdText = comboModel.make_short_sentence(80)
            # Checking for AttributeError
            while createdText is None:
                createdText = comboModel.make_sentence()
            poemText += createdText
        # Introduce line breaks depending on punctuation
        # This replaces commas and dots with newlines, and reduces two newlines to one
        poemText = poemText.replace(",", "\n").replace(".", "\n").replace("\n\n", "\n")
        poemText.replace("\n\n", "\n")
        
        # Break up lines that are too long
        MAX_LINE_LENGTH = 35
        poemLineList = poemText.split("\n")
        formattedPoemText = ""
        for line in poemLineList:
            # If a line is longer than the maximum length, break it up recursively
            if len(line) > MAX_LINE_LENGTH:
                formattedPoemText += breakLine(line, MAX_LINE_LENGTH) + "\n"
            # If a line is short, just keep it
            else:
                formattedPoemText += line + "\n"

        # Poems have a maximum length of 10 lines because of visual layouting
        # Therefore, throw away all lines that go beyond that
        formattedPoemText = formattedPoemText.split("\n")
        if len(formattedPoemText) > 10:
            formattedPoemText = formattedPoemText[:10]
        formattedPoemText = "\n".join(formattedPoemText)
        formattedPoemText += "\n"

        # Add current date
        formattedPoemText += "\ncreated " + str(LOCALTIME[0]) + "-" + str(LOCALTIME[1]) + "-" + str(LOCALTIME[2])

        return formattedPoemText


    # Method makePoemHeader
    # Creates poem header with varying length based on models and weights
    def makePoemHeader(self):
        comboModel = combineModels(self.__modelObject1, self.__modelObject2,
                                   self.__fictionWeightFactor, self.__newsWeightFactor)
        # Make poem header
        headerText = ""
        for i in range(5):  # Creates big amount of text to avoid IndexError
            createdHeader = comboModel.make_sentence()
            # Checking for AttributeError
            while createdHeader is None:
                createdHeader = comboModel.make_sentence()
            headerText += createdHeader
        # Randomly vary header length (2-6 words)
        headerText = headerText.replace(",", "").replace(".", "")
        listOfHeaderWords = headerText.split()
        poemHeader = ""
        headerLength = random.randrange(2, 7)
        for i in range(headerLength):
            # Keep length of poem header at maximum 25 characters for layout reasons
            if (len(poemHeader) + len(listOfHeaderWords[i])) <= 25:
                poemHeader += listOfHeaderWords[i] + " "
        return poemHeader
    

    # Method __str__
    # Prints formatted poem containing header, text and creation time
    def __str__(self):
        # Underscoring poem header
        poemHeader = self.__poemHeader
        underscore = ""
        for char in poemHeader:
            underscore += "-"
        poemHeader = poemHeader + "\n" + underscore + "\n"
        # Adding poem text below the header
        formattedPoem = "\n" + poemHeader + "\n" + self.__poemText + "\n"
        return formattedPoem


    # Method save
    # Saves poem jpg image to specified location
    def save(self, save_path):
        save_image(self.__poemImage, save_path)


    # Method make_poem_image
    # Creates poem image
    def make_poem_image(self):
        img = make_image(self.__poemHeader, self.__poemText)
        return img


    # Method show_poem_image
    # Shows poem image to user
    def show_poem_image(self):
        show_image(self.__poemImage)


    # Method getCreationTime
    # Returns poem creation time
    def getCreationTime(self):
        return self.__creationTime

