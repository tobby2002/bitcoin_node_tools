# Basic Script to open bitcoin-cli debug.log and parse the latest
# updates into a flask server so users can monitor activity
import sys
import getopt


def open_log(logfile):
    inputfile = 'debug.log'

    try:
        opts, args = getopt.getopt(argv, "f:x:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(f"Input File: {inputfile}")
        print(f"Output File: {outputfile}")
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

    print(f"Input File: {inputfile}")
    print(f"Output File: {outputfile}")


# Start the code
print("Log File Manager")
print("----------------")
print("By default debug.log will be used from current directory")
print("to change the debug file to read use:")
print('logreader -f <log filename> -u <update frequency in seconds>')
print('example: logreader -f debug.info -u 120')

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

# filename = open("debug.log", "r")
# print(filename.read())

#  Todo list
# Format: HTML, TXT
# Post direction: email, ftp
