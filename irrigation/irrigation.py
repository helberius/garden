import os
import json
import logging
import datetime
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from common.configuration import Configuration

class Irrigation():
    conf = None
    logging_file = None
    def __init__(self):
        # print('irrigation')

        # conf_folder =os.environ['conf_irrigation']
        # print(conf_folder)
        self.conf =  Configuration()
        self.create_log()

        self.log.info('-----------------------------------------------------------------')
        self.log.info('This is the irrigation module :'  + str(datetime.datetime.now()))
        self.log.info('-----------------------------------------------------------------')
        self.start_irrigation()
        self.log.info('job done, have a good day')
        GPIO.cleanup()



    def create_log(self):
        path_configuration_folder = os.environ['conf_folder']

        self.log = logging.getLogger("irg")
        self.log.setLevel(self.conf.log_level)
        path_log_file = os.path.join(path_configuration_folder,'irrigation_log.txt')
        fh = logging.FileHandler(path_log_file)
        fh.setLevel(self.conf.log_level)
        ch = logging.StreamHandler()
        #ch.setLevel(self.conf['log_level'])
        self.log.addHandler(fh)
        self.log.addHandler(ch)


    def start_irrigation(self):
        self.log.debug('start_irrigation')
        #self.log.info(self.conf['tempos'])
        current_day_of_week = datetime.datetime.today().weekday()
        self.log.debug('current day of the week: ' + str(current_day_of_week))

        ls_relays=[]
        try:
            Relay1_GPIO = 12
            Relay2_GPIO = 7
            Relay3_GPIO = 8
            Relay4_GPIO = 25
            ls_relays=[Relay1_GPIO,Relay2_GPIO,Relay3_GPIO, Relay4_GPIO ]
        except Exception as err:
            self.log.error('Error while initializing the gpio')
            self.log.error(repr(err))


        try:
            for i in range(0,len(self.conf.peridiocity_irrigation)):
                line = self.conf.peridiocity_irrigation[i]
                relay = ls_relays[i]
                if current_day_of_week in line['days']:
                    self.log.info('i will operate here today:')
                    self.log.info(line)
                    GPIO.output(relay, GPIO.HIGH)
                    sleep(line['duration']*self.conf.time_factor)
                    GPIO.output(relay, GPIO.LOW)


        except Exception as err:
            self.log.error('Error while working with gpios')
            self.log.error(repr(err))
