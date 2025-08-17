- Populate an initial CSV file with guest names.
- Adjust collection file name in collect_nameID.py with the csv generated above
- Connect a RFID reader to a Raspberry Pi and run collect_nameID.py
- The screen will prompt when to tap the card of a particular guest in order to add 
an RFID UUID to a particular guest's row in the CSV.
- The collect_nameID.py file will output a 'name_and_UID.csv' file