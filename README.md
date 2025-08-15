# Interactive Wedding Seating Chart

# Parts list
- Seeeduino XIAO SAMD21 https://www.seeedstudio.com/Seeeduino-XIAO-3Pcs-p-4546.html
  - https://wiki.seeedstudio.com/Seeeduino-XIAO/
- RFID reader
  - https://www.amazon.com/dp/B01I1J17LC/ref=sspa_dk_hqp_detail_aax_0?psc=1&sp_csd=d2lkZ2V0TmFtZT1zcF9ocXBfc2hhcmVk
 
# Instructions
## Create floor plan
- Use a map of the venue
## Connect guest name to RFID card
- Collect your guest's RSVPs and organize those that are coming into tables that won't cause too much drama
- Assign them a table number and seat number, and a unique ID.
- Create escort cards for each guest by attaching an RFID sticker to a card or paper with their name on it
- Use a collection script to assign each escort card to each person's unique ID.
-   I sorted the list and cards alphabetically and tapped the cards in order to avoid confusion

 
# Other Resources
- I used FastLED to control the LED strip. https://fastled.io/
- Adafruit's NeoPixel library would also probably work well. https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library-use
