# Library Bot

[Library Bot](https://t.me/Library13Bot) is a Telegram Bot that allows you to check the availability of _any_ book in _any_ NLB library!
  - Type _/help_ for help on how to use it
  - Type _/start_ for info on the bot

## Get Started

To get started, **clone this repo**
```
$ git clone git://github.com/soimort/you-get.git
```
Navigate into the directory and install the requirements
```
$ cd LibraryBot
$ pip3 install -r requirements.txt
```
Create a blank cache.csv and credentials.py file
```
$ touch cache.csv
$ touch credentials.py
```
Add to the credentials.py file in the following format
```python3
TOKEN = '<your telegram token>'
URL = '<your webhook path>'
GOODREADS_KEY = '<your goodreads api key>'
```
That's it! Start the server
```
$ flask run
```

## Features

  - Send the name of any book to it and it will tell you if it is available in your library

## Todos:

  - Type _/options_ to set your library via Inline Buttons
  - Check a list of books at once
