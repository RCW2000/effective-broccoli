import csv
import util
import math
import random
import TreePartition as pt
from itertools import combinations, permutations
def identifyOutliers(dataTable:util.DataTable):#identify outliers and Highlight rows to be romoved on figure
    attributeValues=dataTable.currentAttributeValues
    std_devs=[]
    means=[]
    #for each attribute
    for col in range(len(attributeValues)):
        #calculate standard deviiation and mean of each column
        mean=util.mean(attributeValues[col])
        std_dev=util.std_dev(attributeValues[col])
        means.append(mean)
        std_devs.append(std_dev)
    outliers=[]
    #determine outliers
    for i in range(1,len(attributeValues)):
        for j in range(len(attributeValues[i])):
            if attributeValues[i][j] > means[i]+std_devs[i]*2 or attributeValues[i][j]< means[i]-std_devs[i]*2:
                #add to outliers list
                outliers.append([i,j])
    dataTable.outliers=outliers

def findMedians(dataTable:util.DataTable):
    attributeValues=dataTable.currentAttributeValues
    medians=[]
    for col in range(len(attributeValues)):
        print(len(attributeValues[0]))
        median=util.median(attributeValues[col])
        medians.append(median)
    return medians

def entropy(s:list):
    #print(s)
    s_av=[s[i][1] for i in range(len(s))]
    s_classes=[s[i][2] for i in range(len(s))]
    m,pi,_=set_class_info(s_av,s_classes)
    #pi=freq of each class
    sum=0
    for i in range (0,m):
        sum=sum-(pi[i] * math.log(pi[i],2))
    return sum


def info_gain(s_num, s1, s2):
    #s_num=cardinality of S
    ent_s1=entropy(s1)
    ent_s2=entropy(s2)
    s1_num=len(s1)
    s2_num=len(s2)
    
    s1_part=(s1_num/s_num)*ent_s1
    s2_part=(s2_num/s_num)*ent_s2

    return s1_part+s2_part
    
def set_class_info(s:list,classValues:list):
    unique_classValues=list(set(classValues))
    m=len(unique_classValues)
    pi=[(classValues.count(unique_classValues[i])/len(classValues)) for i in range(m)]
    return m,pi,unique_classValues

def createPartionColumn(attributeCol:list,classValues:list):
    PartitionColumn=[]
    classValues=classValues
    for val_ind in range(len(attributeCol)):
        PartitionColumn.append([val_ind,attributeCol[val_ind],classValues[val_ind]])
    return PartitionColumn

def isStopCondition(partitionCol:list,OriginalValues):
    av=[partitionCol[i][1] for i in range(len(partitionCol))]
    classes=[partitionCol[i][2] for i in range(len(partitionCol))]
    m,pi,_=set_class_info(av,classes)
    #print(pi)
    if m<2:
        return True
    if min(pi)/max(pi) <0.5:
        return True
    if m < math.floor(len(list(set(OriginalValues)))/2) or m==math.floor(len(list(set(OriginalValues)))/2):
        return True
    if len(list(set(av)))==1:
        return True
    
    return False

