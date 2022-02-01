
## Nothing Sacred Cards

Nothing Sacred Cards is card generation software. It is designed for designers who are rapidly iterating on games with cards, NOT for creating final, polished versions.

Nothing Sacred Cards offers the following awesome features:

Keep everything in text files! Source control it, search it, and easily change your card text, instead of keeping them in awkward formats like Photoshop.

Separate content and presentation! Keep your card information in one file, and tell Nothing Sacred Cards how to display that information in a separate file. That means you can experiment with different card layouts rapdily without messing with the actual content of the cards.

Automate card layout! Nothing Sacred Cards takes card content and your layout specifications to generate card images with one button. Instantly get testable cards in a single PDF file, ready for printing!

Inline images! Freely mix symbols and text to make your cards as easy to read as possible. Want to change a symbol or image later? No problem! Just change the image file and re-generate all of the cards!


## Requirements

Nothing Sacred Cards is written in Python and makes use of the Pygame and ReportLab libraries.

1. Install Python 2.7.
	1. Download Python 2.7 here: http://python.org/download/

2. Install Pygame
	1. Download Pygame here: http://www.pygame.org/download.shtml
	2. Make sure you get the most recent version for python 2.7.

3. Install ReportLab
	1. Download ReportLab here: http://www.reportlab.com/software/opensource/rl-toolkit/download/
	2. Make sure you get the most recent version for python 2.7.
	3. To use .png files, you will need the Python Imaging Library, which you can get here: http://www.pythonware.com/products/pil/

