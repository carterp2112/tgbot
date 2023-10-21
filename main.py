import logging
from telegram import ForceReply
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler
import os


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def openLink():
    f = open("linkdump.txt", "rt")
    
    dewey = list(enumerate(f))
    
    for i in range(len(dewey), 2):
        dewey[i][1] = dewey[i][1].casefold()
    return dewey

def extractLink(name):
    name = name.casefold()
    numbered_list = openLink()
    brokenQuery = []
    matches = 0
    titles = []
    links = []
    
    brokenQuery = name.split()
    for x in brokenQuery:
        if x not in ["the", "of", "a", "in", "to"]:
            continue
        else:
            brokenQuery.remove(x)
    
    print(brokenQuery)
    
    for i in range(0, len(numbered_list) - 1, 2):  
        for a in brokenQuery:
            if a in numbered_list[i][1].casefold():  
                matches += 1
        if matches > 0:
            titles.append(numbered_list[i][1])  
            links.append(numbered_list[i + 1][1])  
            matches = 0

    if titles == []:
        return "none", "found"
    else:
        return links, titles
    
def formatQuery(links, titles):  
    
    if(links == "none" and titles == "found"):
        return "Your query turned up nothing. Please refine your search and try again."
    
    query = ""
    for i in range(len(links)):
        query += titles[i] + links[i] + '\n'
        
    return "Your query turned up " + str(len(titles)) + " results:\n" + query + "If Results are too broad, try narrowing your query based off of these results."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am the Promethean Scholar, a scholar of promethean might. Please refer to '/help' for assistance with commands, or simply type your search query without a command. Join https://t.me/+RkzOB7QPj7IzM2Yx for more information on Democratic Kampuchea.")

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("https://t.me/+RkzOB7QPj7IzM2Yx\n^ The Democratic Kampuchea Telegram\nhttps://discord.gg/byARfHyKES\n^ The Democratic Kampuchea Discord")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    var1, var2 = extractLink(update.message.text)
    query = formatQuery(var1, var2)
    await update.message.reply_text(text=query)
    
async def unknown(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm sorry, I don't know that command. Please consider using\n'/help'.")
    
async def help_needed(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Here is a list of the available commands:\n1) /start - For default message.\n2) /invite - For invite to Kampuchea Servers\n3) /help - If you need assistance.\nOR\nSimply type anything into the chat and I will read it as a search query.")
   
if __name__ == '__main__':
    application = ApplicationBuilder().token('6759299864:AAEnaaMZQy2ApZDcYXRHZSk1Xs32apGO_vE').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    invite_handler = CommandHandler('invite', invite)
    application.add_handler(invite_handler)
    
    help_handler = CommandHandler('help', help_needed)
    application.add_handler(help_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.add_handler(MessageHandler(filters.TEXT, echo))
    
    application.run_polling(True)