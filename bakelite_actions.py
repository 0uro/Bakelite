#!/usr/bin/python3
# coding: utf8

from subprocess import *

phone = ['linphonecsh','generic']
answer = phone + ['answer']
term = phone + ['terminate']

mpg = 'mpg123'
snd = '/home/pi/Bakelite/sounds/'

PHONE = {
            'hook'      : 0     ,\
            'counter'   : 0     ,\
            'NUM'       : ""    ,\
        }

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
    911 : [ 'self.doDiags()',               "effectue un diagnostic système."],\
    999 : [ 'self.playMp3("itcrowd")',      "appel non urgent."],\
}

#test = {\
#        'call'  :   lambda:("Incoming" in str(check_output(phone + ['calls'])) |\
#                            "Outgoing" in str(check_output(phone + ['calls'])) |\
#                            "Stream"   in str(check_output(phone + ['calls'])) ),\
#        'net'   :   lambda:("1 received" in str(check_output(['/bin/ping','-c1','www.free.fr'])))\
#}
#    'call'      :   [ lambda:(test['call']), "appel en cours."],\
#    'no_call'   :   [ lambda:(test['call']), "aucun appel en cours."],\
#    'net'       :   [ lambda:(test['net']),  "connecté au réseau."],\
#    'no_net'    :   [ lambda:(test['net']),  "problème de connexion détecté"],\
