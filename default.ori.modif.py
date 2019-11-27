#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import threading

from threadfile import MonThread

sys.path.append(os.path.join(os.path.dirname(__file__), "resources", "lib"))

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

global tempsdeLecture
tempsdeLecture = 2.0        # when a time.sleep(tempsdeLecture) is done to let the user read the screen. to ajust
                            # to be ergonomic or ask the user the wish timeout



class mainBoucle(pyxbmct.AddonDialogWindow):
        #couverture = None  # type: ControlImage

    def __init__(self,*args, **kwargs):
        super(mainBoucle, self).__init__()

        #if sys.version_info.major==3:
        #   super().__init__(*args, **kwargs)

        # def onInit(self):
        self.longprocess = False
        self.EvenementPause = threading.Event()

        xbmc.log('Starting test Long Process thread ...', xbmc.LOGNOTICE)
        SIZESCREEN_HEIGHT = xbmcgui.getScreenHeight()  # exemple  # 1080
        SIZESCREEN_WIDTH = xbmcgui.getScreenWidth()  # 1920
        self.GRIDSCREEN_Y, Reste = divmod(SIZESCREEN_HEIGHT, 10)  # 108
        self.GRIDSCREEN_X, Reste = divmod(SIZESCREEN_WIDTH, 10)  # 192

        self.screenx = SIZESCREEN_WIDTH
        self.screeny = SIZESCREEN_HEIGHT
        xbmc.log('Size of Screen : ' + str(self.screenx) + ' x ' + str(self.screeny), xbmc.LOGNOTICE)

        #pyxbmct :
        self.setGeometry(self.screenx, self.screeny, 9, 4)
        #self.setGeometry(700, 450, 9, 4)
        #self.set_info_controls()
        #self.set_active_controls()
        # enlever mais à étudier de près :
        #self.set_navigation()
        xbmc.log('geometrySet' , xbmc.LOGNOTICE)
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


        self.image_dir = ARTWORK    # path to pictures used in the program

        self.image_background =   self.image_dir + '/fond-noir.jpg'  # in next release could be change by users
        self.image_button_pause = self.image_dir + '/pause.png'   # get from Xsqueeze
        self.image_button_stop =  self.image_dir + '/stop.png'     # get from Xsqueeze
        self.image_button_play =  self.image_dir + '/play.png'     # get from Xsqueeze

        '''
        # la boite de texte 2 carrés de large sur 8 de hauteur (test avec 3 -> pas assez d'espace)
        # attention qu'elle ne chevauche pas la playerbox
        self.textbox = xbmcgui.ControlTextBox(50, 50, self.GRIDSCREEN_X * 3 , self.GRIDSCREEN_Y * 7  , \
                                              textColor='0xFF888888')                   # surface  : 384 x 756
        # défilement ?
        self.textbox.autoScroll()
        self.textbox.

        self.addControl(self.textbox)
        textbox_label = pyxbmct.Label('TextBox')
        self.placeControl(textbox_label, 3, 0)
        '''
        # TextBox pyxbmct
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 3, 1, 2, 1)
        self.textbox.setText('It can display long text.\n'
                             'Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(1000, 1000, 1000)

        # bouton play
        self.button = pyxbmct.Button('Play')
        self.placeControl(self.button, 8, 2)
        # Connect control to close the window.
        self.connect(self.button, self.play)

        # bouton stop
        self.button = pyxbmct.Button('Stop')
        self.placeControl(self.button, 8, 3)
        # Connect control to close the window.
        self.connect(self.button, self.close)

        '''
        # bouton pause
        button_pause_x = self.GRIDSCREEN_X * 4 - 30
        button_pause_y = self.GRIDSCREEN_Y * 6  # take place play button
        self.button_pause = xbmcgui.ControlButton(button_pause_x, button_pause_y, 32, 32, \
                                                      "Pause", \
                                                      focusTexture=self.image_button_pause, \
                                                      noFocusTexture=self.image_button_pause, alignment=24, \
                                                      textColor='0xFF000000', focusedColor='0xFF000000', \
                                                      shadowColor='0xFFCCCCCC', disabledColor='0xFF000000')
        self.addControl(self.button_pause)
        self.button_pause.setVisible(True)
        self.button_pause_ID = self.button_pause.getId()

        # bouton Resume
        button_resume_x = self.GRIDSCREEN_X * 4 - 60
        button_resume_y = self.GRIDSCREEN_Y * 6  # take place play button

        self.button_resume = xbmcgui.ControlButton(button_resume_x, button_resume_y, 32, 32, \
                                                  "Resume", \
                                                  focusTexture=self.image_button_pause, \
                                                  noFocusTexture=self.image_button_pause, alignment=24, \
                                                  textColor='0xFF000000', focusedColor='0xFF000000', \
                                                  shadowColor='0xFFCCCCCC', disabledColor='0xFF000000')

        self.addControl(self.button_resume)

        self.button_resume.setVisible(True)
        self.button_resume.setEnabled(True)
        self.button_resume_ID = self.button_resume.getId()

        # focus
        self.setFocus(self.button_play)
        '''

    def onAction(self, action):
        # Action id's are there :
        # https://codedocs.xyz/AlwinEsch/kodi/group__kodi__key__action__ids.html
        if action == 10 or action == 92 or action == 13 or action == 163:
            self.saveQuit()

            # piqué de speedtest mais à revoir totalement

    def saveQuit(self):
        self.close()

    def play(self):
        self.run()

    def onClick(self, control):  # est-ce les clics sur les boutons ?
        xbmc.log("appui sur un  bouton" + str(control), xbmc.LOGNOTICE)
        if control == self.button_play_ID:
            xbmc.log(str(self.button_play_ID), xbmc.LOGNOTICE)
            print('Action asked : Play')
            self.setFocus(self.button_stop)
            self.run()
            # self.displayButtonPause('visible')
            # voir si on peut mettre ici le lancement du thread de souscription plutôt que dans squeezetest()
            # mieux serait de placer un controleur intermediaire qui aiguille vers les subscribe ou commande ou etc...
            # à réflechir

        if control == self.button_stop_ID:
            xbmc.log("appui sur bouton stop", xbmc.LOGNOTICE)
            print('Action asked : Stop ')
            self.saveQuit()

        if control == self.button_pause_ID:
            xbmc.log("appui sur bouton Pause", xbmc.LOGNOTICE)
            print('Action asked : Pause ')
            # insèrer event

        if control == self.button_resume_ID:
            xbmc.log("appui sur bouton Resume", xbmc.LOGNOTICE)
            print('Action asked : Resume ')
            # insèrer event de reprise du thread


    def update_textbox(self, text):
        self.textbox.setText("\n".join(text))


    def run(self):

        informationText = ['Running Test Long Process Addon Script'] # une liste
        self.update_textbox(informationText)
        informationText.append('Version de Kodi : ' + str(KODI_VERSION))
        self.update_textbox(informationText)
        informationText.append('Addon : ' + ADDONNAME + ' ; version : ' + ADDONVERSION)
        self.update_textbox(informationText)
        #self.displayScreenSize(self, informationText)
        informationText.append('Size of screen : ' + str(self.screenx) + ' x ' + str(self.screeny))
        self.update_textbox(informationText)
        xbmc.log("Au milieu de l'affichage", xbmc.LOGNOTICE)
        informationText.append('Now is playing :')
        self.update_textbox(informationText)
        #self.setFocus(self.button_stop)
        xbmc.log("before EventPause", xbmc.LOGNOTICE)
        self.EvenementPause.set()
        xbmc.log("after EventPause", xbmc.LOGNOTICE)
        self.longprocessbackground = MonThread(self.EvenementPause)
        self.longprocessbackground.start()
        while not self.longprocessbackground.threadisrunning:  # on attend que le thread soit bien démarré j'aurais pu utiliser un event ?
            # print('un tour')
            time.sleep(0.1)
        xbmc.log("after start long thread", xbmc.LOGNOTICE)
        self.longprocess = True
        while self.longprocessbackground.threadisrunning:
            informationText.append(self.longprocessbackground.dataExchange)
            self.update_textbox(informationText)
        informationText.append(" sorti de boucle ")
        self.update_textbox(informationText)


if __name__ == '__main__':
    window = mainBoucle('thread long Demo')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window

