
# print_fonts
# Prints out a list of fonts installed on your system.
# Use to fill out your font file.
# MAX is the maximum number of fonts to print out.
#   (decrease to see only the first MAX fonts in case output is too long.)

import pygame

MAX = 1000
count = 0

pygame.init()

fs = pygame.font.get_fonts()
fs.sort()

for f in fs:
	print(f)
	count += 1
	if count > MAX:
		break

