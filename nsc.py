
import card_drawer
import constants
reload(constants)

import json
import os
import os.path
import sys
import optparse
from pygame.locals import *

output_target = constants.OT_HOME
# True: don't rotate the cards for printing
horizontal_cards = False

def main(options, args):
	skip_sheets = options.skip_sheets
	save_pdf = options.save_pdf
	if save_pdf and skip_sheets:
		print("!!! Cannot save PDFs and use the --skip_sheets option!")

	# If desired_cards is empty, all cards discovered will be included.
	# Otherwise, only cards with names in the list will be included.
	# Similarly for desired_types.
	desired_cards = options.desired_cards
	desired_types = options.desired_types

	# Get card info from files
	card_files = os.listdir(constants.INPUT_DIR)
	all_cards = []
	cards = []
	input_files = options.input_files
	if input_files:
		desired_card_files = []
		for card_file in card_files:
			if card_file in input_files:
				desired_card_files += [card_file]
	else:
		desired_card_files = card_files
	for card_file in desired_card_files:
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
		template_info["name"] = template_file[:-5]
		templates[template_info["name"]] = template_info

	# Get font info
	fonts = {}
	file = open(constants.FONTS_FILE)
	fonts_info = json.load(file)

	cd = card_drawer.CardDrawer(templates, fonts_info, output_target)
	
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

		if not skip_sheets:
			cards = cd.drawSheet(cards)
			card_drawer.pygame.display.update()
			if len(cards) == 0:
				if save_pdf:
					cd.writePDF()
				card_drawer.pygame.quit()
				sys.exit()
		else:
			card_drawer.pygame.quit()
			sys.exit()

if __name__ == "__main__":
	parser = optparse.OptionParser(usage="""%prog [options]
Nothing Sacred Cards - Create and rapidly iterate cards while designing board game.""",
			version = "%prog 1.0")
	parser.add_option("-s", "--skip_sheets", dest="skip_sheets", action="store_true", help="Do not generate sheets of cards after creating cards. Note: Do not use this option if you'd like to generate pdfs.", default=False)
	parser.add_option("-p", "--pdf", dest="save_pdf", action="store_true", help="Generate a pdf of all cards for printing. Note: Will not work if sheets are skipped.", default=False)
	parser.add_option("-c", "--card", dest="desired_cards", action="append", help="The name of a card to generate. Can be used multiple times to generate multiple cards. If none specified, all cards will be generated.")
	parser.add_option("-t", "--type", dest="desired_types", action="append", help="The type of card to generate. Can be used multiple times to generate multiple types of cards. If none specified, all types will be generated.")
	parser.add_option("-i", "--input_file", dest="input_files", action="append", help="The input file (in the cards/ directory) to use for generating cards. Can be used multiple times to get cards from multiple input files. If none specified, all .json files in the cards/ directory will be used.")

	(options, args) = parser.parse_args()

	sys.exit(main(options, args))

