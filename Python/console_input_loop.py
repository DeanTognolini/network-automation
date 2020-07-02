#!/usr/bin/env python3
import serial, sys, os
from openpyxl import load_workbook
from time import sleep

def main():
    while True:
        xlsx_filename = input("What is the spreadsheets filename? (specific absolute path if not in the same direction as this python file.): ")
        if os.path.isfile(xlsx_filename) == True:
            break
        elif os.path.isfile(xlsx_filename) == False:
            print("I couldn't find that filename, if it isn't located in the same directory as this python file you need to specify the absolute path")
            continue

    while True:
        column_hostnames = input("What is the hostnames column?: ").upper()
        if column_hostnames.isalpha():
            break
        else:
            print("Your input must be a letter.")
            continue

    while True:
        first_row = input("Which row is the first hostname and IP on?: ")
        if first_row.isdigit():
            first_row = int(first_row)
            break
        else:
            print("Your input must be a number.")
            continue

    while True:
        last_row = input("Which row is the last hostname and IP on?: ")
        if last_row.isdigit():
            last_row = int(last_row) + 1
            break
        else:
            print("Your input must be a number.")
            continue

    # Opens serial connection.
    console = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity="N",
    stopbits=1,
    bytesize=8,
    timeout=8
    )

    # Loads xlsx ready to read cell data
    workbook = load_workbook(filename=xlsx_filename, data_only=True)
    sheet = workbook.active

    # This is just a little counter I'll use to track the remaining configs
    # that need to be sent, just for info.
    x = range(first_row, last_row)
    x = len(x)

    # Loops through cell data, finds the correct configuration and sends down
    # serial interface.
    for cell in range(first_row, last_row):
        celldata = sheet[column_hostnames + str(cell)].value
        print("""
-----------------------------------------------
Locating and reading config file for {hostname}.
-----------------------------------------------""".format(hostname = celldata))

        # Locates configuration file and reads into variable.
        try:
            with open(celldata, "r") as f:
                conf = f.read()
        except OSError:
            print("\n**** I couldn't find a file called {hostname}. ****".format(hostname = celldata))
        else:
            print("\n{hostname} config file located. Preparing to send...".format(hostname = celldata))
            # Checks serial connection is open and sends data down serial interface.
            if console.isOpen() == True:
                print("\nSerial connection opened to " + console.name + ".")
                print("\nSending config. Standby...")
                sleep(5)
                console.write(conf.encode())
                print ("""
-----------------------------------------------
Config transfer complete for {hostname}
-----------------------------------------------""".format(hostname = celldata))

            elif console.isOpen() == False:
                print("Could not connect to console interface.")
                sys.exit()

            x = x - 1
            print("There are {count} configs remaining to be transferred.".format(count = x))

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
