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
        self.discretizedRecords=[]


def Generate_Table_From_CSV(filepath):
    csvfile = open(filepath,mode='r')
    rawdata = csv.reader(csvfile)
    table=[line for line in rawdata]
    column_headers=table[0]
    records=table[1:]
    table=sg.Table(records,column_headers,expand_x=True,expand_y=True,justification='right',num_rows=35,key='OG_Table')
    originalData=[column_headers,records,record_to_values(records),table]
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
        return float(Ordered_Data[medianInd-1])
    else:
        medianInd_1=math.floor(len(Ordered_Data)/2)
        medianInd_2=math.ceil(len(Ordered_Data)/2)
        return (float(Ordered_Data[medianInd_1-1])+float(Ordered_Data[medianInd_2-1]))/2
    
def record_to_values(record:list):
    attributeValues=[]
    for j in range(len( record[0])):
        helperArr=[]
        for i in range(len(record)):
            helperArr.append(float(record[i][j]))
        attributeValues.append(helperArr)
    return attributeValues

def values_to_records(values:list):
    records=[]
    inc=0
    helperArr=[]
    while inc < len(values[0]):
        for col in range(len(values)):
            helperArr.append(values[col][inc])
        records.append(helperArr)
        helperArr=[]
        inc=inc+1
    return records

def partitionMed(partitionCol:list):
    av=[partitionCol[i][1] for i in range(len(partitionCol))]
    return median(av)

def partitionMean(partitionCol:list):
    av=[partitionCol[i][1] for i in range(len(partitionCol))]
    return mean(av)