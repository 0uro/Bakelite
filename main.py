#!/usr/bin/python3
# coding: utf8

from RPi import GPIO
from time import sleep
from subprocess import check_output
from threading import Thread
from tempfile import TemporaryFile
from gTTS import *

from bakelite_actions import *

global NUM,hook
NUM,hook = "",1

class Bakelite(Thread):
    def __init__(self, instance="other", pinRotary=4, pinHook=11, period=0.125):
        Thread.__init__(self)
        self.instance = instance

        self.p = period
        self.pinH,self.pinR = pinHook,pinRotary
        # CALL      -1 -> incoming    +1 -> outgoing    0 -> no call
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinR,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)	
        GPIO.setup(self.pinH,GPIO.IN,pull_up_down=GPIO.PUD_UP)


    def runCmd(self,arg):
        """TestPerformers"""
        check_output(cmds[arg][1])
        return ( cmds[arg][0] in str(check_output(cmds[arg][1])))

    def doCall(self):
        """Execute Call"""
        global NUM
        cmds['call'][1].append('call '+ NUM)
        call(cmds['call'][1])
        cmds['call'][1].pop(-1)

    def run(self):
        """ count impulsions and returns value """
        global NUM,hook
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

        elif self.instance == "hook":
            """Updates the hook status"""
            if (GPIO.input(self.pinH)):
                hook = 0
            while 1:
                # Awaits for pin change on hook and reads pin value
                GPIO.wait_for_edge(self.pinH,GPIO.FALLING)
                sleep(0.5)
                if (GPIO.input(self.pinH)):
                    hook = 0
                    self.runCmd('term')
                else:
                    hook = 1
                    self.runCmd('answer')
                NUM=""

    def main(self):
        global NUM,hook
        h=Bakelite("hook")
        h.start()
        r=Bakelite("rotary")
        r.start()
        while 1:
            """Main loop - call functions"""
            sleep(0.8)
            #| cmds['stream'][1] ):cmds['out'][1] |
            if hook:
                if not ( self.runCmd('in') | self.runCmd('out') | self.runCmd('stream') ):
                    # Calling routine
                    if ((len(NUM) == 2) | (len(NUM) == 3)):
                        if ((NUM == '17') | (NUM == '18') | (NUM == '112')):
                            print("calling emergency")
#                            self.doCall()
                    elif len(NUM) == 10:
                        print("calling")
                        self.doCall()
            else:
                # Service codes
                if len(NUM) == 3:
                    ok=0
                    print("Lenght :" + str(len(act.keys())))
                    for i in act.keys():
                        #print "NUM : " + str(NUM)
                        #print "act : " + str(act.keys()[i])
                        if NUM == i:
                            exec(act[NUM])
                            ok=1

if __name__ == '__main__':
    p=Bakelite()
    p.main()
