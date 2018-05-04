#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_service():
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # You can browse other available api services and versions here:
    #     http://g.co/dv/api-client-library/python/apis/
    return googleapiclient.discovery.build('storage', 'v1')


def upload_object(bucket, filename, readers="", owners=""):
    service = create_service()

    # This is the request body as specified:
    # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
    body = {
        'name': filename,
    }

    # If specified, create the access control objects and add them to the
    # request body
    if readers or owners:
        body['acl'] = []

    for r in readers:
        body['acl'].append({
            'entity': 'user-%s' % r,
            'role': 'READER',
            'email': r
        })
    for o in owners:
        body['acl'].append({
            'entity': 'user-%s' % o,
            'role': 'OWNER',
            'email': o
        })

    # Now insert them into the specified bucket as a media insertion.
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert
    with open(filename, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket, body=body,
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            media_body=googleapiclient.http.MediaIoBaseUpload(
                f, 'video/ogg'))
        resp = req.execute()

    return resp


"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import argparse
import json
import tempfile

import googleapiclient.discovery
import googleapiclient.http



#==============================

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

#==============================

from telegram import ext
from telegram import ReplyKeyboardMarkup

#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#from telegram import ext.Filters
#from telegram import ext.MessageHandler
#from telegram import ext.Updater


#def novo(bot, update):
    
def text(bot, update):
    update.message.reply_text(update.message.text)


#    print("before")
#    update.message.reply_text("Hey Whatsapp?")
#    bot.once()
#    print("after")
#    #update.message.reply_text(update.message.text)
#    keyboard = [['ES', 'EN']]
#
#    # Create initial message:
#    message = "Hey, I'm DisAtBot! / ¡Hey, soy DisAtBot! \n\n\
#              Please select a language to start. / Por favor selecciona un idioma \
#              para comenzar."
#
#    reply_markup = ReplyKeyboardMarkup(keyboard,
#                                       one_time_keyboard=True,
#                                       resize_keyboard=True)
#    update.message.reply_text(message, reply_markup=reply_markup)

    
def voice(bot, update):
    print ("00000000000000")
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    newFile.download('voice.ogg')
    create_service()
    print ("AAAAAAAAAAAAAA")
    upload_object("sdbot", "voice.ogg")
    audio = types.RecognitionAudio(uri='gs://sdbot/voice.ogg')
    
    print ("BBBBBBBBBBBBBB")
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code='pt-BR')
    
    # [START migration_sync_response]
    response = client.recognize(config, audio)
    print ("11111111111111")
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}\n Confidence: {}'.format(
              result.alternatives[0].transcript, result.alternatives[0].confidence))
        print ("22222222222222")
        transcript = result.alternatives[0].transcript
        if transcript.upper().startswith("CARLOS"):
            transcript = transcript.replace("Carlos", "")
            print ("33333333333333")
            update.message.reply_text(transcript)

def main():

    updater = ext.Updater("")
    dp = updater.dispatcher
    dp.add_handler(ext.MessageHandler(ext.Filters.voice, voice))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
