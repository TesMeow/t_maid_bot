#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging,os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters, ConversationHandler
from random import choice, sample

# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CONTENT, TIME, FREQ = range(3)


def start(update, context):
    update.message.reply_text(
        '主人您好，我是Tessa的女仆Tia酱。请问主人需要被提醒的内容是什么呢？')

    return CONTENT


def content(update, context):
    user = update.message.from_user
    logger.info("Reminder Content of %s: %s", user.id, update.message.text)
    update.message.reply_text('明白了呢主人，是想被提醒 {} 呢。\n那么请问主人想在几点被提醒呢？'.format(update.message.text))

    return TIME


def time(update, context):
    user = update.message.from_user
    logger.info("Time of %s: %s", user.id, update.message.text)
    update.message.reply_text('请问主人想间隔多久被提醒一次呢？')

    return FREQ

def freq(update, context):
    user = update.message.from_user
    logger.info("Freq of %s: %s", user.id, update.message.text)
    update.message.reply_text('好的哦，Tia酱记住啦～')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.id)
    update.message.reply_text('主人再见啦w')

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token = os.environ["TOKEN"], use_context = True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CONTENT: [MessageHandler(Filters.text, content)],

            TIME: [MessageHandler(Filters.text, time)],

            FREQ: [MessageHandler(Filters.text, freq)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
