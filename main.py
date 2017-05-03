#!/usr/bin/python3
# coding: utf8

from RPi import GPIO
from time import sleep
from subprocess import check_output,Popen
from threading import Thread
from tempfile import TemporaryFile
from os import path

from bakelite_actions import *

mpg = "/usr/bin/mpg123"
snd = "/home/pi/Bakelite/sounds/"

global NUM,hook,counter
NUM,hook,counter = "",1,0

class Bakelite(Thread):
    def __init__(self, instance="other", pinRotary=4, pinHook=11, period=0.125):
        Thread.__init__(self)
        self.instance = instance

        self.p = period
        self.pinH,self.pinR = pinHook,pinRotary
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)	
        GPIO.setup(self.pinH,GPIO.IN,pull_up_down=GPIO.PUD_UP)

        self.playMp3 = lambda g:(Popen([mpg, snd + g + ".mp3"]))
        self.callMp3 = lambda h:(call([mpg, snd + g + ".mp3"]))
        self.runCmd = lambda  j:( cmds[j][0] in str( check_output(cmds[j][1]) ) )

    def doCall(self):
        """Execute Call"""
        global NUM
        cmds['call'][1].append('call '+ NUM)
        call(cmds['call'][1])
        cmds['call'][1].pop(-1)
        NUM=""

    def listServices(self):
        """Tells all available service codes"""
        for i in act.keys():
            if isinstance(i,int) & ( (i!=17) & (i!=18) & (i!=112) ):
                call([ mpg, snd + str(i) + "_num.mp3" ])
                self.callMp3(str(i))

#    def diags(self):
#        """Execute system diagnosis"""
#            if isinstance(i,str):
#        if not (cmds["net"][0] in cmds["net"][1]):
#            exec(act["net"][0])

    def run(self):
        """ count impulsions and returns value """
        global NUM,hook,counter
        if self.instance == "rotary":
            """Read the rotary"""
            while 1 :
                enLecture,pulse = 1,0
                # Pin change is used by pin hook status, so we'll use enLecture variable
                while GPIO.input(self.pinR):
                    # Awaits the rotary release
                    sleep(0.01)
                while enLecture:
                    pulse=pulse+1
                    sleep(self.p)
                    if(GPIO.input(self.pinR) == 1):
                        enLecture=0
                        if(pulse==10):
                            pulse=0
                        NUM = NUM + str(pulse)
                        print("rotary NUM : " + str(NUM) + " pulse : " + str(pulse))
                        enLecture = 0
                        counter = 0

        elif self.instance == "hook":
            """Updates the hook status"""
            if (GPIO.input(self.pinH)):
                hook = 0
            while 1:
                # Awaits for pin change on hook and reads pin value
                GPIO.wait_for_edge(self.pinH,GPIO.FALLING)
                Popen(["/usr/bin/killall","mpg123"])
                sleep(0.5)
                if (GPIO.input(self.pinH)):
                    hook = 0
                    self.runCmd('term')
                else:
                    hook = 1
                    self.runCmd('answer')
                NUM=""

    def main(self):
        global NUM,hook,counter
        h=Bakelite("hook")
        h.start()
        r=Bakelite("rotary")
        r.start()
        while 1:
            """Main loop - call functions"""
            sleep(0.8)
            if len(NUM) != 0:
                counter = counter + 1
                print(counter)
            if counter == 10:
                NUM,counter="",0
                counter = 0
            for i in act.keys():
                if NUM == str(i):
                    exec(act[i][0])
                    NUM=""
            if hook & (len(NUM) == 10):
                self.doCall()

if __name__ == '__main__':
    p=Bakelite()
    p.main()
