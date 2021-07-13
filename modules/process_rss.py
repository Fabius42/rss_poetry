# === RSS_POETRY RSS TEXT PROCESSING ===

# This file contains the functions to retrieve RSS text with the module
# Feedparser, and clean the internet text with the module BeautifulSoup.

import feedparser
from bs4 import BeautifulSoup

# function getRSS(url)
# reads rss-text from a specified url
# input: str url
# output: str article headers
def getRSS(url):
    feed = feedparser.parse(url)
    rssText = ""
    for entry in feed.entries:
        articleTitle = entry.title
        articleContent = entry.summary
        rssText += (articleTitle + "\n" + articleContent + "\n\n")
    return rssText

# function cleanText(dirtyText)
# removes unwanted html elements, expressions and characters from text
# input: str of unclean text
# output: str of clean text
def cleanText(dirtyText):
    # remove html elements
    soup = BeautifulSoup(dirtyText, features="html.parser")
    text = soup.get_text()
    # remove continue reading expression
    text2 = text.replace('Continue reading...', '')
    # remove special characters
    cleanOutput = ""
    for line in text2:
        cleanLine = ""
        for char in line:
            if char.isalnum() or char in " \n,-.":
                cleanLine += char
        cleanOutput += cleanLine
    return cleanOutput