def Partition(partitionCol:list,OriginalValues,Partfunction):
    #create table to hold partioned sets where each r/c = A11A21 etc
    partition_table=[[0 for i in range(2)] for i in range(len(partitionCol))]
    print('created table: '+str(len(partition_table)))
    #patrition set until stop adding each to table
    i=0
    j=0
    finPartitions=[]
    while i < len(partition_table):
        j=0
        while j <2:
            if i==0:
                k=1
                partition_table[i][0]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]<Partfunction(partitionCol)]#A1
                partition_table[i][1]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]>Partfunction(partitionCol) or partitionCol[i][1]==Partfunction(partitionCol)]#A2
                #print(partition_table[i][1][0][1])
                #print('partition added')
                if partition_table[i][0]==[]:
                    partition_table[i][0]=False
                if partition_table[i][1]==[]:
                    partition_table[i][1]=False
                #add to fin part
                if partition_table[i][0]==[] or partition_table[i][1]==[]:
                    finPartitions.append([partitionCol,'No Split'])
                    partition_table[i][0]=False
                    partition_table[i][1]=False
                elif (partition_table[i][0]!=False and isStopCondition(partition_table[i][0],OriginalValues)==True) and (partition_table[i][1]!=False and isStopCondition(partition_table[i][1],OriginalValues)==True):
                    finPartitions.append([partition_table[i][0],info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])])
                    finPartitions.append([partition_table[i][1],'Duplicate'])
                    partition_table[i][0]=False
                    partition_table[i][1]=False
                elif partition_table[i][0]!=False and isStopCondition(partition_table[i][0],OriginalValues)==True:
                    finPartitions.append([partition_table[i][0],info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])])
                    partition_table[i][0]=False
                elif partition_table[i][1]!=False and isStopCondition(partition_table[i][1],OriginalValues)==True:
                    finPartitions.append([partition_table[i][1],info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])])
                    partition_table[i][1]=False
                j=j+2 
            elif i==1:
                if  partition_table[i-1][0]!=False:
                    partition_table[i][0]=[partition_table[i-1][0][g] for g in range(len(partition_table[i-1][0])) if partition_table[i-1][0][g][1]<Partfunction(partition_table[i-1][0])]
                    if partition_table[i][0]==[]:
                        partition_table[i][0]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][0]=[partition_table[i-1][0][g] for g in range(len(partition_table[i-1][0])) if partition_table[i-1][0][g][1]>Partfunction(partition_table[i-1][0]) or partition_table[i-1][0][g][1]==Partfunction(partition_table[i-1][0])]
                        if partition_table[i+1][0]==[]:
                            partition_table[i+1][0]=False
                    if partition_table[i][0]==[] or partition_table[i+1][0]==[]:
                        finPartitions.append([partition_table[i-1][0],info_gain(len(partitionCol),partition_table[i-1][0],partition_table[i-1][1])])
                        partition_table[i-1][0]=False
                        partition_table[i][0]=False
                        partition_table[i+1][0]=False
                    elif (partition_table[i][0]!=False and isStopCondition(partition_table[i][0],OriginalValues)==True) and (partition_table[i+1][0]!=False and isStopCondition(partition_table[i+1][0],OriginalValues)==True):
                        finPartitions.append([partition_table[i][0],info_gain(len(partition_table[i-1][0]),partition_table[i][0],partition_table[i+1][0])])
                        finPartitions.append([partition_table[i+1][0],'Duplicate'])
                        partition_table[i][0]=False
                        partition_table[i+1][0]=False
                    elif partition_table[i][0]!=False and isStopCondition(partition_table[i][0],OriginalValues)==True:
                        finPartitions.append([partition_table[i][0],info_gain(len(partition_table[i-1][0]),partition_table[i][0],partition_table[i+1][0])])
                        partition_table[i][0]=False
                    elif partition_table[i+1][0]!=False and isStopCondition(partition_table[i+1][0],OriginalValues)==True:
                        finPartitions.append([partition_table[i+1][0],info_gain(len(partition_table[i-1][0]),partition_table[i][0],partition_table[i+1][0])])
                        partition_table[i+1][0]=False
                else:
                    partition_table[i][0]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][0]=False
                if partition_table[i-1][1]!=False:
                    partition_table[i][1]=[partition_table[i-1][1][g] for g in range(len(partition_table[i-1][1])) if partition_table[i-1][1][g][1]<Partfunction(partition_table[i-1][1])]
                    if partition_table[i][1]==[]:
                        partition_table[i][1]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][1]=[partition_table[i-1][1][g] for g in range(len(partition_table[i-1][1])) if partition_table[i-1][1][g][1]>Partfunction(partition_table[i-1][1]) or partition_table[i-1][1][g][1]==Partfunction(partition_table[i-1][1])]    
                        if partition_table[i+1][1]==[]:
                            partition_table[i+1][1]=False
                    if partition_table[i][1]==[] or partition_table[i+1][1]==[]:
                        finPartitions.append([partition_table[i-1][1],info_gain(len(partitionCol),partition_table[i-1][0],partition_table[i-1][1])])
                        partition_table[i-1][1]=False
                        partition_table[i][1]=False
                        partition_table[i+1][1]=False
                    elif (partition_table[i][1]!=False and isStopCondition(partition_table[i][1],OriginalValues)==True) and (partition_table[i+1][1]!=False and isStopCondition(partition_table[i+1][1],OriginalValues)==True):
                        finPartitions.append([partition_table[i][1],info_gain(len(partition_table[i-1][1]),partition_table[i][1],partition_table[i+1][1])])
                        finPartitions.append([partition_table[i+1][1],'Duplicate'])
                        partition_table[i][1]=False
                        partition_table[i+1][1]=False
                    elif partition_table[i][1]!=False and isStopCondition(partition_table[i][1],OriginalValues)==True:
                        finPartitions.append([partition_table[i][1],info_gain(len(partition_table[i-1][1]),partition_table[i][1],partition_table[i+1][1])])
                        partition_table[i][1]=False
                    elif partition_table[i+1][1]!=False and isStopCondition(partition_table[i+1][1],OriginalValues)==True:
                        finPartitions.append([partition_table[i+1][1],info_gain(len(partition_table[i-1][1]),partition_table[i][1],partition_table[i+1][1])])
                        partition_table[i+1][1]=False
                else:
                    partition_table[i][1]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][1]=False
                j=j+2
                #print('partition added')
            elif k>0:
                if  partition_table[i-2][j]!=False:
                    partition_table[i][j]=[partition_table[i-2][j][g] for g in range(len(partition_table[i-2][j])) if partition_table[i-2][j][g][1]<Partfunction(partition_table[i-2][j])]
                    if partition_table[i][j]==[]:
                        partition_table[i][j]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][j]=[partition_table[i-2][j][g] for g in range(len(partition_table[i-2][j])) if partition_table[i-2][j][g][1]>Partfunction(partition_table[i-2][j]) or partition_table[i-2][j][g][1]==Partfunction(partition_table[i-2][j])]
                        if partition_table[i+1][j]==[]:
                            partition_table[i+1][j]=False
                    if partition_table[i][j]==[] or partition_table[i+1][j]==[]:
                        finPartitions.append([partition_table[i-2][j],info_gain(len(partition_table[i-3][j]),partition_table[i-2][j],partition_table[i-1][j])])
                        partition_table[i-2][j]=False
                        partition_table[i][j]=False
                        partition_table[i+1][j]=False
                    elif (partition_table[i][j]!=False and isStopCondition(partition_table[i][j],OriginalValues)==True) and (partition_table[i+1][j]!=False and isStopCondition(partition_table[i+1][j],OriginalValues)==True):
                        finPartitions.append([partition_table[i][j],info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])])
                        finPartitions.append([partition_table[i+1][j],'Duplicate'])
                        partition_table[i][j]=False
                        partition_table[i+1][j]=False
                    elif partition_table[i][j]!=False and isStopCondition(partition_table[i][j],OriginalValues)==True:
                        finPartitions.append([partition_table[i][j],info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])])
                        partition_table[i][j]=False
                    elif partition_table[i+1][j]!=False and isStopCondition(partition_table[i+1][j],OriginalValues)==True:
                        finPartitions.append([partition_table[i+1][j],info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])])
                        partition_table[i+1][j]=False    
                    #print('partition added')
                else:
                    partition_table[i][j]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][j]=False
                    k=k*-1
                j=j+1
            elif k<0:
                if partition_table[i-3][j]!=False:
                    partition_table[i][j]=[partition_table[i-3][j][g] for g in range(len(partition_table[i-3][j])) if partition_table[i-3][j][g][1]<Partfunction(partition_table[i-3][j])]
                    if partition_table[i][j]==[]:
                        partition_table[i][j]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][j]=[partition_table[i-3][j][g] for g in range(len(partition_table[i-3][j])) if partition_table[i-3][j][g][1]>Partfunction(partition_table[i-3][j]) or partition_table[i-3][j][g][1]==Partfunction(partition_table[i-3][j])]
                        if partition_table[i+1][j]==[]:
                            partition_table[i+1][j]=False
                    if partition_table[i][j]==[] or partition_table[i+1][j]==[]:
                        finPartitions.append([partition_table[i-3][j],info_gain(len(partition_table[i-5][j]),partition_table[i-3][j],partition_table[i-4][j])])
                        partition_table[i-3][j]=False
                        partition_table[i][j]=False
                        partition_table[i+1][j]=False
                    elif (partition_table[i][j]!=False and isStopCondition(partition_table[i][j],OriginalValues)==True) and (partition_table[i+1][j]!=False and isStopCondition(partition_table[i+1][j],OriginalValues)==True):
                        finPartitions.append([partition_table[i][j],info_gain(len(partition_table[i-3][j]),partition_table[i][j],partition_table[i+1][j])])
                        finPartitions.append([partition_table[i+1][j],'Duplicate'])
                        partition_table[i][j]=False
                        partition_table[i+1][j]=False
                    elif partition_table[i][j]!=False and isStopCondition(partition_table[i][j],OriginalValues)==True:
                        finPartitions.append([partition_table[i][j],info_gain(len(partition_table[i-3][j]),partition_table[i][j],partition_table[i+1][j])])
                        partition_table[i][j]=False
                    elif partition_table[i+1][j]!=False and isStopCondition(partition_table[i+1][j],OriginalValues)==True:
                        finPartitions.append([partition_table[i+1][j],info_gain(len(partition_table[i-3][j]),partition_table[i][j],partition_table[i+1][j])])
                        partition_table[i+1][j]=False
                    #print('partition added')
                else:
                    partition_table[i][j]=False
                    if i+1 <len(partition_table):
                        partition_table[i+1][j]=False
                    k=k*-1
                j=j+1             
        if i==0:
            i=i+1
        elif i==1:
            i=i+2
        else:
            k=k*-1
            i=i+2
    #print(partition_table)
    print('added partitions to table')
    tot_gains=0
    for i in range(len(finPartitions)):
        if finPartitions[i][1]!='No Skip' and finPartitions[i][1]!='Duplicate' and finPartitions[i][1]!=False:
            tot_gains=tot_gains+finPartitions[i][1]
        finPartitions[i]=finPartitions[i][0]
    return finPartitions,tot_gains


