# newsbot
a python3 program that reads RSS news feeds and blends them with works of fiction to create free-form poetry, sent to specified email recipient(s). newsbot is live at [thepoetrybot.com](http://www.thepoetrybot.com) where you can also subscribe to a free news-poem newsletter.

## required modules
the following modules are required:
* feedparser
* bs4
* markovify

## set-up
if you want to send the newsbot-output via mail, you need to add your email address and password in the `mailconfig.txt` file in the specified lines.

## how it works
newsbot consists of three parts: RSS parsing, poem generation, and sending of the result(s).
1. parse RSS
* get RSS headlines from web (via feedparser)
* clean news texts (remove html tags and odd symbols via BeautifulSoup)
2. create poem
* create markov-model based on news-text (via markovify)
* read pre-created JSON-model of fiction texts
* combine the two models with custom weight factor
3. send poem
* get email-metainformation (recipient, formatting, etc.) from user
* send poem email with informative header via a Gmail account (via smtplib and email)
  
## advanced usage
### custom text generation models
in its present configuration, newsbot only uses four pre-configured JSON-models for the fiction part of the poem generation. to add different flavors to the output, new JSON models can be created with the supplied class `JsonModule` from the file `jsonModule.py`.
### other RSS source feeds
change the variable `url` (line 12 in `newsbot.py`) to any RSS source you want to use for poem generation.
### different weight fiction vs RSS text
change the variable `fictionWeightFactor` (line 16 in `newsbot.py`) to any positive rational number. for numbers higher than 1, the chosen fiction text gets more weight; for numbers lower than 1, the news text is more dominant. this variable acts as multiplicator for the output of the function `autoWeightFactor`, which balances the text bodies of fiction and news texts by default equally.
