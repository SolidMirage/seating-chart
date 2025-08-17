# Create a table to associate NFC tag UIDs with guest names
# by using a Raspberry Pi Zero 2 W connected to an PN532 NFC reader
import board
import busio
from digitalio import DigitalInOut
import pandas as pd
import os
import time

from adafruit_pn532.i2c import PN532_I2C

import pdb

filename = "../include/names_and_tables.csv"
df = pd.read_csv(filename)
df["UID"] = "" 

print("Hello, blinka!")

def setupRFID():
  global i2c, reset_pin, req_pin, pn532
  # I2C connection:
  i2c = busio.I2C(board.SCL, board.SDA)
  # with I2C, we recommend connecting RSTPD_N (reset) to a 
  # digital pin for manual hardware reset
  reset_pin = DigitalInOut(board.D6)

  # On raspberry pi, you must also connect a pin to P32 "H_Request" for
  # hardware wakeup! this means we don't need to do the I2C clock-stretch
  req_pin = DigitalInOut(board.D12)
  pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
  ic, ver, rev, support = pn532.firmware_version
  print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

  #configure pn532 to communicate with MiFare cards
  pn532.SAM_configuration()

setupRFID()
nameIndex = 0
prevUID = 0

# Example outputs:
# Waiting for Alan Doe
# Found card with UID 1267239301898624
# 
# Waiting for Alan Doe
# still previous card! please press new card
#
# Waiting for Alan Doe
# no ID found
while nameIndex < len(df['First']):
  print("waiting for: {0} {1}".format(df['First'][nameIndex],df['Last'][nameIndex]))
  uid = pn532.read_passive_target(timeout=3)
  if uid is None:
    print('no ID found')
    continue

  currUID = int.from_bytes(uid,"big")
  if currUID == prevUID:
    print('still previous card! please press new card')
    time.sleep(3)
    continue

  prevUID = currUID
  df.loc[nameIndex, "UID"] = currUID
  print("found card with UID:", str(currUID))
  nameIndex = nameIndex + 1

output_file = '../include/name_and_UID.csv'
df.to_csv(output_file, encoding='utf-8', index=False)