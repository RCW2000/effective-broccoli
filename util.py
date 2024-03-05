import csv
import matplotlib.pyplot as plt
import math
import PySimpleGUI as sg
class DataTable:
    def __init__(self, originalData:list):
        self.columnHeaders=originalData[0]
        self.OriginalRecords=originalData[1]
        self.OriginalAttributeValues=originalData[2]
        self.OriginalTable=originalData[3]
        self.currentAttributeValues=self.OriginalAttributeValues
        self.outliers=[]


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
    table=sg.Table(records,column_headers,expand_x=True,expand_y=True,justification='right',num_rows=35,key='OG_Table')
    originalData=[column_headers,records,attributeValues,table]
    return originalData

def variance(data:list):
    sum=0
    sq_sum=0
    for num in data:
        num=float(num)
        sum=sum+num
        sq_sum=sq_sum+(num*num)
    avg=sum/(len(data))
    sq_avg=sq_sum/(len(data))
    return sq_avg-(avg*avg)

def std_dev(data:list):
    return math.sqrt(variance(data))