import csv

def Generate_Table_From_CSV(filepath):
    csvfile = open(filepath,mode='r')
    rawdata = csv.reader(csvfile)
    