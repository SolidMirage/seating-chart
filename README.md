# Interactive Wedding Seating Chart
## Table of Contents
- [Introduction](#introduction)
- [Parts List](#parts-list)
- [Instructions](#instructions)
- [Personal Notes](#personal-notes)
- [Further Resources](#further-resources)

## Introduction
For my wedding I wanted to create an interactive seating chart to show guests to their spot for dinner. The assigned seats are important in order to make sure correct dishes are given to guests to cater to the preferences they chose as well as avoid any allergens. I would like to share what I made so others may get inspired to their own electronic fun goodies for their weddings or events. 

There is a series of LEDs underneath translucent acrylic that can obfuscate most of the electronics. The acrylic shows the map of the venue through a combination of engraving and spray painting. Each guest has an escort card with their name and table number and a hidden RFID tag. When the guest taps their card onto an indicated spot on the acrylic, the animation on the LEDs changes to highlight a pathway to the table and seat they are assigned.

You will find in this repository files that can be used to create an interactive seating chart as I have made in two ways. One way is with a PlatformIO project where I used a Seeeduino XIAO SAMD21 board connected to a PN532 NFC breakout board and LEDs. The other way is with Python scripts running on a Raspberry Pi Zero W connected to a PN532 NFC board and LEDs.

## Parts list
- Seeeduino XIAO SAMD21
  - Buy at: https://www.seeedstudio.com/Seeeduino-XIAO-3Pcs-p-4546.html
  - Documenation at: https://wiki.seeedstudio.com/Seeeduino-XIAO/
- Raspberry Pi Zero 2 W
  - https://www.seeedstudio.com/Raspberry-Pi-Zero-2-W-with-Header-p-5935.html
- RFID reader
  - https://www.amazon.com/dp/B01I1J17LC/
- Pebble LEDs
  - Buy at: https://www.aliexpress.us/item/3256808337134015.html
  - There are many vendors of these. I used 1.5cm pitch, but use what makes sense for your size
- Power source
  - I used a cell phone charger battery
  - Might need a separate one for the LEDs as well as the chosen microcontroller
- Translucent Acrylic
  - [Black LED acrylic](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/black_led_sheet/668)
  - [White Translucent Acrylic](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/acrylic_sheets_color/341)
    - Around 40% transmission seems to work well
 
## Instructions
### Create floor plan
- Make a map of the venue with decorations in a design tool
- Place a spot where the RFID reader should go
- Decide how large you would like the final map to be
  - Draw on wrapping paper, tape pieces of printer paper together, sketch on cut cardboard, etc
- Use a translucent acrylic as a base, and decorate with the map
  - Laser cutting, vinyl stickers, paper stickers, sharpies, UV Printing are all options here
### Physically layout LEDs
  - Print on paper the same map and decoration to be used underneath the acrylic. This will be used as a guide to layout the LEDs
  - Leave extra LEDs at the beginning/end of the paths to allow for slack for the connections to the microcontroller and power. Extra LEDs can be covered up with black electrical tape if you don't want them to be lighting up later
  - Attach LEDs to the paper backing in a layout that makes sense to show the paths and seats. Hot glue or tape can be good options
### Create map of each LEDs number for easier reference
- Several ways to do this:
  - Take an overhead picture of the LEDs and number using digital program
  - Take an overhead picture of the LEDs, print out the picture and write numbers
  - Write numbers next to each LED on the paper
### Create routes to each guest
- In the SAMD21 XIAO code, you'll find a header file that has hardcoded paths for each guest that use the indices of the LEDs written in the previous step
- In the Raspberry Pi code, you'll find functions that tries to reduce the number of hardcoded paths
  - Each table has a hardcoded path
  - Each guest has a number 'chair' associated from the bottom part of the table counting clockwise
- Test by connecting the microcontroller of your choice to your LEDs to confirm correct paths to each seat
### Connect guest name to RFID card
- Collect your guest's RSVPs and organize those that are coming into tables that won't cause too much drama
- Assign them a table number and seat number, and a unique ID
- Create escort cards for each guest by attaching an RFID sticker to a card or paper with their name on it
- Use a collection script to assign each escort card to each person's unique ID
  - I sorted the list and cards alphabetically and tapped the cards in order to avoid confusion
  - An example script is in the supplement folder
### Connect RFID card to route
- Combine the list in the previous step with the LED routes made in two steps prior in code on the microcontroller
### Create a physical box to hold everything together
- Foam core board, wood, more acrylic, etc combined with glue, screws, epoxy, etc
### Bring to wedding
- Charge batteries and extra batteries the night before.
- Label parts and provide instructions of assembly and placement to someone trusted in the bridal party
### Enjoy!!
 
## Personal Notes
It was a fun challenge to think of a way to reduce the amount of hard coding possible. It was also quite fun to use different boards and languages to accomplish the same task. In the future I would like to explore using CircuitPython on the XIAO to make an interactive seating chart. For the guest cards I ended up printing names onto cardstock, cutting them out with my vinyl cutter, and taping an NFC tag to each card. I've since found out many different forms of NFC tags that can be bought that are cute and elegant. I'd like to try using wooden NFC tags.

## Further Resources
- I used FastLED to control the LED strip. https://fastled.io/
- Adafruit's NeoPixel library also works well https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library-use
