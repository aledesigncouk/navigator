__version__ = '0.3'
__author__ = 'Alessio Deidda / Cecilia Baggini'

mainWindow = 'QMainWindow { background: #000000 url("imgs/main_bg.gif") center left no-repeat; }'
cameraWindow = 'QWidget { background: #000000; }'
playerWindow = 'QWidget { background: #ffffff; } '

btn_H = 'QPushButton { height: 256px; width: 128px; border: none;'
btn_V = 'QPushButton { height: 128px; width: 256px; border: none;'

btn_quit = btn_H + ' background: url("imgs/quit-icon.png") center no-repeat; }'
btn_navit = btn_H + ' background: url("imgs/navit-icon.png") center no-repeat; }'
btn_camera = btn_H + ' background: url("imgs/camera-icon.png") center no-repeat; }'
btn_sensors = btn_H + ' background: url("imgs/sensors-icon.png") center no-repeat; }'
btn_back = btn_V + ' background: url("imgs/back-icon.png") center no-repeat; }'

### NOTES: set a common style when required, maybe a string variable that can be attached