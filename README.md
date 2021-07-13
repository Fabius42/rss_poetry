# RSS_Poetry
**Create and Visualize surprising Poems by blending online news feeds with works of literature on the Command-Line**
- Choose which online news or other RSS sources to use as starting point
- Choose between different poetic "moods" (dystopic, abrahamic, intellectual, or erotic)
- Save your poem as easily-shareable 800x600px image
- Train your own markov model based on custom literature texts

<img src="https://github.com/Fabius42/rss_poetry/blob/master/saved-images/nobody-knew.jpg" width=600>

## How to Run
1. Clone the repository
2. Make sure you have the following modules installed:
	- feedparser
	- pillow
	- bs4
	- markovify
3. Run rss_poetry.py (requires Python 3)

<img src="https://github.com/Fabius42/rss_poetry/blob/master/saved-images/command-line.jpg" width=600>

## Custom Text Generation Models
There are four pre-configured JSON-models included that set different poetic "moods" because they contain different vocabulary words and phrases. If you have a selection of literary works that you are passionate about, or want to play with, you can create your own JSON-models with the class `JsonModule` in the file `json_model_.py`. Just change the variables in line 13-14 and run the file.

## Fine-tuning the Poem Generator
If you choose to blend RSS text with a fiction model (versus the "generic" option that doesn't take fiction text into account), the poem generator uses a weight to decide "how much" of each of these text sources will show in the resulting poem. Currently, the weight is set to a balanced position that creates poems that have a discernible "mood" while also making strong references to the provided RSS texts. You can change the variable `fictionWeightFactor` (line 17 in `rss_poetry.py`) to any positive rational number. For numbers higher than 1, the chosen fiction text gets more weight; for numbers lower than 1, the news text is more dominant.

<img src="https://github.com/Fabius42/rss_poetry/blob/master/saved-images/but-us.jpg" width=600>
<img src="https://github.com/Fabius42/rss_poetry/blob/master/saved-images/google-fined.jpg" width=600>