def entropy_discretization(attributeValues:list,dataTable:util.DataTable):
    partitionCols=[]
    partitions=[]
    headers=dataTable.columnHeaders
    classValues=attributeValues[0]
    for col in range(1,len(attributeValues)):
        partitionCols.append(createPartionColumn(attributeValues[col],classValues))
    print('partion columns created')
    for i in range(len(partitionCols)):
        #do med
        #med_parts,med_gain=Partition(partitionCols[i],attributeValues[col],util.partitionMed)
        #print(len(med_parts))
        #print('med '+str(i)+' run done')
        #if i==3:
          #  mean_parts,mean_gain=Partition(partitionCols[i],attributeValues[col],util.partitionMean)
        #do mean
       # mean_parts,mean_gain=Partition(partitionCols[i],attributeValues[col],util.partitionMean)
        
       
        #add max gain partitions to partitions
        #if med_gain>mean_gain:
         #   partitions.append(med_parts)
        #else:
        #    partitions.append(mean_parts)
        partitions.append(pt.PartitionTree(partitionCols[i]).finPartitions)
    #discretize
    #print(partitions[0])
    #print(partitions[0][0])
    #print(partitions[0][0][0])
    #print(partitions[0][0][0][0])
    dataTable.partitions=partitions
    #number of parts for each attr
    numParts=[]
    #unique discrete values
    unqDistValues=[]
    #ranges per each discrete value
    ranges=[]
    
    unNamedRecord=[]
    NamedRecord=[]
    for i in range(len(list(set(classValues)))):
        unqDistValues.append(list(set(classValues))[i])
    for i in range(len(list(set(classValues)))):
        numParts.append(headers[0])
    for i in range(len(list(set(classValues)))):
        ranges.append('Class Value')


    inc=1
    for i in range(len(dataTable.partitions)):#all 7 fin parts
        for j in range(len(dataTable.partitions[i])): #each part in a given fin part
                numParts.append(headers[i+1])
                rangersHelper=[]
                for k in range(len(dataTable.partitions[i][j])): #the second val in each part
                    rangersHelper.append(dataTable.partitions[i][j][k][1])
                    dataTable.partitions[i][j][k][1]=inc
                unqDistValues.append(inc)    
                ranges.append(rangersHelper)
                inc=inc+1
        inc=1

    for i in range(len(numParts)):
        unNamedRecord.append([numParts[i],unqDistValues[i],str(min(ranges[i]))+" - "+str(max(ranges[i]))])
        NamedRecord.append([numParts[i],unqDistValues[i],"I"+str(i+1),str(min(ranges[i]))+" - "+str(max(ranges[i]))])
    dataTable.namedDisTbl=NamedRecord
    dataTable.unNamedDistTbl=unNamedRecord
    finpartitionCols=partitions
    #print(finpartitionCols[0])
    print('discretization done')
    #collapse partitions together
    helper_arr=[]
    CollapsePartitions=[]
    for i in range(len(finpartitionCols)):
        for j in range(len(finpartitionCols[i])):
            helper_arr=helper_arr+finpartitionCols[i][j]
        CollapsePartitions.append(helper_arr)
        #print(CollapsePartitions[i])
        helper_arr=[]
    
    print(len(finpartitionCols))    
    #print(finpartitionCols[0])
    #sort partition
    for i in range(len(CollapsePartitions)):
        CollapsePartitions[i].sort(key=util.orderRecords)
        #print(CollapsePartitions[0])
    
    #print(CollapsePartitions)
    print('sort done')
    #clean collumns together
    
    discretizedCols=[]
    for i in range(len(CollapsePartitions)+1):
        if i==0:
            discretizedCols.append(classValues)
        else: 
            discretizedCols.append(CollapsePartitions[i-1])
    #rint('return ready')
    #print(discretizedCols)
    
    
    return discretizedCols,util.values_to_records(discretizedCols)

