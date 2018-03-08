import visa
from time import sleep
import argparse

#parse arguments
parser = argparse.ArgumentParser(description='Send a list of messages to an Agilent 33600 AWG')
parser.add_argument('-f','--filename', help='Macro file containing SCPI commands', default="", required=False)
parser.add_argument('-a','--address', help="Address of device", default="142.104.60.122", required=False)
parser.add_argument('-l', '--line', help="A single command to send to the device", default="", required=False)
parser.add_argument('-r', '--reset', help="Reset device before running commands", action='store_true', required=False)

args = parser.parse_args()

#print an error message if neither a line or macro file is specified
if args.line == "" and args.filename == "":
    parser.error("either -l or -f must be specified")
    


#load the VISA resource manager
rm = visa.ResourceManager('@py')

#connect to the device
inst = rm.open_resource("TCPIP::"+args.address+"::INSTR")
print(inst.query("*IDN?"))

#reset the device
if args.reset:
    print("Resetting device...")
    inst.write("*RST")

#sent start control message
message="Controlling\nRemotely"
inst.write("DISP:TEXT '"+message+"'")

#sent commands to device

#single line
if args.line !="":
    inst.write(args.line)
    print(args.line)

#macro file
if args.filename != "":
    for line in open(args.filename):
        sleep(0.1)
        #ignore commented lines
        if line[0] == '#':
            continue;
        writeString = line.split("#")[0].strip()
        inst.write(writeString)
        print(writeString)

#clear message
inst.write("DISP:TEXT ''")

#check for errors
instrument_err = "error"
while instrument_err != '+0,"No error"\n':
    inst.write('SYST:ERR?')
    instrument_err = inst.read()
    if instrument_err[:2] == "+0": #ignore no error message
        continue;
    print(instrument_err)


#close device connection
inst.close()
