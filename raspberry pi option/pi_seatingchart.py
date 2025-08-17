# Interactive Seating Chart
# This code is for Raspberry Pi Zero 2 W connected to a PN532 NFC reader
# and three strands of pebble LEDs.
import serial
import board
import busio
from digitalio import DigitalInOut
import pandas as pd
import os
import time
from adafruit_pn532.i2c import PN532_I2C
import numpy
import neopixel


# Setup addresable LED driver
pixel_pin = board.D18
num_pixels = 110 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3,
  auto_write=False)

# Create dataframe to work with the CSV file with guest names
nameIDfile = "../name_table_seat_uid.csv"
df = pd.read_csv(nameIDfile)
df['UID'] = df['UID'].apply(str)

# Initialize RFID reader
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

# Each table can have a different number of guests
# ID is the table number that will be on a sign in the real world
# num_seats is the number of guest at each table has
# strandID identifies the string of LEDs that has the path to and around the table
# the LED index numbers that go around the table clockwise
class Table():
  def __init__(self, ID, num_seats, strandID, segments, seats):
    self.ID = ID
    self.num_seats = num_seats
    self.strandID = strandID
    self.segments = segments
    self.seats = seats

# Initialize Table objects
def setupTables():
  # there are 11 tables
  tables.append(Table(1, 10, 1, [(9,23),(37,43),(68,75)],
    [ 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]))
  tables.append(Table(2, 8, 1, [(9,23),(37,43)],
    [ 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]))
  tables.append(Table(3, 10, 1, [(9,23),(37,45)],
    [ 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]))
  tables.append(Table(4, 10, 1, [(9,25)],
    [ 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]))
  tables.append(Table(5, 10, 0, [(10,17),(47,51),(76,80)],
    [ 98, 99,100,101,102,103,104,105,106,107]))
  tables.append(Table(6, 10, 0, [(10,17),(47,51),(76,83)],
    [ 84, 85, 86 ,87, 88, 89, 90, 91, 92, 93]))
  tables.append(Table(7, 10, 0, [(10,17),(47,52)],
    [ 52, 53, 54, 68, 69, 70, 71, 72, 73, 74]))
  tables.append(Table(8, 10, 0, [(10,17),(47,56)],
    [ 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]))
  tables.append(Table(9, 10, 0, [(10,19)], 
    [ 19, 20, 21, 38, 39, 40, 41, 42, 43, 44]))
  tables.append(Table(10, 10, 0, [(10,25)], 
    [ 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]))
  tables.append(Table(11, 10, 2, [(10,36)],
    [ 37, 38, 43, 44, 45, 47, 48, 54, 55, 56]))

tables = []
num_seats_table = 10

def drawToTable(tableID):
  buildStr = ""
  for seg in tables[tableID].segments:
    buildStr += "S{0}E{1}".format(seg[0], seg[1])
  return buildStr

def drawToSeat(tableID, seat):
  seatIndex = ord(seat) - ord('A')
  buildStr = ""
  currSeat = 0
  table = tables[tableID]
  if seatIndex < num_seats_table/2:
    buildStr += "S{0}".format(table.seats[currSeat])
    while currSeat < seatIndex:
      if table.seats[currSeat+1] - table.seats[currSeat] > 1:
        buildStr += "E{0}".format(table.seats[currSeat])
        buildStr += "S{0}".format(table.seats[currSeat+1])
      currSeat = currSeat + 1
  else:
    currSeat = num_seats_table - 1
    buildStr += "S{0}".format(table.seats[currSeat])
    while currSeat > seatIndex:
      if table.seats[currSeat-1] - table.seats[currSeat] > 1:
        buildStr += "E{0}".format(table.seats[currSeat])
        buildStr += "S{0}".format(table.seats[currSeat+1])
      currSeat = currSeat - 1
  buildStr += "E{0}".format(table.seats[seatIndex])
  return buildStr

baud_rate = 115200 
device_loc = "/dev/ttyS0"
setupRFID()
setupTables()

lastID = 0
timeLastTapped = 0
andNum = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0
while True:
  uid = pn532.read_passive_target(timeout=2)
  if uid is None:
    continue
  if time.time() - timeLastTapped < 5:
    time.sleep(2)
    continue
  IDnum = str(numpy.int64(int.from_bytes(uid,"big")))
  IDnum = IDnum[:-1] + "0" 
  lastID = IDnum
  timeLastTapped = time.time()
  tableID = df[str(IDnum)  == df['UID']]['Table'].iloc[0]-1
  seat = df[str(IDnum) ==  df['UID']]['Seat'].iloc[0]
  sendStr = drawToTable(tableID) + drawToSeat(tableID,seat)
  numSegments = sendStr.count('S')
  sendStr = "L{1}N{0}".format(
    numSegments,tables[tableID].strandID) + sendStr

  for i in range(3):
    pixels.fill((255,0,0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0,0,0))
    pixels.show()
    time.sleep(1)
  
  #ser = serial.Serial(device_loc, baudrate=baud_rate,timeout=3.0)
  #print(sendStr)
  #ser.write(sendStr.encode())
  #ser.close()
