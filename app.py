from credentials import TOKEN,URL
from book import getBooks,BookData,isAvailable
from flask import Flask, request
from telepot.loop import OrderedWebhook
from telepot.namedtuple import InlineKeyboardMarkup,InlineKeyboardButton
import telepot
import csv

app = Flask(__name__)
bot = telepot.Bot(TOKEN)

def searchFunction(chat_id : str, text: str) -> None:
    title,author,image_url = BookData(text)
    if title == None:
        bot.sendMessage(chat_id,"No results found. Please check the spelling and try again.")
    else:
        bot.sendPhoto(chat_id,image_url,caption=f"Getting results for *{title}* by _{author}_",parse_mode='Markdown')
        books = getBooks(title,author)
        library = getLibrary(chat_id)
        if len(books) == 0:
            bot.sendMessage(chat_id,f"No results were found :(",parse_mode='Markdown')
        else:
            available = isAvailable(books[0][2],library)
            if available:
                message = f"{books[0][0]} by {books[0][1]} is available at {library} ✅"
            else:
                message = f"{books[0][0]} by {books[0][1]} is not available at {library} ❌"
            bot.sendMessage(chat_id,message)

def removeCache(chat_id : str) -> None:
    rows = []
    with open('cache.csv','r') as f:
        Reader = csv.reader(f)
        for row in Reader:
            if row[0] != str(chat_id):
                rows.append(row)
    with open('cache.csv','w') as f:
        Writer = csv.writer(f)
        Writer.writerows(rows)

def addCache(chat_id : str,cache : str) -> None:
    removeCache(chat_id)
    with open('cache.csv','a') as f:
        Writer = csv.writer(f)
        Writer.writerow([chat_id,cache])

def getCache(chat_id : str,remove_cache=True) -> str:
    with open('cache.csv','r') as f:
        Reader = csv.reader(f)
        for row in Reader:
            if row[0] == str(chat_id):
                if remove_cache: removeCache(chat_id)
                return row[1]

def getLibrary(chat_id : str) -> str:
    # TODO with db
    return 'Sengkang Public Library'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text = msg['text']
        if text[0] == '/':
            if '/start' in text:
                bot.sendMessage(chat_id,"Welcome to _Library Bot_!\nGet availability of any book in NLB!📖\n",parse_mode='Markdown')
            elif '/help' in text:
                bot.sendMessage(chat_id,"Simply send the name of a book to check if it's available at your library\nUse /options to select your library")
            elif '/options' in text:
                # TODO set default library
                bot.sendMessage(chat_id, "Sorry.. this feature has not been implemented yet.\nDefaults to Sengkang Public Library")
                # keyboard = []
                # bot.sendMessage(chat_id,"Choose your default library",reply_markup=keyboard)
            elif '/search' in text:
                bot.sendMessage(chat_id,"What's the name of the book?")
                addCache(chat_id,'search')
            else:
                bot.sendMessage(chat_id,"Sorry. I don't recogonize this command yet.")
        else:
            cache = getCache(chat_id)
            if cache:
                if cache == 'search':
                    searchFunction(chat_id,text)
            else:
                # bot.sendMessage(chat_id,"Sorry... I didn't get that. Maybe you meant to use a command?")
                searchFunction(chat_id,text) # Defaults to search if no command is used
    else:
        bot.sendMessage(chat_id, "Sorry, I don't support this type of file yet. :(")

@app.route('/webhook_path', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

bot.setWebhook(URL)
webhook = OrderedWebhook(bot, handle)
webhook.run_as_thread()

if __name__ == "__main__":
    app.run()