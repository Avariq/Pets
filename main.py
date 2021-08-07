import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from time import sleep
import time

app = Client("my_account")

@app.on_message(filters.command("spam", prefixes = "!") & filters.me)
async def spam(client, msg):
    target = msg.chat.id
    text = msg.text.split(" ", maxsplit = 2)
    times = int(text[1])
    to_spam = text[2]

    delete_id = msg.message_id

    await app.delete_messages(target, delete_id)

    for i in range(times):
        try:
            await app.send_message(target, to_spam)
        except FloodWait as e:
            time.sleep(e.x)
    print("Done")

@app.on_message(filters.command("mention", prefixes = "!") & filters.me)
def mention(_, msg):
    target = msg.chat.id
    members = []
    i = 0

    for messagee in app.iter_history(chat_id=target, limit=1):
        messagee.delete()

    for member in app.iter_chat_members(target):
        if i == 5:
            app.send_message(target, members)
            members.clear()
            i = 0
        if member.user.mention.__contains__("conqista"):
            pass
        else:
            members.append(member.user.mention("entity"))
        i += 1
    if len(members) > 0:
        app.send_message(target, members)

@app.on_message(filters.command("type", prefixes="!") & filters.me)
def type(client, msg):
    orig_text = msg.text.split("!type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "▒"
    i = 0

    while (tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.015)  # 50 ms
            tbp = tbp + text[i]
            i += 1

            msg.edit(tbp)
            sleep(0.015)

        except FloodWait as e:
            sleep(e.x)

@app.on_message(filters.command("clear", prefixes="!") & filters.me)
def clear(_, msg):
    amount = 1
    target = msg.chat.id
    text_or = msg.text.split(" ", maxsplit=1)
    if " " in msg.text:
        amount = text_or[1]
        amount = int(amount)

    amount += 1

    for message in app.iter_history(chat_id=target, limit=amount):
        message.delete()

@app.on_message(filters.command("get_edge", prefixes="!") & filters.me)
def get_edge(_, msg):
    target = msg.chat.id
    count = 0

    for message in app.iter_history(chat_id=target, limit=1000):
        if (message.text == "!set_edge"):
            message.delete()
            app.send_message(target, "{} deleted".format(count))
            break
        else:
            count += 1
            message.delete()

@app.on_message(filters.command("get_first", prefixes="!") & filters.me)
def get_first(_, msg):
    target = msg.chat.id
    amount = msg.text.split(" ")[1]
    amount = int(amount)

    for message in app.iter_history(chat_id=target, limit=amount, reverse=True):
        message.reply_text(".", quote=True)

@app.on_message(filters.command("reverse", prefixes = "!") & filters.me)
def reverse(_, msg):
    target = msg.chat.id
    message = str(msg.text.split(" ", maxsplit=1)[1])
    msg.delete()
    res = ""
    k = len(message) - 1
    while k > -1:
        res += message[k]
        k -= 1


    app.send_message(target, res)

translator = { "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г", "i": "ш", "o": "щ", "p": "з", "[": "х", "]": "ї",
               "a": "ф", "s": "і", "d": "в", "f": "а", "g": "п", "h": "р", "j": "о", "k": "л", "l": "д", ";": "ж", "'": "є", "z": "я",
               "x": "ч", "c": "с", "v": "м", "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю", "&": "?", " ": " "}

@app.on_message(filters.command("t", prefixes = "!") & filters.me)
def translate(_, msg):
    target = msg.chat.id
    message = ""
    res = ""
    id = ""
    msg.delete()

    for m in app.iter_history(target, limit=15):
        if m.from_user.id == msg.from_user.id:
            message = str(m.text)
            id = m.message_id
            break

    for i in message:
        res += translator[i]

    app.edit_message_text(chat_id=target, message_id=id, text=res)

@app.on_message(filters.command("roll", prefixes = "!") & filters.me)
def roll(_, msg):
    target = msg.chat.id
    message = msg.text.split(" ", maxsplit=1)[1]
    res = message
    for i in range(16):
        temp = res
        res = message + " " + str(random.randint(0, 100)) + "%"
        if res != temp:
            app.edit_message_text(chat_id=target, message_id=msg.message_id, text=res)


app.run()