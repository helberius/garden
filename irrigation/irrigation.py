import os
import json
import logging
import datetime
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
from common.configuration import Configuration

class Irrigation():
    conf = None
    logging_file = None
    ls_relays=[8,10,12,16]
    
    def __init__(self):
        # print('irrigation')

        # conf_folder =os.environ['conf_irrigation']
        # print(conf_folder)
        self.conf =  Configuration()
        self.create_log()

        self.log.info('-----------------------------------------------------------------')
        self.log.info('This is the irrigation module :'  + str(datetime.datetime.now()))
        self.log.info('-----------------------------------------------------------------')
        self.init_pins()
        #self.start_irrigation()
        self.log.info('job done, have a good day')
        self.play_relay_1()
        self.play_relay_2()
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

    def init_pins(self):
        try:
            
            for r in self.ls_relays:
                GPIO.setup(r, GPIO.OUT)
                GPIO.output(r, True)
            
        except Exception as err:
            self.log.error('Error while initializing the gpio')
            self.log.error(repr(err))
        
    def start_irrigation(self):
        self.log.debug('start_irrigation')
        #self.log.info(self.conf['tempos'])
        current_day_of_week = datetime.datetime.today().weekday()
        self.log.debug('current day of the week: ' + str(current_day_of_week))

        try:
            for i in range(0,len(self.ls_relays)):
                line = self.conf.peridiocity_irrigation[i]
                relay = self.ls_relays[i]
                if current_day_of_week in line['days']:
                    self.log.info('i will operate here today:')
                    self.log.info(line)
                    GPIO.output(relay, False)
                    sleep(line['duration']*self.conf.time_factor)
                    GPIO.output(relay, True)


        except Exception as err:
            self.log.error('Error while working with gpios')
            self.log.error(repr(err))
            
    def play_relay_1(self):
        for i in range(0,10):
            for r in self.ls_relays:
                GPIO.output(r,False)
                sleep(0.25)
                GPIO.output(r,True)
                sleep(0.25)
        
    def play_relay_2(self):
        for i in range(0,10):
            for r in self.ls_relays:
                GPIO.output(r,False)
                sleep(0.15)
                GPIO.output(r,True)
                sleep(0.1)
            for r in self.ls_relays[::-1]:
                GPIO.output(r,False)
                sleep(0.15)
                GPIO.output(r,True)
                sleep(0.1)                
