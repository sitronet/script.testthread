#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import xbmc

class MonThread (threading.Thread):

    dataExchange = ''       # ?? or use a queue ?? attribute of Class seen outside the Class
    recevoirEnAttente = threading.Event()
    demandedeStop = threading.Event()

    def __init__ (self, evenementActif , evenementaManger , threadisrunning) :

        threading.Thread.__init__ (self)
        self.evenementActif = evenementActif
        self.evenementaManger = evenementaManger
        self.threadisrunning = threadisrunning
        self.dataExchange = ''

    def run (self) :
        xbmc.log(" long thread run ...", xbmc.LOGNOTICE)
        self.threadisrunning.set()
        xbmc.log("event thread is running  : " + str(self.threadisrunning.is_set()), xbmc.LOGNOTICE)
        if not self.evenementActif.is_set():        # buton pause is on
            xbmc.log(" thread en pause ...", xbmc.LOGNOTICE)
            self.evenementActif.wait()              # wait the buton resume
        else:
            xbmc.log(str("event Actif : " + str(self.evenementActif.is_set)), xbmc.LOGNOTICE)
        for i in range (0, 50) :
            if not self.evenementActif.is_set():
                self.dataExchange = 'Mon long Thread ; en  pause dans la boucle For'
                xbmc.log(" Mon long thread en pause ...dans boucle For ", xbmc.LOGNOTICE)
                self.evenementaManger.set()
            xbmc.log(" je suis Monthread , je suis dans ma boucle n° :  " + str(i) , xbmc.LOGNOTICE)
            self.evenementActif.wait()  # always True unless the buton pause is set
            self.dataExchange = "MonThread give to eat - Turn n° : " + str(i) + " do you like it ?"
            self.evenementaManger.set()
            time.sleep (0.5)

        self.dataExchange = "MonThread arrete de donner à manger : "
        self.threadisrunning.clear()        # the long thread will stop
        xbmc.log(" long thread End of run()", xbmc.LOGNOTICE)
        # indique au prog main que c'est la fin pour la boucle de main
        xbmc.log("event long thread is running : " + str(self.threadisrunning.is_set()), xbmc.LOGNOTICE)
        return

    #follow some function that are not used but could be test and call from the main process
    def thread_pause_fonction (self) :
        # fontion pause
        self.evenementActif.clear()

    def thread_resume_fonction(self):
        '''
        fonction Resume when buton resume is on
        :return:
        '''
        self.evenementActif.set()

