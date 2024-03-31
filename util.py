import csv
import math
import PySimpleGUI as sg
import DM_Assignment_1 as dm
import texttable as tt
class DataTable:
    def __init__(self, originalData:list):
        self.columnHeaders=originalData[0]
        self.OriginalRecords=originalData[1]
        self.currentRecords=self.OriginalRecords
        self.OriginalAttributeValues=originalData[2]
        self.OriginalTable=originalData[3]
        self.currentAttributeValues=self.OriginalAttributeValues
        self.dataNoOutliers=None
        self.outliers=None
        self.outlierRecords=None
        self.sansOutlierTable=None
        self.outlierRemovalReport=None
        self.RMV_txt=""
        self.discretizedRecords=None
        self.discretizedNoDups=None
        self.discretizationText=None
        self.dupedRecords=None
        self.trainData=None
        self.testData=None
        self.CorelationMatrix=None
        self.redundantAttr=None
        self.corrMatrixTXT=None
        self.partitions=None
        self.namedDisTbl=None
        self.unNamedDistTbl=None
        self.currentHeaders=self.columnHeaders


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

def generate_Discretization_Report(dataTable:DataTable):
    #discretized_records=dataTable.discretizedRecords
    #discretized_recordsNoDupes=dataTable.discretizedNoDups
    duped_records=dataTable.dupedRecords
    DisText=str(len(duped_records))+" record(s) were removed due to duplication.\n"
    #number of records removed
    DisText=DisText+"The Following Records were Removed:\n"
    #records affected
    for i in range(len(duped_records)):
        DisText=DisText+str(duped_records[i])+"\n"
    dataTable.discretizationText=DisText

def generate_Corelation_Matrix_Report(dataTable:DataTable,threshold):
    print(dataTable.redundantAttr)
    matrix=dataTable.CorelationMatrix
    head=dataTable.columnHeaders[1:]
    dataTable.corrMatrixTXT=""
    for i in range(len(head)):
        dataTable.corrMatrixTXT=dataTable.corrMatrixTXT+str(head[i])+" "
    for l in range(len(matrix)):
        dataTable.corrMatrixTXT=dataTable.corrMatrixTXT+"\n" + str(head[i]) +" "
        for j in range(len(matrix)):
            dataTable.corrMatrixTXT=dataTable.corrMatrixTXT+str(matrix[l][j])+" "
    dataTable.corrMatrixTXT=dataTable.corrMatrixTXT+"\nThreshold Value: "+str(threshold)+"\nHighly Correlated Attributes:\n"
    if len(dataTable.redundantAttr) >0:
        for i in range(len(dataTable.redundantAttr)):
            dataTable.corrMatrixTXT=dataTable.corrMatrixTXT+str(head[dataTable.redundantAttr[i][0]])+" <-> "+str(head[dataTable.redundantAttr[i][1]])+" Correlation Value: "+str(matrix[dataTable.redundantAttr[i][0]][dataTable.redundantAttr[i][1]])+"\n"
    else: 
        "None"
    return dataTable.corrMatrixTXT
    


def nottagSort(dataList:list):
    data=dataList.copy()
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            if data[i] > data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    return data

def ascData(data:list):
    sorted_Data=nottagSort(data)
    return sorted_Data

def median(data:list):
    #sort data
    Ordered_Data=ascData(data)
    #find median
    if len(Ordered_Data)%2!=0:
        medianInd=len(Ordered_Data)//2
        print(str(medianInd)+"here")
        print(Ordered_Data)
        print(len(Ordered_Data))
        return float(Ordered_Data[medianInd])
    else:
        half=int(len(Ordered_Data)/2)
        medianInd_1=half-1
        medianInd_2=-half
        print(str(medianInd_1)+"here 2")
        print(medianInd_2)
        print(Ordered_Data)
        print(len(Ordered_Data))
        return (float(Ordered_Data[medianInd_1])+float(Ordered_Data[medianInd_2]))/2
    
def record_to_values(record:list):
    attributeValues=[]
    for j in range(len( record[0])):
        helperArr=[]
        for i in range(len(record)):
            helperArr.append(float(record[i][j]))
        attributeValues.append(helperArr)
    return attributeValues

def record_to_valuesI(record:list):
    attributeValues=[]
    for j in range(len( record[0])):
        helperArr=[]
        for i in range(len(record)):
            helperArr.append(int(record[i][j]))
        attributeValues.append(helperArr)
    return attributeValues

def values_to_records(values:list):
    records=[]
    inc=0
    for i in range(len(values[0])):
        record_helper=[]
        for j in range(len(values)):
            record_helper.append(values[j][inc])
        records.append(record_helper)
        inc=inc+1
    #print(records)
    return records

def orderRecords(records):
    return records[0]

def orderItemSets(its):
    its.replace('I',"")
    return int(its)

def DownloadData(Data, headers, filepath):
    with open(filepath,'w') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(Data)
    print('FIle Saved')


def support(Freq,data:list):
    return Freq/len(data)

def confidence(Freq, data:list,A):
    ct=0
    for i in range(len(data)):
        if len(set(A).intersection(set(data[i])))>0 :
            ct=ct+1
    if ct==0:
        return 0
    return Freq/ct

def freqAUB(A,B,data):
    ct=0
    for i in range(len(data)):
        if len(set(A).intersection(set(data[i])))>0  and len(set(B).intersection(set(data[i])))>0:
            ct=ct+1
    return ct
def associationCalc(rules,data:list):
    confidences=[]
    supports=[]
    for i in range(len(rules)):
        A=rules[i][0]
        B=rules[i][1]
        freq=freqAUB(A,B,data)
        confidences.append(confidence(freq,data,A))
        supports.append(support(freq,data))
    return confidences,supports

def nameToAttribute(nameTable,name):
    for i in range(len(nameTable)):
        if len(set(name).intersection(set(nameTable[i])))>0:
            return nameTable[i][0]

def nameToValue(nameTable,name):
    for i in range(len(nameTable)):
        if len(set(name).intersection(set(nameTable[i])))>0:
            return nameTable[i][1]
        
def nameToRange(nameTable,name):
    for i in range(len(nameTable)):
        if len(set(name).intersection(set(nameTable[i])))>0:
            return nameTable[i][3]
        
def display_Records(dataTable:DataTable,rmv_Ind):
    #add filler colums of data
    da=dataTable.currentAttributeValues.copy()
    if rmv_Ind==None:
        return values_to_records(da)
    for i in range(len(dataTable.columnHeaders)+len(rmv_Ind)):
        if i in rmv_Ind:
            da.insert(i,['null' for i in range(len(da[0]))])
    return values_to_records(da)

    
