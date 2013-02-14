
# CardDrawer
# A class to draw cards for printing purposes.

import constants

import datetime
import pygame
import os
import os.path
import string

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class CardDrawer:
	pygame_init = False
	window_surface = None
	ot = None

	# The relationship between types and templates found in type_map.json
	type_map = {}
	templates = {}

	start_x = 0
	start_y = 0

	window_width_inches = 8.5
	window_height_inches = 11
	resolution = 300.0

	window_width = int(window_width_inches * resolution)
	window_height = int(window_height_inches * resolution)

	text_margin = 8
	normal_margin = 15
	line_width = 3
	quarter_inch = resolution / 8

	raw_card_width = 2.5
	raw_card_height = 3.5
	raw_safe_margin = .125
	card_width = raw_card_width * resolution
	card_height = raw_card_height * resolution
	safe_margin = raw_safe_margin * resolution

	out_dir = ""
	pdf_file = ""
	inline_images = {}
	full_images = {}
	background_images = {}

	text_height = 0
	space_image = None
	space_width = 0

	sheets = 0

	drawn_cards = []

	def __init__(self, templates={}, type_map={}, fonts={}, output_target=None):
		if not self.pygame_init:
			self.initPygame()

		self.ot = output_target
		if self.ot == None:
			self.ot = constants.OT_HOME

		self.templates = templates
		self.type_map = type_map

		if not fonts:
			self.fonts_info = {"name":"default", "font":"garamond", "size":64}
		else:
			self.fonts_info = fonts

		self.initialize()

	# drawCards
	# Draws a bunch of cards
	def drawCards(self, cards=[]):
		self.changeSize(self.card_width, self.card_height)

		for c in cards:
			if c["name"] not in self.drawn_cards:
				self.window_surface.fill(constants.WHITE)
				self.drawCard(c)
				self.drawn_cards += [c["name"]]

	# drawSheet
	# Draws a sheet of cards
	# Returns the cards not included
	def drawSheet(self, cards=[], input_dir=None, raw_card_names=False):
		if not input_dir:
			input_dir = self.out_dir

		self.changeSize(self.window_width, self.window_height)
		self.window_surface.fill(constants.WHITE)

		row_cards = int(self.window_height / self.card_width)
		col_cards = int(self.window_width / self.card_height)

		start_x = 0
		x = start_x
		cards_r = 0
		start_y = 0
		y = start_y
		cards_c = 0
		card_count = 0
		seen_cards = []

		for c in cards:
			if raw_card_names:
				image = pygame.image.load(input_dir + "\\" + c)
			else:
				image = pygame.image.load(input_dir + "\\" + self.convertName(c["name"]) + ".png")
			# if not self.horizontal_cards:
			image = pygame.transform.rotate(image, 90)
			self.window_surface.blit(image, (x, y))
			seen_cards += [c]

			y += self.card_width
			cards_r += 1
			if cards_r == row_cards:
				y = start_y
				cards_r = 0
				x += self.card_height
				cards_c += 1
			card_count += 1
			if cards_c == col_cards:
				break

		pygame.display.update()
		if self.sheets in range(0, 10):
			num_string = "0" + str(self.sheets)
		else:
			num_string = str(self.sheets)
		self.printToFile(self.out_dir + '\\sheet' + num_string + '.png')
		self.sheets += 1

		return cards[card_count:]

	def convertName(self, name):
		name = "_".join(name.split(" "))
		name = "".join(name.split("?"))
		name = "".join(name.split("&"))
		return name

	# getText
	# Returns the text for a block based on a particular card.
	def getText(self, card=None, block=None):
		words = block["content"].split(" ")
		replaced_words = []
		for word in words:
			if len(word) > 0:
				# Handle special characters
				if word[0] == "\\":
					code = word[1:]
					if code in card.keys():
						replaced_words += [card[code]]
					else:
						replaced_words += [word]
				else:
					replaced_words += [word]
		return " ".join(replaced_words)

	# drawBlock
	# Draws a template block for the given card, returning a link to the file.
	def drawBlock(self, card=None, block=None, template=None):
		print("  Drawing block: " + block["name"])

		bg_image = None
		if "background_image" in block.keys():
			bg_name = block["background_image"]
			bg_image = self.getBackground(bg_name)
		
		if "width" not in block.keys():
			if bg_image:
				self.block_width = bg_image.get_width()
			else:
				self.block_width = self.safe_card_width
		else:
			self.block_width = block["width"]
		if "height" not in block.keys():
			if bg_image:
				self.block_height = bg_image.get_height()
			else:
				self.block_height = self.safe_card_height
		else:
			self.block_height = block["height"]

		if "align_x" not in block.keys():
			self.align_x = "left"
		else:
			self.align_x = block["align_x"]
		if "align_y" not in block.keys():
			self.align_y = "top"
		else:
			self.align_y = block["align_y"]

		if "rotation" not in block.keys():
			self.block_rotation = 0
		elif block["rotation"] == 180:
			self.block_rotation = 180
		else:
			self.block_rotation = 0

		# Determine position on card for block location reference
		default_pos_x = self.start_x + self.safe_margin
		if "pos_x" not in block.keys():
			self.pos_x = default_pos_x
		else:
			pos_x = block["pos_x"]
			if pos_x == "flush_left":
				self.pos_x = self.start_x
			elif pos_x == "left":
				self.pos_x = self.start_x + self.safe_margin
			elif pos_x == "center":
				self.pos_x = int(self.card_width / 2) + self.start_x
			elif pos_x == "right":
				self.pos_x = self.start_x + self.card_width - self.safe_margin
			elif pos_x == "flush_right":
				self.pos_x = self.start_x + self.card_width
			else:
				self.pos_x = pos_x
		default_pos_y = self.start_y + self.safe_margin
		if "pos_y" not in block.keys():
			self.pos_y = default_pos_y
		else:
			pos_y = block["pos_y"]
			if pos_y == "flush_top":
				self.pos_y = self.start_y
			elif pos_y == "top":
				self.pos_y = self.start_y + self.safe_margin
			elif pos_y == "center":
				self.pos_y = int(self.card_height / 2) + self.start_y
			elif pos_y == "bottom":
				self.pos_y = self.start_y + self.card_height - self.safe_margin
			elif pos_y == "flush_bottom":
				self.pos_y = self.start_y + self.card_height
			else:
				self.pos_y = pos_y

		# Determine anchor point
		default_ax = self.pos_x
		if "anchor_x" not in block.keys():
			pos_x = default_ax
		else:
			ax = block["anchor_x"]
			if ax == "left":
				pos_x = self.pos_x
			elif ax == "center":
				pos_x = self.pos_x - int(self.block_width / 2)
			elif ax == "right":
				pos_x = self.pos_x - self.block_width
			else:
				pos_x = self.pos_x - ax
		default_ay = self.pos_y
		if "anchor_y" not in block.keys():
			pos_y = default_ay
		else:
			ay = block["anchor_y"]
			if ay == "top":
				pos_y = self.pos_y
			elif ay == "center":
				pos_y = self.pos_y - int(self.block_height / 2)
			elif ay == "bottom":
				pos_y = self.pos_y - self.block_height
			else:
				pos_y = self.pos_y - ay

		if "color" in block.keys():
			if "actual_color" not in block.keys():
				block["actual_color"] = self.getColor(block["color"])
			color = block["actual_color"]
		else:
			color = template["actual_color"]

		if "background_color" in block.keys():
			background_color = self.getColor(block["background_color"])
			pygame.draw.rect(self.window_surface, background_color, pygame.Rect(pos_x, pos_y, self.block_width, self.block_height))

		# Render background image
		if bg_image:
			if self.block_rotation == 180:
				bg_image = pygame.transform.rotate(bg_image, 180)
			bg_x = pos_x + (self.block_width - bg_image.get_width()) / 2
			bg_y = pos_y + (self.block_height - bg_image.get_height()) / 2
			self.window_surface.blit(bg_image, (bg_x, bg_y))

		# Render content of block
		text = self.getText(card, block)
		font = "default"
		self.renderText(text, start_x=pos_x, start_y=pos_y, color=color, width=self.block_width, height=self.block_height, font=font, align=self.align_x, v_align=self.align_y, rotation=self.block_rotation, card=card)

	# drawCard
	# Draws a card for printing
	def drawCard(self, card=None):
		if not card:
			return

		# Check card
		if "name" not in card.keys():
			print("!!! No name found for " + str(card))
			return
		print("Drawing card: " + card["name"])
		if "type" not in card.keys():
			print("!!! No type found for " + str(card))
			return

		# Find template
		if card['type'] not in self.type_map.keys():
			print("!!! Could not find type_map entry for type " + card['type'])
			return
		template_name = self.type_map[card['type']]
		if template_name not in self.templates.keys():
			print("!!! Could not find template " + template_name)
			return
		template = self.templates[template_name]
		if "blocks" not in template.keys():
			print("!!! No blocks for tempalte " + template_name)
			return
		blocks = template["blocks"]

		self.setDimensions(template)

		# Draw card edge
		pygame.draw.rect(self.window_surface, constants.LIGHT_GREY, pygame.Rect(self.start_x, self.start_y, self.card_width, self.card_height))

		# Draw inner border
		if "border_color" in template.keys():
			border_color = self.getColor(template["border_color"])
			border_x = self.start_x + self.line_width
			border_y = self.start_y + self.line_width
			border_width = self.card_width - 2 * self.line_width
			border_height = self.card_height - 2 * self.line_width
			pygame.draw.rect(self.window_surface, border_color, pygame.Rect(border_x, border_y, border_width, border_height))

			body_x = border_x + self.safe_margin - self.line_width
			body_y = border_y + self.safe_margin - self.line_width
			body_width = border_width - 2 * (self.safe_margin - self.line_width)
			body_height = border_height - 2 * (self.safe_margin - self.line_width)
		else:
			body_x = self.start_x + self.line_width
			body_y = self.start_y + self.line_width
			body_width = self.card_width - 2 * self.line_width
			body_height = self.card_height - 2 * self.line_width


		# Draw card body
		if "background_color" in template.keys():
			background_color = self.getColor(template["background_color"])
		else:
			background_color = constants.WHITE
		pygame.draw.rect(self.window_surface, background_color, pygame.Rect(body_x, body_y, body_width, body_height))

		# Draw background image
		bg_image_name = None
		if "background_image" in card.keys():
			bg_image_name = card["background_image"]
		elif "background_image" in template.keys():
			bg_image_name = template["background_image"]
		if bg_image_name:
			image = self.getBackground(bg_image_name)
			if image:
				bg_x = self.start_x + (self.card_width - image.get_width()) / 2
				bg_y = self.start_y + (self.card_height - image.get_height()) / 2
				self.window_surface.blit(image, (bg_x, bg_y))

		# Determine default color
		if "actual_color" not in template.keys():
			if "color" in template.keys():
				template["actual_color"] = self.getColor(template["color"])
			else:
				template["actual_color"] = constants.ACTUAL_BLACK

		# Draw each block
		for block in blocks:
			if "content" not in block.keys():
				print("!!! No content defined for " + str(block))
				block["content"] = ""
			block["image_path"] = self.drawBlock(card, block, template)

		# Print card
		pygame.display.update()
		self.printToFile(self.out_dir + "\\" + self.convertName(card["name"]) + '.png')
		print("")

	def drawLine(self, x=0, y=0, length=0, horizontal=True, color=None, width=-1):
		if not color:
			color = constants.ACTUAL_BLACK
		if width < 0:
			width = self.line_width

		if horizontal:
			pygame.draw.rect(self.window_surface, color, pygame.Rect(x, y, length, width))
		else:
			pygame.draw.rect(self.window_surface, color, pygame.Rect(x, y, width, length))

	# renderText
	# Renders the given text, handling multiple lines, special characters,
	#   and images.
	# Returns the height of the text block.
	def renderText(self, text, start_x=0, start_y=0, color=None, width=None, height=0, actually_render=True, draw_images=True, font=None, line_space=None, align="left", v_align="top", rotation=0, allow_styling=True, card=None):
		# Setup defaults
		if color == None:
			color = constants.ACTUAL_BLACK
		if font == None:
			font = 'rules'
		if line_space == None:
			line_space = self.text_margin

		# Define space images
		space_image = self.fonts[font].render(" ", True, constants.ACTUAL_BLACK)

		# Initialize variables
		x = start_x
		images = []
		cur_width = 0
		text_buffer = self.normal_margin
		total_height = 0
		# basic_height = self.fonts[font].size(" ")[1]
		basic_height = self.safe_margin
		cur_height = basic_height
		blank_line = True
		words = text.split(" ")
		rule_count = 0
		lines = []

		# Handle actual rendering
		for word in words:
			# Initialize word specific variables
			y_offset = text_buffer
			keyword = False
			revert_bold = False
			revert_italic = False
			render_rule = False
			modified_word = ""
			# Make sure we have an actual word
			if len(word) > 0:
				# Handle special characters
				if word[0] == "\\":
					code = word[1:]
					codes = code.split(":")
					if len(codes) == 2:
						command = codes[0]
						code = codes[1]
						if command == "img":
							if not card:
								print("!!! Card not included for text render!")
								code = None
							elif code in card.keys():
								if card[code][0] == "\\":
									code = card[code][1:]
					# End of Line
					if code == "n":
						lines += [{"width":cur_width, "height":cur_height, "align":align, "images":images}]
						images = []
						x = start_x
						total_height += cur_height
						cur_height = basic_height
						cur_width = 0
						continue
					# Bold
					elif code == "b":
						if allow_styling:
							self.fonts[font].set_bold(not self.fonts[font].get_bold())
						continue
					# Italic
					elif code == "i":
						if allow_styling:
							self.fonts[font].set_italic(not self.fonts[font].get_italic())
						continue
					# Inline
					elif code in self.inline_images.keys():
						image = self.getInline(code)
						y_offset = 0
					# Full
					elif code in self.full_images.keys():
						image = self.getFull(code)
						image_x = start_x + (width - image.get_width()) / 2
						if cur_width != 0:
							lines += [{"width":cur_width, "height":cur_height, "align":align, "images":images}]
							images = []
						lines += [{"width":image.get_width(), "height":image.get_height(), "align":"center", "images":[image]}]
						x = start_x
						if cur_width == 0:
							total_height += image.get_height() + self.normal_margin
						else:
							total_height += cur_height + image.get_height() + self.normal_margin
						cur_height = basic_height
						cur_width = 0
						continue
				# Handle writing a word
				else:
					image = self.fonts[font].render(word, True, color)

				image_width = image.get_width()
				image_height = image.get_height()

				# Handle line wrapping
				if width:
					if cur_width + image_width >= width:
						lines += [{"width":cur_width, "height":cur_height, "align":align, "images":images}]
						images = []
						x = start_x
						total_height += cur_height
						cur_height = basic_height
						cur_width = 0

				# Draw image
				total_width = image_width
				if cur_width > 0:
					images += [space_image]
					total_width += self.space_width
				images += [image]

				# Update position for next image
				x += total_width
				cur_width += total_width
				if image_height > cur_height:
					cur_height = image_height

		# Draw remaining images after processing the last word
		last_align = align
		if align == "justified":
			last_align = "left"
		lines += [{"width":cur_width, "height":cur_height, "align":last_align, "images":images}]

		if cur_width > 0:
			total_height += cur_height

		# Actually render images, one line at a time.
		if actually_render:
			# Determine y based on vertical alignment
			y = start_y
			if v_align == "center" or v_align == "bottom":
				if v_align == "center":
					y = y + (height - (total_height + (len(lines) - 1) * line_space)) / 2
				if v_align == "bottom":
					y = y + height - (total_height + (len(lines) - 1) * line_space)
			if rotation == 180:
				lines.reverse()
			fs_y = y
			for line in lines:
				draw_x = self.determineStartX(start_x, line["width"], line["align"], width)
				if rotation == 180:
					line["images"].reverse()
				self.renderImages(line["images"], (draw_x, y), width=width, space_image=space_image, align=line["align"], rotation=rotation)
				y += line["height"] + line_space

		if self.fonts[font].get_bold():
			print("!!! Font left bold: " + text)
		if self.fonts[font].get_italic():
			print("!!! Font left italic: " + text)

		return total_height

	# determineStartX
	# Returns the x value of where a line should start to be rendered
	def determineStartX(self, start_x, cur_width, align, width):
		if align == "center":
			return start_x + (width - cur_width) / 2
		elif align == "right":
			return start_x + width - cur_width
		else:
			return start_x

	# renderImages
	# Render a collection of images starting at (x, y), centered vertically.
	def renderImages(self, images, (x, y), width=0, space_image=None, align="left", rotation=0):
		total_height = 0
		cur_x = x
		cur_y = y

		# Handle justify spaces
		if align == "justify":
			image_width = 0
			image_count = 0
			for image in images:
				if image != space_image:
					image_width += image.get_width()
					image_count += 1
			space_width = (width - image_width) / (image_count - 1)

		# Find the total height
		for image in images:
			if image.get_height() > total_height:
				total_height = image.get_height()

		# Render images
		for image in images:
			if align != "justify" or image != space_image:
				if rotation == 180:
					image = pygame.transform.rotate(image, 180)
				self.window_surface.blit(image, (cur_x, cur_y + (total_height - image.get_height()) / 2))
				cur_x += image.get_width()
				if align == "justify":
					cur_x += space_width

	# trim
	# Remove unwanted details from a word.
	# Removes case and end punctuation.
	def trim(self, word):
		modified_word = word.lower()
		if modified_word[-1] in string.punctuation:
			modified_word = modified_word[:-1]
		return modified_word

	# setDimensions
	# Sets the size of the card based on the given template
	def setDimensions(self, template):
		if "size" in template.keys():
			size = template["size"]
			if size == "poker":
				self.raw_card_width = constants.POKER_WIDTH
				self.raw_card_height = constants.POKER_HEIGHT
			elif size == "mini":
				self.raw_card_width = constants.MINI_WIDTH
				self.raw_card_height = constants.MINI_HEIGHT
			else:
				self.raw_card_width = constants.POKER_WIDTH
				self.raw_card_height = constants.POKER_HEIGHT
		else:
			self.raw_card_width = constants.POKER_WIDTH
			self.raw_card_height = constants.POKER_HEIGHT
		self.card_width = self.raw_card_width * self.resolution
		self.card_height = self.raw_card_height * self.resolution
		self.safe_card_width = self.card_width - 2 * self.safe_margin
		self.safe_card_height = self.card_height - 2 * self.safe_margin
		self.changeSize(self.card_width, self.card_height)

	# writePDF
	# Compiles all of the pngs into a single pdf for printing!
	def writePDF(self, back=None):
		if back != None:
			back = back + constants.SHEET_BACK_POSTFIX
		pdf_resolution = 72.0
		resolution_converstion = self.resolution / pdf_resolution
		pdf_margin = .5
		page_size = (resolution_converstion * (letter[0] - .9 * pdf_margin * pdf_resolution), resolution_converstion * (letter[1] - .9 * pdf_margin * pdf_resolution))
		pdf_x_offset = pdf_margin * pdf_resolution
		pdf_y_offset = -4 * pdf_margin * pdf_resolution
		back_pdf_y_offset = pdf_margin * pdf_resolution
		c = canvas.Canvas(self.out_dir + '\\cards.pdf', pagesize=page_size)

		pngs = os.listdir(self.out_dir)
		for f in pngs:
			if f[-4:] == '.png' and f[:5] == "sheet":
				c.drawImage(os.path.join(self.out_dir, f), pdf_x_offset, pdf_y_offset)
				c.showPage()
				if back != None:
					c.drawImage(os.path.join(constants.ART_DIR, back), 0, back_pdf_y_offset)
					c.showPage()

		c.save()

	def getInline(self, image='none'):
		if image not in self.inline_images.keys():
			print("!!! Unknown image: " + image)
			image = 'none'
		image = self.inline_images[image]
		return image

	def getFull(self, image='none'):
		if image not in self.full_images.keys():
			print("!!! Unknown image: " + image)
			image = 'none'
		image = self.full_images[image]
		return image

	def getBackground(self, image='none'):
		if image not in self.background_images.keys():
			print("!!! Unknown background image: " + image)
			image = 'none'
			return None
		image = self.background_images[image]
		return image

	# getColor
	# Returns a color based on the color word.
	def getColor(self, color):
		if color in constants.COLOR_MAP.keys():
			return constants.COLOR_MAP[color]
		if color[0] == "(":
			color = color[1:]
		if color[-1] == ")":
			color = color[:-1]
		colors = color.split(", ")
		if len(colors) == 1:
			colors = colors[0].split(",")
		if len(colors) != 3:
			print("!!! Illegal color: " + str(colors))
			return constants.WHITE
		red = self.toInt(colors[0])
		green = self.toInt(colors[1])
		blue = self.toInt(colors[2])
		return (red, green, blue)

	# toInt
	# Returns the integer value of a string, whether in base 10 or 16.
	def toInt(self, string):
		if len(string) < 3 or string[0:2] != "0x":
			return int(string)
		else:
			return int(string, 16)

	# printToFile
	# Prints the sheet to a file so it can be printed.
	def printToFile(self, path):
		pygame.image.save(self.window_surface, path)

	# initialize
	# Sets up the images used in the game and the constants used for drawing.
	def initialize(self):
		# Setup Images
		inline_files = os.listdir(constants.INLINE_DIR)
		for inline_file in inline_files:
			if inline_file[0] == "." or inline_file[-1] == "~":
				continue
			image_name = '.'.join(inline_file.split('.')[:-1])
			self.inline_images[image_name] = pygame.image.load(os.path.join(constants.INLINE_DIR, inline_file))

		full_files = os.listdir(constants.FULL_DIR)
		for full_file in full_files:
			if full_file[0] == "." or full_file[-1] == "~":
				continue
			image_name = '.'.join(full_file.split('.')[:-1])
			self.full_images[image_name] = pygame.image.load(os.path.join(constants.FULL_DIR, full_file))

		background_files = os.listdir(constants.BACKGROUND_DIR)
		for background_file in background_files:
			if background_file[0] == "." or background_file[-1] == "~":
				continue
			image_name = '.'.join(background_file.split('.')[:-1])
			self.background_images[image_name] = pygame.image.load(os.path.join(constants.BACKGROUND_DIR, background_file))

		# Update sizes based on output target
		if self.ot == constants.OT_TGC:
			self.old_resolution = self.resolution
			self.resolution = 300.0
			self.resolution_scale = self.resolution / self.old_resolution

			self.window_width = int(self.window_width_inches * self.resolution)
			self.window_height = int(self.window_height_inches * self.resolution)

			self.text_margin = int(self.text_margin * self.resolution_scale)
			self.normal_margin = int(self.normal_margin * self.resolution_scale)
			self.line_width = int(self.line_width * self.resolution_scale)

			self.card_width = self.raw_card_width * self.resolution
			self.card_height = self.raw_card_height * self.resolution
			self.changeSize(self.card_width, self.card_height)

			for f in self.fonts:
				f['size'] *= int(self.resolution_scale)

		# Setup Fonts
		self.fonts = {}
		for f in self.fonts_info:
			self.fonts[f["name"]] = pygame.font.Font(pygame.font.match_font(f["font"]), f["size"])

		# Setup Basic Strings
		text = " "
		size = self.fonts['default'].size(text)
		self.text_height = size[1]
		self.space_width = size[0]
		self.space_image = self.fonts['default'].render(text, True, constants.ACTUAL_BLACK)

		# Make output folder
		n = datetime.datetime.today()
		self.out_dir = constants.OUTPUT_DIR + '\\' + str(n.year) + '_' + str(n.month) + '_' + str(n.day) + '_' + str(n.hour) + '_' + str(n.minute) + '_' + str(n.second)
		os.mkdir(self.out_dir)

	def changeSize(self, width, height):
		self.window_surface = pygame.display.set_mode((int(width), int(height)), 0, 32)

	def initPygame(self):
		pygame.init()

		self.changeSize(self.card_width, self.card_height)

		self.pygame_init = True

