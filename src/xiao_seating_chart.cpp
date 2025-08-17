// This displays a default rainbow pattern along
// the LEDs that are under the map. When a guest
// taps their RFID card name onto the reader, the
// pathway to their seat will light up three times
// and then go back to the default pattern.
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include <FastLED.h>
#include <xiao_seating_chart.h>

// If using the breakout or shield with I2C, define just the pins connected
// to the IRQ and reset lines.  Use the values below (2, 3) for the shield!
#define PN532_IRQ   (2)
#define PN532_RESET (3)  // Not connected by default on the NFC Shield

// Initialize NFC board
// use this line for a breakout or shield with an I2C connection:
Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

// Definitions to help the strings of LEDs to work with FastLED
#define DATA_PIN_0 7
#define DATA_PIN_1 9
#define NUM_LEDS_0 76
#define NUM_LEDS_1 76

// Define the array of leds
CRGB ledsA[NUM_LEDS_0];
CRGB ledsB[NUM_LEDS_1];

// Define colors used to light up path
CRGB pathColor = CRGB::BlanchedAlmond;
CRGB seatColor = CRGB::Green;

void fill_all_solid(CRGB color);
void animateToPosition(uint8_t startLeft, uint8_t targetLED);
uint8_t uid_match(uint8_t* cardUID, uint8_t* pplUID);
void init_paths();
void rainbow();

void setup() {
  // Initialize path variables
  init_paths();

  Serial.begin(115200);
  Serial.println("Hello!");

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if(! versiondata){
    Serial.print("Didn't find PN53x board");
    while(1); // halt
  }

  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
  Serial.print('.'); Serial.print((versiondata>>8) & 0xFF, DEC);

  FastLED.addLeds<NEOPIXEL, DATA_PIN_0>(ledsA, NUM_LEDS_0).setCorrection(TypicalSMD5050);  // GRB ordering is assumed
  FastLED.addLeds<NEOPIXEL, DATA_PIN_1>(ledsB, NUM_LEDS_1).setCorrection(TypicalSMD5050);  // GRB ordering is assumed
  FastLED.setBrightness(150);
  
  for(int i = 0; i < NUM_LEDS_0; i++){
        ledsA[i] = CRGB::Black;
    }
  FastLED.show();
}

// fill both strands with same color
void fill_all_solid(CRGB color){
  fill_solid(ledsA, NUM_LEDS_0, color);
  fill_solid(ledsB, NUM_LEDS_1, color);
  FastLED.show();
}


// Light path to seat 5 times with two LED strands
void animateToPosition(struct person seat){
  fill_all_solid(CRGB::Black);
  CRGB* currLeds = ledsA;
  if(seat.branch == 1){
    currLeds = ledsB;
  }

  for(uint8_t i = 0; i < 5; i++){
    for(uint8_t step = 0; step < seat.pathLen; step++){
      currLeds[seat.path[step]] = pathColor;
      fadeToBlackBy(currLeds, NUM_LEDS_0, 80);
      delay(40);
      currLeds[seat.path[seat.pathLen-1]] = seatColor;
      FastLED.show();
    }
  }
}

// Compare two UID numbers stored as arrays
uint8_t uid_match(uint8_t* cardUID, uint8_t* pplUID){
  for(uint8_t byte = 0; byte < 7; byte++){
    if(cardUID[byte] != pplUID[byte]){
      return 0;
    }
  }
  return 1;
}

// Initialize path object that were in the header file
void init_paths(){
  guests[0].path = path0;
  guests[0].pathLen = pathLen0;

  guests[1].path = path1;
  guests[1].pathLen = pathLen1;

  guests[2].path = path2;
  guests[2].pathLen = pathLen2;

  guests[3].path = path3;
  guests[3].pathLen = pathLen3;

  guests[4].path = path4;
  guests[4].pathLen = pathLen4;
}

void rainbow(){
  static uint8_t hue = 0;
  hue+=5;
  
  for(int led = 0; led < NUM_LEDS_0; led++){
    ledsA[led] = ColorFromPalette(RainbowColors_p, hue+map(led, 0, NUM_LEDS_0, 0, 255));
    ledsB[led] = ColorFromPalette(RainbowColors_p, hue+map(led, 0, NUM_LEDS_0, 0, 255));
  }
  Serial.println(hue);
  FastLED.show();
}

void loop() {

  // default show moving rainbow animation
  rainbow();

  // Look for NFC card
  uint8_t success;
  uint8_t uid[] = {0,0,0,0,0,0,0}; //Buffer to store the returned UID
  uint8_t uidLength;                // Length of the UID (4 or 7 bytes depending on ISO14443A card type)

  // Wait for an ISO1443A type card (Mifare, etc.). When one is found
  // 'uid' will be populated with the UID, and uidLength will indicate
  // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength,100);

  if(success){
    // Display some basic information about the card
    Serial.println("Found an ISO14443A card");
    Serial.print("  UID Length: "); Serial.print(uidLength, DEC); Serial.println(" bytes");
    Serial.print("  UID Value: ");
    nfc.PrintHex(uid, uidLength);
    Serial.println();

    // Check if NFC card is in list and then light up path to the guest's seat
    for(uint8_t ppl = 0; ppl < NUM_GUESTS; ppl++){
      if(uid_match(uid,guests[ppl].id)){
        animateToPosition(guests[ppl]);
        break;
      }
    }
  }

  FastLED.show();
}