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
        print(result)
        page = wikipedia.page(result[0])
        wikitext = page.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        print(e)
        return 'Нет Информации'


@bot.message_handler(commands=["start", "help"])
def start(message):
    global userInput
    if not userInput:
        bot.send_message(message.chat.id,
                         "Привет!\n- /artist получить информацию об артисте\n- /song получить информацию о песне")


@bot.message_handler(commands=["artist"])
def artist(message):
    global userInput
    if not userInput:
        userInput = True
        bot.send_message(message.chat.id, "Введите имя артиста или напишите \'/done\' для выхода")


@bot.message_handler(commands=["song"])
def song(message):
    global userInput
    if not userInput:
        userInput = True
        bot.send_message(message.chat.id, "Введите имя песни или напишите \'/done\' для выхода")


@bot.message_handler(commands=["done"])
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
