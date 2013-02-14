
import card_drawer
import constants
reload(constants)

import json
import os
import os.path
import sys
from pygame.locals import *

output_target = constants.OT_HOME
# True: don't rotate the cards for printing
horizontal_cards = False

def main():
	save_pdf = False

	# If desired_cards is empty, all cards discovered will be included.
	# Otherwise, only cards with names in the list will be included.
	# Similarly for desired_types (use constants.TYPES[type] for legal strings).
	desired_cards = []
	desired_types = ["playing_card", "face_card"]

	# Get card info from files
	card_files = os.listdir(constants.INPUT_DIR)
	all_cards = []
	cards = []
	for card_file in card_files:
		if card_file[0] == "." or card_file[-1] == "~":
			continue
		file = open(os.path.join(constants.INPUT_DIR, card_file))
		cards_info = json.load(file)
		for card_info in cards_info:
			if not desired_cards or card_info["name"] in desired_cards:
				if not desired_types or card_info["type"] in desired_types:
					all_cards += [card_info]
					if "number" in card_info.keys():
						cards += [card_info] * card_info["number"]
					else:
						cards += [card_info]

	# Get template info
	templates = {}
	template_files = os.listdir(constants.TEMPLATE_DIR)
	for template_file in template_files:
		if template_file[0] == "." or template_file[-1] == "~":
			continue
		file = open(os.path.join(constants.TEMPLATE_DIR, template_file))
		template_info = json.load(file)
		templates[template_info["name"]] = template_info

	# Get type map
	file = open(constants.TYPE_MAP_FILE)
	type_map_info = json.load(file)

	# Get font info
	fonts = {}
	file = open(constants.FONTS_FILE)
	fonts_info = json.load(file)

	cd = card_drawer.CardDrawer(templates, type_map_info, fonts_info, output_target)
	
	while True:
		for event in card_drawer.pygame.event.get():
			if event.type == QUIT:
				card_drawer.pygame.quit()
				sys.exit()

			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					card_drawer.pygame.quit()
					sys.exit()
				elif event.key == ord('p'):
					cd.printToFile()

		if len(all_cards) > 0:
			cd.drawCards(all_cards)
			all_cards = []

		cards = cd.drawSheet(cards)
		card_drawer.pygame.display.update()
		if len(cards) == 0:
			if save_pdf:
				cd.writePDF()
			card_drawer.pygame.quit()
			sys.exit()

if __name__ == "__main__":
	main()

