# KKengraver Enhanced
A command line tool for a KKMoon laser engraver, improved version based on aquamorta's kkengraver

# Description of the engraver software

This software is intended to be used with a KKMoon laser engraver (3000mW).
It comes with ABSOLUTELY NO WARRANTY. It may or may not work with an other kind of
laser engraver.

## Preliminaries

First I have to thank aquamorta for the [aquamorta's kkengraver](https://github.com/aquamorta/kkengraver), a great Python program this script is based on.
I wanted to be able to engrave  and cut test samples with variing power, depth and amount of cutting passes. 

So this software does two thing:

1. Engrave tests with variing power and depth settings
2. Cutting tests with variing amount of cutting passes

## How to run

1. Start TEST1.py
2. Select if you want to actively engrave/cut or only use dummy movements and low-power drawing frames
3. Select COM port from selection list (only works with Windows)
4. Select desired testing mode from test menu options
5. Check and confirm if drawing frame is centered on test piece correctly
6. Wait until test is finished and observe progress via webcam (if installed for viewing progress)

<p float="left">
 <img src="https://github.com/Alasterer/kkengraver_enhanced/blob/main/Laser_Engraver_Test_Templates_v4.jpg" height="900"/>
</p>
