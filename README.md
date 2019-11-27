
This script is for testing the pyxbmct lib for Kodi whith threads
* it is not working as I should like*

Description :
there is a simple main programm , in this main prog the initial steps are :
Create 4 effectives buttons (start, pause, resume and stop) and one textbox.
one test button to see if an action occurs when press the buttons. then set the navigation from button to others


The goal is : to start a long process computational with the start button.
pause the long process with the pause button, resume with the resume button, etc...
and stop the program with the stop button. (very simple)
The long process computational is a simple long loop (while or for) and print in the textbox a message for each turn of the loop

the long process could be inside the main program or in a separate thread ,
just define a boolean flag on the beginning of the code to try either one or the other.

The program doesn't work as my wish because once the long process is started the buttons have no action even if we can navigate
between them. The buttons don't respond to the click (keyboard, mouse, whatever) but respond before the launch of the long thread.


If you could solve the issue, let's tell me.
