import telebot
import wikipedia
import re
import constants

userInput = False
bot = telebot.TeleBot(constants.API_KEY)
wikipedia.set_lang("ru")


def get_wiki(s):
    try:
        result = wikipedia.search(s)
        page = wikipedia.page(result[0])
        wikitext = page.content[:1000]
        return split_content(wikitext)
    except Exception as e:
        return 'Нет Информации'


def split_content(content):
    s = content.split('.')
    s = s[:-1]
    wikitext = ''
    for x in s:
        if not ('==' in x):
            if len((x.strip())) > 3:
                wikitext = wikitext + x + '.'
        else:
            break
    wikitext = re.sub('\([^()]*\)', '', wikitext)
    wikitext = re.sub('\([^()]*\)', '', wikitext)
    wikitext = re.sub('\{[^\{\}]*\}', '', wikitext)
    return wikitext


@bot.message_handler(commands=["start"])
def start(message):
    global userInput
    if not userInput:
        bot.send_message(message.chat.id,
                         "Привет!\n- /артист получить информацию об артисте\n- /песня получить информацию о песне")


@bot.message_handler(commands=["артист"])
def artist(message):
    global userInput
    if not userInput:
        userInput = True
        bot.send_message(message.chat.id, "Введите имя артиста или напишите \'/готово\' для выхода")


@bot.message_handler(commands=["песня"])
def song(message):
    global userInput
    if not userInput:
        userInput = True
        bot.send_message(message.chat.id, "Введите имя песни или напишите \'/готово\' для выхода")


@bot.message_handler(commands=["готово"])
def done(message):
    global userInput
    if userInput:
        userInput = False
        start(message)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global userInput
    if userInput:
        userInput = False
        bot.send_message(message.chat.id, get_wiki(message.text))


bot.polling(none_stop=True, interval=0)
