from tkinter.messagebox import showerror

import snap7

plc = snap7.client.Client()
IP_ADDRESS = '10.7.14.111'
db_to_write = True

try:
    plc.connect(IP_ADDRESS, 0, 1)
    plc.db_write(db_number=db_to_write, start=0, data=bytearray([1]))  # Write 1 to DB1 at offset 0
    plc.disconnect()  # Disconnect from the PLC
    print("Value 1 sent to DB1 successfully.")
except snap7.snap7exceptions.Snap7Exception as e:
    showerror(title='Error', message=str(e))