def TTSplit(records:list, percent):
    data0=[records[i] for i in range(len(records)) if records[i][0]==0.0] 
    data1=[records[i] for i in range(len(records)) if records[i][0]==1.0] 
    data0num=int(len(data0)*percent)
    data1num=int(len(data1)*percent)
    testData=[]
    for i in range(data0num+data1num):
        testData.append(random.sample(data0,data0num))
        testData.append(random.sample(data1,data1num))
    trainData=[records[i] for i in range(len(records)) if records[i] not in testData]
    return trainData,testData

def CalcCoeffient(AttrA,AttrB):
    A_bar=util.mean(AttrA)
    B_bar=util.mean(AttrB)
    A_Min=[AttrA[i]-A_bar for i in range(len(AttrA))]
    B_Min=[AttrB[i]-B_bar for i in range(len(AttrB))]

    Min_Multi=[A_Min[i]*B_Min[i] for i in range(len(AttrA))]
    SQR_A_Min=[math.pow(A_Min[i],2) for i in range(len(AttrA))]
    SQR_B_Min=[math.pow(B_Min[i],2) for i in range(len(AttrB))]

    Min_Multi_Sum=sum(Min_Multi)

    SQR_A_Min_Sum=sum(SQR_A_Min)
    SQR_B_Min_Sum=sum( SQR_B_Min)

    SQRT_A_Min_Sum=math.sqrt(SQR_A_Min_Sum)
    SQRT_B_Min_Sum=math.sqrt( SQR_B_Min_Sum)

    SQR_Product=SQRT_A_Min_Sum*SQRT_B_Min_Sum

    return Min_Multi_Sum/SQR_Product



