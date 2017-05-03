#!/usr/bin/python3
# coding: utf8

from RPi import GPIO
from time import sleep
from subprocess import check_output,Popen
from threading import Thread
from os import path

from bakelite_actions import *

global STATUS
STATUS= {\
            'hook'      : 0     ,\
            'count'     : 0     ,\
            'num'       : ""    ,\
        }

class Bakelite(Thread):
    def __init__(self, instance="other", pinRotary=4, pinHook=11, period=0.125):
        Thread.__init__(self)
        self.instance = instance

        self.p = period
        self.pinH,self.pinR = pinHook,pinRotary
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)	
        GPIO.setup(self.pinH,GPIO.IN,pull_up_down=GPIO.PUD_UP)

        self.playMp3 = lambda g:(Popen( [mpg , snd + g + '.mp3'] ))
        self.callMp3 = lambda h:(call( [mpg , snd + h + '.mp3' ] ))
        self.runCmd = lambda  j:( cmds[j][0] in str( check_output(cmds[j][1]) ) )

    def doCall(self):
        """Execute Call"""
        global STATUS
        phone.append('call ' + STATUS["num"])
        call(phone)
        STATUS["num"]=""
        phone.pop(-1)

    def listServices(self):
        """Tells all available service codes"""
        for i in act.keys():
            if isinstance(i,int) & ( (i!=17) & (i!=18) & (i!=112) ):
                call([ mpg + str(i) + "_num.mp3" ])
                self.callMp3(str(i))

#    def doDiags(self):
#        for i in act.keys():
#            if isinstance(i,str):
#                exec( act[i][0]() )
#                if act[i][0]():
#                    self.callMp3(i)

    def run(self):
        """ count impulsions and returns value """
        global num,hook,count
        if self.instance == "rotary":
            """Reads the rotary"""
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
                        STATUS["num"] = STATUS["num"] + str(pulse)
#                        print("rotary num : " + str(STATUS['num']) + " pulse : " + str(pulse))
                        enLecture = 0
                        STATUS["count"] = 0

        elif self.instance == "hook":
            """Updates the hook status"""
            if (GPIO.input(self.pinH)):
                hook = 0
            while 1:
                # Awaits for pin change on hook and reads pin value
                GPIO.wait_for_edge(self.pinH,GPIO.FALLING)
                Popen(["killall",mpg[0]])
                sleep(0.5)
                if (GPIO.input(self.pinH)):
                    STATUS["hook"] = 0
                    print(term)
                    call(term)
                else:
                    STATUS["hook"] = 1
                    call(answer)
                STATUS["num"]=""

    def main(self):
        """Start instances, handles timeout and execute actions"""
        global STATUS
        h=Bakelite("hook")
        h.start()
        r=Bakelite("rotary")
        r.start()

        while 1:
            """Main loop - call functions"""
            sleep(0.8)

            # Timeout
            if len(STATUS["num"]) != 0:
                STATUS["count"] = STATUS["count"] + 1
            if STATUS["count"] == 10:
                STATUS["num"],STATUS["count"]="",0

            # Service codes
            for i in act.keys():
                if STATUS["num"] == str(i):
                    exec(act[i][0])
                    STATUS["num"]=""

            # Phone call
            if STATUS["hook"] & (len(STATUS["num"]) == 10):
                self.doCall()

if __name__ == '__main__':
    p=Bakelite()
    p.main()
