# Author	: Ali Salehi
# github	: https://github.com/salehiali1374/PDMB
# Email		: salehiali1374@gmail.com
#
# requirement	:  aria2c
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os
import re
from os.path import expanduser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tempfile

#config telegram Bot
TOKEN = 'TOKEN'
updater = Updater(TOKEN)

#config Download Path
Home = expanduser('~')
dl_path = Home + "/Downloads/PDMB"

# start msg, to help user
def start_bot(bot, updater):
    bot.sendMessage(updater.message.chat_id, 'Hello. This is personal download manager bot. If you need help check `/help`')

#gets links with format `/link link(s)`. you can separate your links with space.
def download_link_bot(bot, updater, args):
    bot.sendMessage(updater.message.chat_id, 'We Got Your Link(s)...')
    for links in args:
        print links
        try:
            msg = start_download(links)
            bot.sendMessage(updater.message.chat_id, msg)
        except Exception:
            print Exception.message
            bot.sendMessage(updater.message.chat_id, 'It Seems link has problem.')


def download_file_contents_bot(bot, updater):
    # get file id
    file = bot.getFile(updater.message.document.file_id)
    # create a randon temp file name
    tf = tempfile.mkstemp()
    # download file
    file.download(tf[1])
    # read file content
    bot.sendMessage(updater.message.chat_id, 'We Got Your File...')
    try:
        with open(tf[1], "r") as fp:
            for link in fp:
                print link
                msg = start_download(str(link))
                bot.sendMessage(updater.message.chat_id, msg)
    except Exception:
        print Exception.message
        bot.sendMessage(updater.message.chat_id, "There is something wrong with file...")

# list of downloads
def list_bot(bot, updater):
    file_list = os.listdir(dl_path)
    file_list = '\n\n'.join(file_list)
    bot.sendMessage(updater.message.chat_id, file_list)

# help
def help_bot(bot, updater):
    helpMSG = 'Welcome to PDMB\'s help.\n\n' \
              'I will update this bot as soon as I can.\n' \
              'I appreciate if you inform me of any bug or issue.\n' \
              '--------------------------------------------------------------------\n ' \
              'Here is what I\'v done by now:\n\n' \
              '/link \t:\t you can put your link(s) with space and send it to me. I will download it one by \n\n' \
              '/list \t:\t you can get a list of Completed Downloads.\n\n' \
              'you can ALSO send me a file with links content. make sure to put one link in each line.'
    bot.sendMessage(updater.message.chat_id, helpMSG)


# start download with aria2c
def start_download(link):
    # check links with regex to be valid :)
    linkregex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    mylink = re.findall(linkregex, link)
    if mylink:
        # Download link
        print dl_path
        print mylink[0]
        r = os.system('aria2c -d "{}" -x 16 "{}"'.format(dl_path,str(mylink[0])))#''aria2c -d '+ dl_path + ' -j 16 '+ str(mylink))
        if r == 0:
            return 'Download Complete'
        elif r == 1:
            return 'Unknown Error in URL'
        elif r == 2:
            return 'Timeout'
    else:
        # URL doesn't match with regex !!!
        return 'URL Not Found!'


def main():
    if not os.path.exists(dl_path):
        print "path doesn't exist. try to make one"
        os.makedirs(dl_path)


    updater.start_polling()


    # start
    updater.dispatcher.add_handler(CommandHandler('start', start_bot))

    # to Download links
    updater.dispatcher.add_handler(CommandHandler('link', download_link_bot, pass_args= True))

    # to Download file contents
    updater.dispatcher.add_handler(MessageHandler(Filters.document, download_file_contents_bot))

    # to show list of compelete downloads
    updater.dispatcher.add_handler(CommandHandler('list', list_bot))

    # help
    updater.dispatcher.add_handler(CommandHandler('help', help_bot))
    #for exit
    updater.idle()


if __name__ == '__main__':
    main()