def  IdentifyRedundancies(data,threshold):
    highlyCorrelated=[]
    #create Correlation Matrix
    correlationMatrix=[['null' for i in range(len(data))] for i in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            if i!=j and j>i:
                correlationMatrix[i][j]=CalcCoeffient(data[i],data[j])
                if abs(correlationMatrix[i][j]) > threshold:
                    highlyCorrelated.append([i,j])
            
    
    return correlationMatrix, highlyCorrelated

def removeRedundancies(redundantArr:list, num_attr):
    #sort by count
    remaining=redundantArr
    rmvInd=[]
    unOrdered=[]
    for i in range(len(redundantArr)):
        for j in range(2):
            unOrdered.append(redundantArr[i][j])
    counts=[]
    for i in range(num_attr):
        counts.append(unOrdered.count(i))
    k=0
    while k<len(remaining):
        for i in range(len(remaining)):
            if counts.index(max(counts)) in remaining[i]:
                remaining[i]=='skip'
                k=k+1
        rmvInd.append(counts.index(max(counts)))
        counts[counts.index(max(counts))]=0
    return rmvInd


    
def generateNamedTable(dataTable:util.DataTable):
    txt="Attribute Name | Discrete Value | Naming | Range\n"
    for i in range(len(dataTable.namedDisTbl)):
        txt=txt+str(dataTable.namedDisTbl[i])+"\n"
    return txt

def generateUnNamedTable(dataTable:util.DataTable):
    txt="Attribute Name | Discrete Value | Range\n"
    for i in range(len(dataTable.unNamedDistTbl)):
        txt=txt+str(dataTable.unNamedDistTbl[i])+"\n"
    return txt

def ConvertRecord_to_itemset(headers,records,namedTable):
    itemset=records
    for i in range(len(records)):
        for j in range(len(records[i])):
            col=headers[j]
            val=itemset[i][j]
            for k in range(len(namedTable)):
                if col in namedTable[k] and val in namedTable[k]:
                    itemset[i][j]=namedTable[k][2]
    return itemset

def generateItemset(itemset):
    txt=""
    for i in range(len(itemset)):
        txt=txt+str(itemset[i])+"\n"
    return txt

def Apriori(itemset):
    itemsetVals=[]
    for i in range(len(itemset)):
        for j in range(len(itemset[i])):
            itemsetVals.append(itemset[i][j])
    Cs=list(set(itemsetVals))
    #print(Cs)
    Ls=[[Cs[i],itemsetVals.count(Cs[i])] for i in range(len(Cs)) if itemsetVals.count(Cs[i])>2]
   
    while len(Ls)!=0:
        freqItemset=Cs
        Cs=[list(combinations(Ls[:][0],2))]
        Ls=[[Cs[i],itemsetVals.count(Cs[i])] for i in range(len(Cs)) if itemsetVals.count(Cs[i])>2]

    return freqItemset

def cleanFreqItemSet(FItemSet,namedTable):
    txt='Removed Itemsets\n'
    itemset=FItemSet
    for i in range(len(itemset)):
        for j in range(len(itemset[i])):
            #find attribute
            name=itemset[i][j]
            for k in range(len(namedTable)):
                if name in namedTable[k]:
                    attribute=namedTable[k][0]
                    siblings=[]
                    for l in range(len(namedTable)):
                        if attribute in namedTable[l]:
                            siblings.append(namedTable[l][2])
                    siblingCt=[FItemSet[i].count(siblings[m]) for m in range(len(siblings))]
                    for n in range(len(siblingCt)):
                        if siblingCt[n]>1:
                            j=len(FItemSet[i])
                            txt=txt+str(FItemSet)+" has been removed due to having a duplicates of attribute: "+attribute+"\n"
                            itemset.remove(itemset[i])
    return itemset,txt

def GenerateAssociationRules(FreqItemSet,threshold,data):
    txt="Association Rules\n"
    subsets=[]
    #generate all possible subsets
    for i in range(len(FreqItemSet)):
        for j in range(len(FreqItemSet[i])-1,-1,-1):
            subsets.append(list(combinations(FreqItemSet[i],j)))
    #for i in range(len(subsets)):
     #   ",".join(subsets)
    #Build rules
    av=[]
    for k in range(len(subsets)):
        for l in range(len(subsets[k])):
            av.append(subsets[k][l])
    av=list(set(av))
    rules=list(permutations(av,2))
    c,s=util.associationCalc(rules,data)
    for i in range(len(rules)):
        txt=txt+str(rules[i][0])+" => "+str(rules[i][1])+ " Confidence: "+str(c[i])+ " Support: "+str(s[i])+"\n"
    txt=txt+"The Following Values Survived (Threshold= "+str(threshold)+"):\n"
    survivedRules=[rules[i] for i in range(len(rules)) if c[i] > threshold]
    sc,ss=util.associationCalc(survivedRules,data)
    for i in range(len(survivedRules)):
        txt=txt+str(survivedRules[i][0])+" => "+str(survivedRules[i][1])+ " Confidence: "+str(sc[i])+ " Support: "+str(ss[i])+"\n"
    return rules,survivedRules,txt

def generateSurvRules(rules,namedTable,format, threshold,data):
    F1txt="The Following Values Survived (Threshold= "+str(threshold)+"):\n"
    F2txt="The Following Values Survived (Threshold= "+str(threshold)+"):\n"
    Ntxt="The Following Values Survived (Threshold= "+str(threshold)+"):\n"

    conf,sup=util.associationCalc(rules,data)
    
    if format=='None':
        for i in range(len(rules)):
            Ntxt=Ntxt+str(rules[i][0])+" => "+str(rules[i][1])+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return Ntxt
    elif format=='Format-1':
        for i in range(len(rules)):
            if len(rules[i][0])>1:
                for j in range(len(rules[i][0])):
                    if j==len(rules[i][0])-1:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"="+str(util.nameToValue(namedTable,[i][0][j]))+" => "
                    else:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"="+str(util.nameToValue(namedTable,[i][0][j]))+" ^ "
            else:
                F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0]))+"="+str(util.nameToValue(namedTable,rules[i][0]))+" => "
            if len(rules[i][1])>1:
                for j in range(len(rules[i][1])):
                    if j==len(rules[i][0])-1:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"="+str(util.nameToValue(namedTable,[i][1][j]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
                    else:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"="+str(util.nameToValue(namedTable,[i][1][j]))+" ^ "
            else:
                F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1]))+"="+str(util.nameToValue(namedTable,rules[i][1]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return F1txt
    elif format=='Format-2':
        for i in range(len(rules)):
            if len(rules[i][0])>1:
                for j in range(len(rules[i][0])):
                    if j==len(rules[i][0])-1:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+str(util.nameToRange(namedTable,[i][0][j]))+" => "
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+str(util.nameToRange(namedTable,[i][0][j]))+" ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0]))+str(util.nameToRange(namedTable,rules[i][0]))+" => "
            if len(rules[i][1])>1:
                for j in range(len(rules[i][1])):
                    if j==len(rules[i][0])-1:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+str(util.nameToRange(namedTable,[i][1][j]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+str(util.nameToRange(namedTable,[i][1][j]))+" ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1]))+str(util.nameToRange(namedTable,rules[i][1]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return F2txt

def predict(rules,dependentVariable,testData,unqV):
    finRules=rules
    #clean rules
    for i in range(len(rules)):
        if util.nameToAttribute(rules[i][1] )!= dependentVariable or len(rules[i][1]) > 1:
            finRules.remove(rules[i][1])
    CorrPredictions=[]
    InCorrPredicions=[]
    for i in range(len(finRules)):
        for k in range(len(testData)):
            if  finRules[i][0] in testData[k]:
                if testData[k][0]==finRules[i][1]:
                    CorrPredictions.append[testData[k][0],finRules[i][1],'correct']
                else:
                   InCorrPredicions.append[testData[k][0],finRules[i][1],'inCorrect'] 
    totalsC=[]
    totalsI=[]
    for i in range(len(unqV)):
        totalsC.append(CorrPredictions.count(unqV[i]))
        totalsI.append(InCorrPredicions.count(unqV[i]))

    total_correct=len(totalsC)
    total_inCorrect=len(totalsI)
    percent_correct=100*total_correct/len(testData)



