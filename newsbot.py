# === NEWSBOT MAIN PROGRAM ===

import time

from modules.process_rss import getRSS, cleanText
from modules.create_poem import makeModel, makeModelFromJson, autoWeightFactor, Poem


# // Change weight factor //
# Higher (e.g. 10) -> fiction texts are more dominant
# Lower (e.g. 0.1) -> news text has more weight
fictionWeightFactor = 1


def main():
    # === USER MENU ===

    # Display welcome message
    print("Welcome to rss_poetry!")
    print("This program generates a poem from today's news articles or another custom RSS source. You can select different 'moods' that the poem will be written in. These moods are based on specific books and capture the essence of those writings.")

    # Let user choose between different newspaper URLs or their own RSS URL
    url_choice = input("Select RSS text source:"
                        "\n\t1 = Guardian"
                        "\n\t2 = New York Times"
                        "\n\t3 = BBC"
                        "\n\t4 = LA Times"
                        "\n\t5 = Custom (Enter your own RSS url)"
                        "\n>")
    if url_choice == "2":
        url = "https://feeds.simplecast.com/54nAGcIl" # NY Times
    elif url_choice == "3":
        url = "https://feeds.bbci.co.uk/news/world/rss.xml" # BBC
    elif url_choice == "4":
        url = "https://www.latimes.com/world/rss2.0.xml" # LA Times

    # Custom user URL
    elif url_choice == "5":
        url = input("Please enter your custom URL of a RSS source:\n>")
        url_is_valid = test_url(url)
        # Error checking
        while url_is_valid == False:
            print("rss_poetry can't find RSS text at the provided URL.\n")
            url = input("Please enter your custom URL of a RSS source:\n>")
            url_is_valid = test_url(url)
        print("Valid URL found.")

    # Default catch-all case "1" and if user mistyped / just pressed "enter"
    else:
        url = "https://www.theguardian.com/world/rss" # Guardian


    # Retrieve rss and make a markov model out of the cleaned text
    newsText = getRSS(url)
    cleanNewsText = cleanText(newsText)
    newsModel = makeModel(cleanNewsText)


    # Menu loop allows to repeatedly generate poems
    programActive = True
    while programActive:
        # Choose type of markov model
        modelChoice = None
        while modelChoice not in range(1, 6):  # User input error checking
            modelChoice = input("Select desired poem mood:"
                                "\n\t1 = Generic (only based on news, no books taken into account)"
                                "\n\t2 = Dystopic (1984, Brave New World, Neuromancer)"
                                "\n\t3 = Intellectual (Ulysses, Naked Lunch)"
                                "\n\t4 = Abrahamic (Tanakh, Bible, Quran)"
                                "\n\t5 = Erotic (Memoirs of Fanny Hill, 120 Days of Sodom, Tropical Cancer)"
                                "\n>")
            try:
                modelChoice = int(modelChoice)
            except ValueError:
                continue

        # Generate unique markov model and blend it with current news
        print("\nGenerating poem with chosen mood...")
        if modelChoice == 1:  # The generic option means that no book texts are taken into account
            fictionModel = newsModel
        else:  # In all other cases (1-4) the news model is blended with a fiction model
            fictionModel = makeModelFromJson(modelChoice)

        # Generate custom number of poems
        NUM_POEMS = 1
        for i in range(NUM_POEMS):
            # Create poem
            p = Poem(fictionModel, newsModel, modelChoice, fictionWeightFactor,
                     newsWeightFactor=autoWeightFactor(modelChoice, cleanNewsText))
            # Print poem to console and show the image
            print(p)
            p.show_poem_image()

            # Image save dialog
            pleaseSave = True
            while pleaseSave == True:
                save_image_choice = input("Do you want to save your poem picture? (press 'y' or 'n')\n>")
                if save_image_choice.lower() == "y":
                    save_filename = input("\nChoose a filename to save your poem (e.g. filename.jpg)\n"
                                     "Press 'd' for the default filename 'poem.jpg':\n>")
                    if save_filename.lower() == "d":
                        p.save("saved-images/poems.jpg")
                        print("Poem saved as 'poem.jpg' in folder /saved-images")
                    else:
                        p.save("saved-images/" + save_filename)
                        print("Poem saved as '" + save_filename + "' in folder '/saved-images'")
                pleaseSave = False

        # Exit of menu loop
        pleaseContinue = input("\nDo you want to generate more poems? (press 'y' or 'n')\n>")
        if pleaseContinue.lower() != "y":
            programActive = False
    print("\nThanks for using rss_poetry!\n(written by Fabian Dietrich in 2019)")



# Function test_url
# Tests for a given URL whether a markov model
# can be made from RSS text
# Input: URL
# Output: Boolean
def test_url(url):
    try:
        newsText = getRSS(url)
        cleanNewsText = cleanText(newsText)
        newsModel = makeModel(cleanNewsText)
        return True
    except:
        return False


main()
