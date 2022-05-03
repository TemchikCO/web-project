import requests
from flask import url_for
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from constants import *
from telegram.ext import CommandHandler

markup_games = ReplyKeyboardMarkup([['/Politopy', '/Pony_Run']], one_time_keyboard=False)
markup_install_politopy = ReplyKeyboardMarkup([['/download_politopy', '/back']], one_time_keyboard=False)
markup_install_pony_run = ReplyKeyboardMarkup([['/download_pony_run', '/back']], one_time_keyboard=False)


def information(update, context):
    update.message.reply_text(
        "Привет! Я бот от Temchik&Pupsik Co.\n "
        "Здесь вы можете узнать больше о наших играх", reply_markup=markup_games)


def politopy(update, context):
    update.message.reply_text("Politopy - игра-стратегия, в который вы сможете сражаться со своими друзьями за звание самого крутого стратега. \n"
                              " Иследуйте технологии, завоёвывайте города и убивайте своих соперников различными способами.", reply_markup=markup_install_politopy)


def pony_run(update, context):
    update.message.reply_text("Pony_Run - игра жанра раннер, которая поможет вам скоротать несколько часов времени в дороге.\n"
                              " Игра с захватывающим и динамичным геймплеем не позволит вам заскучать.", reply_markup=markup_install_pony_run)


def download_politopy(update, context):
    with open("C:\Python\WEB_project\last_mission\static\zip_files\politopy.zip", "rb") as file:
        context.bot.send_document(chat_id=update.message.chat_id, document=file,
                                  filename='politopy.zip')
    update.message.reply_text("Спасибо за покупку, ждём вас снова!!!!")


def download_pony_run(update, context):
    with open("C:\Python\WEB_project\last_mission\static\zip_files\pony_run.zip", "rb") as file:
        context.bot.send_document(chat_id=update.message.chat_id, document=file,
                                  filename='pony_run.zip')
    update.message.reply_text("Спасибо за покупку, ждём вас снова!!!!")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", information))
    dp.add_handler(CommandHandler("Politopy", politopy))
    dp.add_handler(CommandHandler("Pony_Run", pony_run))
    dp.add_handler(CommandHandler("back", information))
    dp.add_handler(CommandHandler("download_politopy", download_politopy))
    dp.add_handler(CommandHandler("download_pony_run", download_pony_run))

    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
