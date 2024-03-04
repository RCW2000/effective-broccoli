import csv
import matplotlib.pyplot as plt
class DataTable:
    def __init__(self, originalData:list):
        self.columnHeaders=originalData[0]
        self.OriginalRecords=originalData[1]
        self.OriginalAttributeValues=originalData[2]
        self.OriginalFigure=originalData[3]


def Generate_Table_From_CSV(filepath):
    csvfile = open(filepath,mode='r')
    rawdata = csv.reader(csvfile)
    table=[line for line in rawdata]
    column_headers=table[0]
    records=table[1:]
    attributeValues=[]
    for j in range(len(records[0])):
        helperArr=[]
        for i in range(len(records)):
            helperArr.append(records[i][j])
        attributeValues.append(helperArr)
    figure=plt.table(records, colLabels=column_headers)
    originalData=[column_headers,records,attributeValues,figure]
    return originalData

    