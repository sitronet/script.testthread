
This script is for testing the pyxbmct lib for Kodi whith threads
* it is not working as I should like*

Description :
there is a simple main programm , in this main prog the initial steps are :
Create 4 effectives buttons (start, pause, resume and stop) and one textbox.

The goal is : to start a long process computational with the start button.
pause the long process with the pause button, resume with the resume button, etc...
and stop the program with the stop button.
The long process is a simple loop (while or for) and print in the textbox a message for each turn of the loop

the long process could be inside the main program or in a separate thread ,
just define a boolean flag on the beginning of the code to try either one or the other.

The program doesn't work as my wish because once the long process started the button have no action.
the buttons don't respond to the click (keyboard, mouse, whatever)

If you could solve the issue, let's tell me.
