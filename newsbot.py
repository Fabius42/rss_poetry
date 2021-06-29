# === NEWSBOT MAIN PROGRAM ===

import time

from modules.process_rss import getRSS, cleanText
from modules.create_poem import makeModel, makeModelFromJson, autoWeightFactor, Poem

# === INPUT VARIABLES ===
# // Fill in any RSS-readable web resource //
url = "https://www.theguardian.com/world/rss"
# // Change weight factor //
# Higher (e.g. 10) -> fiction texts are more dominant
# Lower (e.g. 0.1) -> news text has more weight
fictionWeightFactor = 1


def main():
    # Retrieve rss and make a markov model out of the cleaned text
    newsText = getRSS(url)
    cleanNewsText = cleanText(newsText)
    newsModel = makeModel(cleanNewsText)

    # === USER MENU ===
    # Display welcome message
    print("Welcome to Newsbot!")
    print("This program generates a poem from today's Guardian news articles. You can select different 'moods' that the poem will be written in. These moods are based on specific books and capture the essence of those writings.")

    # Menu loop
    programActive = True
    while programActive:
        # Choose type of markov model
        modelChoice = None
        while modelChoice not in range(0, 5):  # User input error checking
            modelChoice = input("Enter number for desired poem mood:"
                                "\n\t0 = Generic (only based on news, no books taken into account)"
                                "\n\t1 = Dystopic (1984, Brave New World, Neuromancer)"
                                "\n\t2 = Intellectual (Ulysses, Naked Lunch)"
                                "\n\t3 = Abrahamic (Tanakh, Bible, Quran)"
                                "\n\t4 = Erotic (Memoirs of Fanny Hill, 120 Days of Sodom, Tropical Cancer)"
                                "\n>")
            try:
                modelChoice = int(modelChoice)
            except ValueError:
                continue

        # Generate unique markov model and blend it with current news
        print("\nGenerating poem with chosen mood...")
        if modelChoice == 0:  # The generic option means that no book texts are taken into account
            fictionModel = newsModel
        else:  # In all other cases (1-4) the news model is blended with a fiction model
            fictionModel = makeModelFromJson(modelChoice)

        # Generate custom number of poems
        numPoems = 1
        for i in range(numPoems):
            # Create poem
            p = Poem(fictionModel, newsModel, modelChoice, fictionWeightFactor,
                     newsWeightFactor=autoWeightFactor(modelChoice, cleanNewsText))
            # print poem to console
            print(p.read())
            p.make_img("C://Users//fdiet\Desktop//newsbot-master//test.jpg")

            # save poem dialog
            pleaseSave = True
            while pleaseSave == True:
                saveChoice = input("Do you want to create a picture from your poem? [ y / n ]\n>")
                if saveChoice.lower() == "y":
                    saveFilename = input("\nChoose a filename to save your poem (e.g. filename.jpg)\n"
                                     "Press 'd' for the default filename 'poem.jpg':\n>")
                    if saveFilename.lower() == "d":
                        p.save("poems.jpg")
                    else:
                        p.save(saveFilename)
                pleaseSave = False

        # exit of menu loop
        pleaseContinue = input("\nDo you want to generate more poems? [y/n]\n>")
        if pleaseContinue.lower() != "y":
            programActive = False
    print("Have a good day!")


main()
