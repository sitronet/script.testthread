#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import threading
import time

from threadfile import MonThread

sys.path.append(os.path.join(os.path.dirname(__file__), "resources", "lib"))

# choose to run on Kodi or Not
global Kodi
Kodi = True

if Kodi:
    import xbmc
    import xbmcgui
    import xbmcaddon
    import pyxbmct

if Kodi:
    ADDON = xbmcaddon.Addon()
    ADDONID = ADDON.getAddonInfo('id')
    ADDONNAME = ADDON.getAddonInfo('name')
    ADDONVERSION = ADDON.getAddonInfo('version')
    ARTWORK = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'), 'resources', 'skins', 'Default', 'media'))
    KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])

    # screen 16:9 so to have grid square fix to 16-9 on 1280 x 720 max of pyxbmct
    SIZE_WIDTH_pyxbmct = 1280
    SIZE_HEIGHT_pyxbmct = 720
    SEIZE = 32
    NEUF = 18

global tempsdeLecture
tempsdeLecture = 2.0        # when a time.sleep(tempsdeLecture) is done to let the user read the screen. to ajust
                            # to be ergonomic or ask the user the wish timeout

# choose if you want test a simple prog or an another thread for the computationnal long process
LongThread = False # True or  False choice todo depend of the test

class TestMainPyxbmct(pyxbmct.AddonFullWindow):

    def __init__(self,*args, **kwargs):
        super(TestMainPyxbmct, self).__init__()

        self.longprocess = False
        self.EvenementActif = threading.Event()
        self.EvenementAManger = threading.Event()
        self.threadisrunning = threading.Event()

        xbmc.log('Starting test Long Process thread ...A... increment ', xbmc.LOGNOTICE)
        SIZESCREEN_HEIGHT = xbmcgui.getScreenHeight()  # exemple  # 1080
        SIZESCREEN_WIDTH = xbmcgui.getScreenWidth()  # 1920
        self.GRIDSCREEN_Y, Reste = divmod(SIZESCREEN_HEIGHT, 10)  # 108
        self.GRIDSCREEN_X, Reste = divmod(SIZESCREEN_WIDTH, 10)  # 192

        self.screenx = SIZESCREEN_WIDTH
        self.screeny = SIZESCREEN_HEIGHT

        # set to don't over the max pyxbmct
        if self.screenx > SIZE_WIDTH_pyxbmct:
            self.screenx = SIZE_WIDTH_pyxbmct
            self.screeny = SIZE_HEIGHT_pyxbmct

        #pyxbmct :
        self.setGeometry(self.screenx  , self.screeny , SEIZE, NEUF)
        xbmc.log('Size of Screen fix to : ' + str(self.screenx) + ' x ' + str(self.screeny), xbmc.LOGDEBUG)

        # TextBox pyxbmct
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 3, 1, 20, 8, 2, 1)
        self.textbox.setText('It can display long text.\n'
                             'Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(100, 100, 100)  # I didn't find the documentation to set param of Scroll, hazardous
        xbmc.log('text box set' , xbmc.LOGNOTICE)

        # bouton play
        self.buttonplay = pyxbmct.Button('Play')
        self.placeControl(self.buttonplay, 25, 7)
        # Connect control to start the long process
        self.connect(self.buttonplay, self.play)
        xbmc.log('play bouton  set', xbmc.LOGNOTICE)

        # bouton stop
        self.buttonstop = pyxbmct.Button('Exit')
        self.placeControl(self.buttonstop, 25, 11)
        # Connect control to close the window.
        self.connect(self.buttonstop, self.saveQuit)
        xbmc.log('stop bouton set', xbmc.LOGNOTICE)

        # mettre un boutontest
        self.buttontest = pyxbmct.Button('Test')
        self.placeControl(self.buttontest, 25, 5)
        # Connect control to test the navigation in the window.
        self.connect(self.buttontest, self.test)
        xbmc.log('test bouton set', xbmc.LOGNOTICE)

        # bouton pause
        self.buttonpause = pyxbmct.Button('Pause')
        self.placeControl(self.buttonpause, 25, 8)
        # Connect control to pause the long process.
        self.connect(self.buttonpause, self.pause)
        #self.connect(self.buttonpause, lambda: self.pause) ?? Why this doesn't work ??
        xbmc.log('pause bouton set', xbmc.LOGNOTICE)

        # bouton resume
        self.buttonresume = pyxbmct.Button('Resume')
        self.placeControl(self.buttonresume, 25, 9)
        # Connect control to resume the long process
        self.connect(self.buttonresume, self.resume)
        xbmc.log('resume bouton set', xbmc.LOGNOTICE)

        # navigation between button see below
        self.set_navigation()

        # Connect a key action (Backspace) to close the window. take from pyxbmct example
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_navigation(self):
        # Set navigation between controls (Button)
        self.buttonstop.controlLeft(self.buttonplay)
        self.buttonstop.controlRight(self.buttonplay)
        self.buttonplay.controlLeft(self.buttontest)
        self.buttonplay.controlRight(self.buttonpause)
        self.buttonpause.controlLeft(self.buttonplay)
        self.buttonpause.controlRight(self.buttonresume)
        self.buttonresume.controlLeft(self.buttonpause)
        self.buttonresume.controlRight(self.buttonstop)
        self.buttontest.controlLeft(self.buttonplay)
        self.buttontest.controlRight(self.buttonplay)
        # Set initial focus
        self.setFocus(self.buttonplay)

    def play(self):
        self.run()

    def test(self):
        xbmc.log("Bouton Test pressé", xbmc.LOGNOTICE)

    def pause(self):
        xbmc.log("Bouton Pause pressé", xbmc.LOGNOTICE)
        self.EvenementActif.clear()

    def resume(self):
        self.EvenementActif.set()
        xbmc.log("Bouton Resume pressé", xbmc.LOGNOTICE)
        #self.longprocessbackground.evenementActif.set() ?? is it possible to do that ??
        # not yet before long..ground is started

    def saveQuit(self):
        self.close()

    def update_textbox(self, text):
        self.textbox.setText("\n".join(text))

    def run(self):
        xbmc.log("début de run  ", xbmc.LOGNOTICE)
        informationText = ['Running Test Long Process Addon Script'] # une liste
        self.update_textbox(informationText)
        informationText.append('Version de Kodi : ' + str(KODI_VERSION))
        self.update_textbox(informationText)
        informationText.append('Addon : ' + ADDONNAME + ' ; version : ' + ADDONVERSION)
        self.update_textbox(informationText)
        informationText.append('Size of screen : ' + str(self.screenx) + ' x ' + str(self.screeny))
        self.update_textbox(informationText)

        informationText.append('Now play button -> prog is playing :')
        self.update_textbox(informationText)
        self.setFocus(self.buttonpause) # after start get focus on the pause bouton
        # à definir le thread n'est pas en pause
        #self.EvenementActif.clear()
        self.EvenementActif.set()
        if LongThread:
            xbmc.log("Start Long Thread run main 1 : " + str(self.threadisrunning.is_set()), xbmc.LOGNOTICE)
            self.longprocessbackground = MonThread(self.EvenementActif , self.EvenementAManger, self.threadisrunning)
            self.longprocessbackground.start()
            xbmc.log("event run main 2 : " + str(self.threadisrunning.is_set()), xbmc.LOGNOTICE)
            self.threadisrunning.wait()   # on attend que le thread soit bien démarré j'aurais pu utiliser un event ?
                                          # remplacer un booléen par un event
            xbmc.log('long thread is running ', xbmc.LOGNOTICE)
            time.sleep(0.1)
            xbmc.log("after long thread is running ", xbmc.LOGNOTICE)
            self.longprocess = True
            while self.threadisrunning.is_set():
                self.EvenementAManger.wait(10)  # Timeout because at the last turn always False so deadlock
                informationText.append(self.longprocessbackground.dataExchange)  # ?? or use Queue ??
                self.EvenementAManger.clear()
                xbmc.log(" prog principal , je prends à manger : " + self.longprocessbackground.dataExchange, xbmc.LOGNOTICE)
                self.update_textbox(informationText)
                informationText.append('Miam miam')
                self.update_textbox(informationText)
                time.sleep(0.1) # to let time interruption of window pyxbmct
                xbmc.log("Run boucle in main with Long thread: " + str(self.threadisrunning.is_set()), xbmc.LOGNOTICE)
        else:
            xbmc.log("Run simple boucle in main ", xbmc.LOGNOTICE)
            for i in range(0, 50):
                xbmc.log(" prog principal , je suis dans le tour n°  : " + str(i),  xbmc.LOGNOTICE)
                if not self.EvenementActif.is_set():    # set if buton pause is on
                    xbmc.log(' en  pause dans la boucle simple', xbmc.LOGNOTICE)
                    self.EvenementActif.wait()  # wait to resume (buton resume)
                time.sleep(0.5)
                informationText.append(" Tour de Boucle simple : " + str(i))
                self.update_textbox(informationText)

        informationText.append(" Sortie de boucle ")
        self.update_textbox(informationText)
        xbmc.log("Sortie de boucle ", xbmc.LOGNOTICE)

        # necessaire pour rejoindre la fin du thread, évite le bug de sortie de programme
        if LongThread:
            self.longprocessbackground.join()
            xbmc.log("join() between thread is done", xbmc.LOGNOTICE)
            informationText.append(" les threads sont joints ")
            self.update_textbox(informationText)
        else:
            xbmc.log("fin de run de main", xbmc.LOGNOTICE)
            informationText.append(" programme terminé ")
            self.update_textbox(informationText)
    # fin fonction run


if __name__ == '__main__':
    window = TestMainPyxbmct('thread long Demo')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window

