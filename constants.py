
import os.path

ROOT_DIR = os.path.join('c:\\', 'projects', 'nsc')
ART_DIR = os.path.join(ROOT_DIR, 'art')
INLINE_DIR = os.path.join(ART_DIR, 'inline')
FULL_DIR = os.path.join(ART_DIR, 'full')
BACKGROUND_DIR = os.path.join(ART_DIR, 'background')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
INPUT_DIR = os.path.join(ROOT_DIR, 'json')
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')

TYPE_MAP_FILE = os.path.join(ROOT_DIR, 'type_map.json')
FONTS_FILE = os.path.join(ROOT_DIR, 'fonts.json')

WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (66, 66, 66)
RED = (226, 31, 31)
GREEN = (0, 0xFF, 0)
BLUE = (68, 174, 227)
YELLOW = (255, 222, 0)
GREY = (0x99, 0x99, 0x99)
LIGHT_GREY = (0xCC, 0xCC, 0xCC)
OFF_WHITE = (0xEE, 0xEE, 0xEE)
VERY_LIGHT_GREY = (0xDD, 0xDD, 0xDD)
ALMOST_LIGHT_GREY = (0xC0, 0xC0, 0xC0)
ACTUAL_BLACK = (0, 0, 0)

COLOR_MAP = {"white": WHITE,
		"black": ACTUAL_BLACK,
		"red": RED,
		"green": GREEN,
		"blue": BLUE,
		"yellow": YELLOW,
		"grey": GREY}

POKER_WIDTH = 2.5
POKER_HEIGHT = 3.5
MINI_WIDTH = 1.75
MINI_HEIGHT = 2.5

# Output targets
OT_HOME = 'home_printer'
OT_TGC = 'the_game_crafter'

