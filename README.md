# Interactive Wedding Seating Chart

# Parts list
- Seeeduino XIAO SAMD21 https://www.seeedstudio.com/Seeeduino-XIAO-3Pcs-p-4546.html
  - https://wiki.seeedstudio.com/Seeeduino-XIAO/
- RFID reader
  - https://www.amazon.com/dp/B01I1J17LC/ref=sspa_dk_hqp_detail_aax_0?psc=1&sp_csd=d2lkZ2V0TmFtZT1zcF9ocXBfc2hhcmVk
- RFID Cards/Stickers
- Pebble LEDs
  - I used 1.5cm pitch https://www.aliexpress.us/item/3256808337134015.html
- Power source
  - I used a cell phone charger battery
 
# Instructions
## Create floor plan
- Make a map of the venue with decorations in a design tool.
- Use a translucent acrylic as a base, and decorate.
  - Laser cutting, vinyl stickers, paper stickers, sharpies, UV Printing are all options here
## Layout LEDs
  - Print on paper the same layout to be used underneath the acrylic. This will be used as a guide to layout the LEDs
  - Leave extra LEDs on the edges to allow for slack for the connections to the microcontroller and power. Extras can be covered up with black electrical tape if they don't want to be shown later.
  - Attach LEDs to the paper backing in a layout that makes sense to show the paths and seats. I used hot glue.
## Connect guest name to RFID card
- Collect your guest's RSVPs and organize those that are coming into tables that won't cause too much drama
- Assign them a table number and seat number, and a unique ID.
- Create escort cards for each guest by attaching an RFID sticker to a card or paper with their name on it
- Use a collection script to assign each escort card to each person's unique ID.
-   I sorted the list and cards alphabetically and tapped the cards in order to avoid confusion
## Create map of LED to tables/seats
- I took an overhead picture of the LEDs and numbered them individually to find which LED is where on the map. I use these numbers to create the paths of light that are connected to each guest
 
# Further Resources
- I used FastLED to control the LED strip. https://fastled.io/
- Adafruit's NeoPixel library would also probably work well. https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library-use
