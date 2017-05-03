#!/usr/bin/python3
# coding: utf8

from gtts import *

from bakelite_actions import *

snd_path = "./sounds/"

for i in act.keys():
    tts = gTTS(act[i][1],"fr")
    tts.save(snd_path + str(i) + ".mp3")
