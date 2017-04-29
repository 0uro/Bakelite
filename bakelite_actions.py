# coding: utf8

from subprocess import *

mpg = '/usr/bin/mpg123'
snd_path = '/home/pi/phone_sounds/'
phone = '/usr/bin/linphonecsh'
kill = '/usr/bin/killall'

gen = 'generic'

#def runCmd(arg):
#    return( cmds[arg][0] in str(check_output(cmds[arg][1])) )

voices = {\
    'list'  : "liste les services disponibles.",\
    'shut'  : "éteint le téléphone.",\
    'pi'    : "donne les premières décimales de pi.",\
    'ghost' : "à utiliser en cas d'attaque de fantômes.",\
    'diag'  : "effectue un diagnostic système.",\
    'crowd' : "appel non urgent.",\
    'nocall': "aucun appel actif.",\
    'call'  : "appel en cours.",\
    'sip'   : "il y a un problème d'enregistrement SIP.",\
    'net'   : "il y a un problème de connection au réseau.",\
    'ok'    : "aucun problème détecté.",\
}

act = {\
    111 : 'self.Test("service")',\
    123 : '/usr/bin/sudo /sbin/halt -f',\
    314 : mpg + 'pi.mp3',\
    666 : mpg + 'ghost.mp3',\
    999 : mpg + 'itcrowd.mp3',\
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
