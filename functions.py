__version__ = '0.3'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import subprocess

# Navit
def startNavit():
    app = '/usr/bin/navit'
    subprocess.Popen([app])
    
# dash camera, set mplayer to write a file in cycle
def dashCam():
    subprocess.run(['mplayer', '-fs', 'tv:///dev/video0'])