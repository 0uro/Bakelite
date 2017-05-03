#!/usr/bin/python3
# coding: utf8

from subprocess import *

gen = 'generic'
phone = '/usr/bin/linphonecsh'
kill = '/usr/bin/killall'

#17  : [ 'self.doCall()',                "numéro police secours."],\
#18  : [ 'self.doCall()',                "numéro des pompiers."],\
#112 : [ 'self.doCall()',                "numéro d'urgence universel."],\

act = {\
    17  : [ 'print(17)',                    "numéro police secours."],\
    18  : [ 'print(18)',                    "numéro des pompiers."],\
    112 : [ 'print(112)',                   "numéro d'urgence universel."],\
    \
    111 : [ 'self.listServices()',          "liste les services disponibles."],\
    123 : [ '/usr/bin/sudo /sbin/halt -f',  "éteint le téléphone."],\
    \
    314 : [ 'self.playMp3("pi")',           "donne les premières décimales de pi."],\
    666 : [ 'self.playMp3("ghost")',        "à utiliser en cas d'attaque de fantômes."],\
    911 : [ 'self.playMp3("sos")',          "effectue un diagnostic système."],\
    999 : [ 'self.playMp3("itcrowd")',        "appel non urgent."],\
    \
    'nocall': ['self.playMp3("nocall")',    "aucun appel actif."],\
    'call'  : ['self.playMp3("call")',      "appel en cours."],\
    'sip'   : ['self.playMp3("sip")',       "il y a un problème d'enregistrement SIP."],\
    'net'   : ['self.playMp3("net")',       "il y a un problème de connection au réseau."],\
    'ok'    : ['self.playMp3("ok")',        "aucun problème détecté."],\
}

# TODO  111 : liste les services
# TODO  911 : aide integree

cmds = {\
    'call'      : [ "Establishing", [phone,gen              ]],\
    'in'        : [ "Incoming",     [phone,gen,'calls'      ]],\
    'out'       : [ "Outgoing",     [phone,gen,'calls'      ]],\
    'stream'    : [ "Stream",       [phone,gen,'calls'      ]],\
    'answer'    : [ "established",  [phone,gen,'answer'     ]],\
    'term'      : [ "ended",        [phone,gen,'terminate'  ]],\
    'kill'      : [ "Complété",     [kill                   ]],\
    'net'       : [ "1 received",   ['/bin/ping','-c1','www.free.fr']   ],\
}
