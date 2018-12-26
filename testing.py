import logging
import os
import time

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']

LedPin =7
FanPin =29

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping = {'status':'status'})

def Gpio_Intent(status,room):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LedPin,GPIO.OUT)

    if status in STATUSON:
        GPIO.output(LedPin,GPIO.HIGH)
        return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        GPIO.output(LedPin,GPIO.LOW)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')
def Gpio_Intent(status,room):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FanPin,GPIO.OUT)

    if status in STATUSON:
        GPIO.output(FanPin,GPIO.HIGH)
        return statement('turning {} fan'.format(status))
    elif status in STATUSOFF:
        GPIO.output(FanPin,GPIO.LOW)
        return statement('turning {} fan'.format(status))
    else:
        return statement('Sorry not possible.')


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=False)

