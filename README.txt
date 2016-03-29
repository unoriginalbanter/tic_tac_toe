#tic_tac_toe
=======================
tic_tac_toe from BANTER
=======================

Version v0.1.0

Basics
======
Tic_tac_toe is a basic project, but I wanted to try something of variable
grid size, and see if I can code a <find winner> method for such a grid. It
was a lot of fun doing this, but admitidly, the most frustrating part of the
whole enterprise was getting an output-to-terminal interface that was readable 
and coherent, AND that respected grid size.

Originally, I had inteded to have a super snarky UI. As it stands, UI is mild
snark.

tic_tac_toe shouldn't have to be installed, so no setup.py was included. If 
you need to run main.py as an executable, just "chmod +x main.py", and change
the shebang line ("#!/usr/...") as fits your specific filesystem, as is, it 
should be fine for python3.5 on a Unix-based or Unix-like OS. If not, you can
run 
    python3.5 main.py
after a quick cd into the tic_tac_toe package page. 

What's Next
===========
 - AI to implement the computer solution to the game (so that the computer 
   should never lose.
 - Terminal UI should get better at catching errors from input. The interface
   module will really only work for a nice user (users are never nice irl).
   
