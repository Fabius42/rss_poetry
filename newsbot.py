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
    print("Welcome to FreestyleNews!")
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
        NUM_POEMS = 1
        for i in range(NUM_POEMS):
            # Create poem
            p = Poem(fictionModel, newsModel, modelChoice, fictionWeightFactor,
                     newsWeightFactor=autoWeightFactor(modelChoice, cleanNewsText))
            # Print poem to console
            print(p.read())

            #p.make_img("C://Users//fdiet//Documents//code//git//my-current-git-repos//freestylenews//test.jpg")

            # Image creation and image save dialog
            pleaseSave = True
            while pleaseSave == True:
                create_image_choice = input("Do you want to create a picture from your poem? (press 'y' or 'n')\n>")
                if create_image_choice.lower() == "y":
                    p.show_poem_image()
                    save_filename = input("\nChoose a filename to save your poem (e.g. filename.jpg)\n"
                                     "Press 'd' for the default filename 'poem.jpg':\n>")
                    if save_filename.lower() == "d":
                        p.save("saved-images/poems.jpg")
                    else:
                        p.save("saved-images/" + save_filename)
                pleaseSave = False

        # Exit of menu loop
        pleaseContinue = input("\nDo you want to generate more poems? (press 'y' or 'n')\n>")
        if pleaseContinue.lower() != "y":
            programActive = False
    print("\nFreestyleNews is sad to stop already >:(")
    print("Goodbye!")


main()
