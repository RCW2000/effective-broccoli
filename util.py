import csv
import math
import PySimpleGUI as sg
class DataTable:
    def __init__(self, originalData:list):
        self.columnHeaders=originalData[0]
        self.OriginalRecords=originalData[1]
        self.OriginalAttributeValues=originalData[2]
        self.OriginalTable=originalData[3]
        self.currentAttributeValues=self.OriginalAttributeValues
        self.dataNoOutliers=[]
        self.outliers=[]
        self.outlierRecords=[]
        self.sansOutlierTable=None
        self.outlierRemovalReport=None
        self.RMV_txt=""


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
            helperArr.append(float(records[i][j]))
        attributeValues.append(helperArr)
    table=sg.Table(records,column_headers,expand_x=True,expand_y=True,justification='right',num_rows=35,key='OG_Table')
    originalData=[column_headers,records,attributeValues,table]
    return originalData

def mean(data:list):
    sum=0
    for num in data:
        sum=sum+num
    avg=sum/(len(data))
    return avg

def variance(data:list):
    sq_sum=0
    for num in data:
        sq_sum=sq_sum+(num*num)
    avg=mean(data)
    sq_avg=sq_sum/(len(data))
    return sq_avg-(avg*avg)

def std_dev(data:list):
    return math.sqrt(variance(data))

def generate_Outlier_Report(dataTable:DataTable):
    outlierList=dataTable.outliers
    columnNames=dataTable.columnHeaders
    attributeValues=dataTable.OriginalAttributeValues
    OutlierText="The Following Outliers Have Been Removed:\n"
    for i in range(len(outlierList)):
        col=outlierList[i][0]
        val=outlierList[i][1]
        num=attributeValues[col][val]
        header=columnNames[col]
        OutlierText=OutlierText+"The Value: "+str(num)+" Located In: "+header+"\n"
    OutlierText=OutlierText+"The Following Records Have Been Removed Due to Containing Outliers:\n"
    rmv_records=[dataTable.OriginalRecords[i] for i in range(len(dataTable.OriginalRecords)) if i in dataTable.outlierRecords ]
    for i in range(len(rmv_records)):
        OutlierText=OutlierText+str(rmv_records[i])+"\n"
    dataTable.RMV_txt=dataTable.RMV_txt+OutlierText
    OutlierText=OutlierText+"Attributes Affected: "
    aff_cols=[]
    for i in range(len(dataTable.outliers)):
        aff_cols.append(dataTable.outliers[i][0])
    aff_cols=list(set(aff_cols))
    for i in range(len(aff_cols)):
        OutlierText=OutlierText+columnNames[aff_cols[i]]+" "
    OutlierText=OutlierText+"\nTotal Records Removed: "+str(len(rmv_records))+" Total Records Remaining: "+str(len(dataTable.OriginalRecords)-len(rmv_records))
    dataTable.outlierRemovalReport=OutlierText

def tagSort(data:list):
    tags=[i for i in range(len(data))]
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            if data[i] > data[j]:
                tags[i], tags[j] = tags[j], tags[i]
    return tags

def ascData(data:list):
    genTags=tagSort(data)
    sorted_Data=[]
    for tag in genTags:
        sorted_Data.append(data[tag])
    return sorted_Data

def median(data:list):
    #sort data
    Ordered_Data=ascData(data)
    #find median
    if len(Ordered_Data)%2!=0:
        medianInd=math.ceil(len(Ordered_Data)/2)
        return float(Ordered_Data[medianInd])
    else:
        medianInd_1=math.floor(len(Ordered_Data)/2)
        medianInd_2=math.ceil(len(Ordered_Data)/2)
        return (float(Ordered_Data[medianInd_1])+float(Ordered_Data[medianInd_2]))/2