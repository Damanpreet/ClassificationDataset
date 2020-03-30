from easydict import EasyDict as edict

config = edict()

config.RGB_DIR = 'JPEG/'
config.OUTPUT = 'output/'

# configuration for 3X4 grid.
config.CROP_DIMS = (250, 350, 1750, 1450) #tw, th, bw, bh
config.GRIDW = 4
config.GRIDH = 3

# gray is background - to identify missing explants
# green and brown - explant
# white, pink, yellow, orange, black - contamination
classes = {(128,128,128):0, (0, 255, 0):1, (150,75,0):1, (181,101,29):1, (187,144,103):1, (255,255,0):2, (255,69,0):2, (0,0,0):2, (255,255,255):2}