*Mac note:* I don't know much about macs, and ReportLab seems to suck on it! Here are three possible solutions:
	
	1. Install ReportLab on your mac following these nasy directions:
	http://two.pairlist.net/pipermail/reportlab-users/2009-May/008351.html
	2. One of my testers was kind enough to create a list of the steps he used to get ReportLab setup on his machine.
	You can follow them here: https://github.com/tealefristoe/nsc/wiki/OS-X-Instructions
	3. Do not bother with creating PDFs. This makes printing much more annoying, but at least you can generate cards.
	To do this:	
		a. Comment out lines 13 and 14 from card_drawer.py (put a # at the beginning of those lines).
		b. Make sure you do not use the -p option when running Nothing Sacred Cards.

4. Setup path variables to access Python from the command line. (Instructions for windows... for mac and linux, I don't think you need to do this, but you might need to do some internet research.)
	1. Right click on My Computer and select properties.
	2. Choose Advanced system settings.
	3. Click continue if a permission window pops up.
	4. Click the Environment Variables button.
	5. Under System variables, select PATH and click the Edit... button.
	6. At the end of the Variable value string, add ";C:\Python27" (or the directory you chose to install python into if something else).
	7. Push OK on the Edit System Variable window.
	8. Push OK on the Environment Variables window.
	9. Push OK on the System Properties window.

5. Unzip Nothing Sacred Cards into the directory of your choice. I recommend a directory without spaces, like c:\games\nsc.


## Running Nothing Sacred Cards

Now that the prerequisites are installed and NSC has been set up, it's time to test it to make sure everything is working!

1. Navigate to your NSC directory.

2. Open a command prompt in your NSC directory.
	1. Make sure no files are highlighted in your NSC directory and shift + right click somewhere on the window (make sure you don't accidentally right click on a file).
	2. Select Open Command Window Here.

3. This is a command prompt, where you're able to give the computer commands in text form. Woah. It may look scary, like the matrix, but it's really not so bad!

4. In the command prompt, type "python nsc.py -i playing_cards.json" (without the quotes), then push Enter.

5. You should see text scroll up on the command window, and you should see flashes of cards in a new window, followed by flashes of sheets of cards. If this doesn't happen, something went wrong! Thankfully, that friendly command prompt should tell you if there are any errors, which you can relay back to Teale for help (or try to fix yourself if you're especially brave!).

6. If all went well, you should have your very own deck of Nothing Sacred Cards!
	1. In your NSC directory, go to output.
	2. In output, you should see a folder with today's date. Open it up.
	3. This folder should be full of 53 different card files and 7 sheet files.
	4. Cool!

7. Nothing Sacred Cards has a lot of options and features. To learn more about them, run "python nsc.py -h" at the command line (without the quotes, of course).
	1. One particularly awesome feature is that NSC can generate PDFs of all of your cards so you can quickly print them out. Let's try that now!
	2. At the command line, run "python nsc.py -i playing_cards.json -p". Note the -p there at the end.
	3. Twiddle your thumbs while NSC does its thang.
	4. Head on over to the output directory to find the most recent folder there.
	5. In addition to the 53 different card files and the 7 sheet files, you should see a PDF file called cards.pdf.
	6. If you want to play with your new cards, open the pdf and print them out!


## Customization Part I: The Emporer's New Suit

Maybe you don't like the default cards that come with Nothing Sacred Cards. Fine. Whatever. See if I care.

But the beautiful thing about Nothing Sacred Cards is that it's very easy to quickly change your cards with your heart's whims! As an example, let's change one of the suits.

1. Navigate to your NSC directory.

2. You should see a directory called art there. Go to art.

3. In art, you should see three directories, background, full, and inline. Go to inline.

4. The inline directory contains images you want to appear inline on your cards. You'll be putting lots of images in this directory when you start making your own cards. In the mean time, notice that there are 3 images for each suit: suit_medium.png, suit_large.png, and suit_large_rotated.png.

5. Let's try changing the leaves (saved in spade files) to something else. Feel free to come up with your own images (they should be 50x50 pixels for _mediumm and 100x100 pixels for _large), or just use the replacement pngs included in the directory.
	1. Rename the old spade files. An easy way to do it is just adding "_old" to the end of the names. For example, "spade_medium.png" now becomes "spade_medium_old.png".
	2. Save the new files with the spade names. Remember, NSC is looking for EXACT name matches, so typos will cause it to vomit up all sorts of text, or make your cards look weird. Make sure you have files named "spade_medium.png", "spade_large.png", and "spade_large_rotated.png".

6. Go back to your command prompt and run Nothing Sacred Cards again (python nsc.py -i playing_cards.py). If all goes to plan, keep going. Otherwise, contact Teale with error messages.

7. Go to your output folder and look for the directory with today's date and time.

8. Check out your spiffy new cards.


## Customization Part II: King to Beggar

Your latest game is all the rage in your game group, but you're a little tired of using cards that don't fit your theme. Your game has nothing to do with royalty, it's all about the down trodden!

No problem. In this tutorial, you'll turn the king to into a beggar. You'll be learning about CARD FILES as you do.

1. Go to your NSC directory.

2. Go to the cards directory, which should be in there.

3. Open playing_cards.json in a text editor.

	a. A json file is a simple way to structure data. For more information about it, look at the json help file.

	b. json files in the cards directory store the information about your cards. You can have any number of files here, as long as they're structured like the json help file describes.

4. This is what your card file will look like. It's intimidating, but we'll go over it so you have the chance to figure it out bit by bit.

	a. Each card is stored between a { and a }. The Ace of Spades is defined as the first card, from line 2 to line 9.

	b. The cards are stored in a list between the [ and ]. Each card except the last has a , after its }.

	c. Each card is made of a bunch of key:value pairs. Think of keys like the names of the type of data you're storing and the values as the actual information for that card.

	d. Each card has to have a "name". Each card's name should be different, and certain special characters might break the program. It can be used to specify specific cards to print.

	e. Each card has to have a "type". This determines which template the card will use to display its information.

	f. Cards don't need a "number", but this key shows how many copies of the card should be included in the deck. If you don't include a number, 1 copy will be included. If you choose 0, the card will not be included at all.

	g. All other keys are optional and contain card specific information. Generally, text in here will be displayed as is on the card where specified, but there are a few special commands you can send to Nothing Sacred Cards here. These will always start with "\\", which tells NSC that something special is coming up.

		i. \\n says to end the current line and start a new line.

		ii. \\b turns on or off bold. Make sure you always turn off bold after you turn it on.

		iii. \\i turns on or off italic. Make sure you turn it off.

		iv. \\image_name tells NSC to include an image from the art/inline or art/full directories. image_name should be the file name without the extension (.png or .jpg). Inline images will appear on the same line as text, while full images will appear centered on a new line.

		v. \\img:key tells NSC to use the image stored in another key.

	h. Playing cards have 5 extra keys:

		i. small_symbol is the image that should be placed in the corner of the card.

		ii. large_symbol is the image that should be used for the suit in the center of the card.

		iii. large_symbol_rotated is the same as large_symbol, but rotated 180 degrees. These are the upside down symbols in the middle of the card.

		iv. center_design is the actual layout of the center image for the card. Note that many of the center designs use the \\img:key functionality. For example, \\img:large_symbol will eventually turn into the image stored in the large_symbol key.

		v. card_number is the letter or number that should appear in the corners of the playing card. This is what we want to change to make the king become a beggar!

5. Search for "card_number":"K" in your file. (Most text editors will search for a string with Ctrl + f.) Replace the K with B. You should do this 4 times, once for each suit.

6. Now go back to the command prompt and run NSC (python nsc.py -i playing_cards.py). Assuming all goes well, you should now find a new folder in the output directory with Kings that have Bs instead of Ks!


## Customization Part III: Magic Cards

So far we've just looked at the playing cards, but Nothing Sacred Cards also comes with some made up magic cards. In this mini-tutorial, you'll learn how to generate these magic cards!

1. Go to your NSC directory.

2. Go back to the command prompt and run NSC, but instead of "python nsc.py -i playing_cards.json", use "python nsc.py -i magic_cards.json". The -i command tells Nothing Sacred Cards where to look for card info (in the cards/ directory), so you're specifying here that you want to generate cards from the magic_cards.json file.
	a. Don't forget that you can always run "python nsc.py -h" at the command line to get a list of all of the features Nothing Sacred Cards has to offer.

3. If all goes well, you should see some spiffy looking magic cards flash on the screen. Head over to the output folder to check out the new cards!

4. The magic cards are quite a bit more complex than the playing cards, both in terms of their card file (magic_cards.json in the nsc/cards directory) and in terms of their template (magic_card_creature.json in nsc/templates). Check out those files to give them a try.

5. Try making your own magic card! Start simple, by just copying an existing one from magic_cards.json and tweaking it a little. Remember that not all of the symbols from magic are in NSC, so try to stick with color mana, 1 or 2 colorless mana, and the tap symbol for now. If you're feeling extra adventurous, why not head over the nsc.py and tell it to only generate the new card you're working on! (Hint: Use the -c command wisely.)
