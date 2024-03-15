import csv
import util
import math
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

def entropy(s:list,classValues:list,s_class:list):
    unique_classValues=list(set(classValues))
    m=len(unique_classValues)
    pi=[(unique_classValues.count(i)/len(classValues)) for i in range(m)]
   
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
    pi=[(unique_classValues.count(i)/len(classValues)) for i in range(m)]
    return m,pi,unique_classValues

def createPartionColumn(attributeCol:list,classValues:list):
    PartitionColumn=[]
    classValues=classValues
    for val_ind in range(len(attributeCol)):
        PartitionColumn.append([val_ind,attributeCol[val_ind],classValues[val_ind]])
    return PartitionColumn

def isStopCondition(partitionCol:list,all_classValues):
    av=[partitionCol[i][1] for i in range(len(partitionCol))]
    classes=[partitionCol[i][2] for i in range(len(partitionCol))]
    m,pi,_=set_class_info(av,classes)
    if m==1:
        return True
    if min(pi)/max(pi) <0.5:
        if m < math.floor(len(list(set(all_classValues)))/2) or m==math.floor(len(list(set(all_classValues)))/2):
            return True
    return False

def medianPartition(partitionCol:list,all_classValues):
    #create table to hold partioned sets where each r/c = A11A21 etc
    partition_table=[[0 for i in range(2)] for i in range(len(partitionCol)*len(partitionCol)*10)]
    print('created table: '+str(len(partition_table)))
    #patrition set until stop adding each to table
    for i in range(len(partition_table)):
        for j in range(2):
            if i ==0:
                k=1
                partition_table[i][0]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]<util.partitionMed(partitionCol)]#A1
                partition_table[i][1]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]>util.partitionMed(partitionCol) or partitionCol[i][1]==util.partitionMed(partitionCol)]#A2
                print('partition added')
            elif i==1:
                if len(partition_table[i-1][j])!=1:
                    partition_table[i][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]<util.partitionMed(partition_table[i-1][j])]
                    partition_table[i+1][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]>util.partitionMed(partition_table[i-1][j]) or partition_table[i-1][j][i][1]==util.partitionMed(partition_table[i-1][j])]
                    i=i+2#inc rows
                    k=k*-1
                    print('partition added')
                else:
                    i=i+2#inc rows
                    k=k*-1
            elif k>0:
                if len(partition_table[i-2][j])!=1:
                    partition_table[i][j]=[partition_table[i-2][j][i] for i in range(len(partition_table[i-2][j])) if partition_table[i-2][j][i][1]<util.partitionMed(partition_table[i-2][j])]
                    partition_table[i+1][j]=[partition_table[i-2][j][i] for i in range(len(partition_table[i-2][j])) if partition_table[i-2][j][i][1]>util.partitionMed(partition_table[i-2][j]) or partition_table[i-2][j][i][1]==util.partitionMed(partition_table[i-2][j])]
                    i=i+2#inc rows
                    k=k*-1
                    print('partition added')
                else:
                    i=i+2#inc rows
                    k=k*-1
            elif k<0:
                if len(partition_table[i-4][j])!=1:
                    partition_table[i][j]=[partition_table[i-4][j][i] for i in range(len(partition_table[i-4][j])) if partition_table[i-4][j][i][1]<util.partitionMed(partition_table[i-4][j])]
                    partition_table[i+1][j]=[partition_table[i-4][j][i] for i in range(len(partition_table[i-4][j])) if partition_table[i-4][j][i][1]>util.partitionMed(partition_table[i-4][j]) or partition_table[i-4][j][i][1]==util.partitionMed(partition_table[i-4][j])]
                    i=i+2#inc rows
                    k=k*-1
                    print('partition added')
                else:
                    i=i+2#inc rows
                    k=k*-1
    print('added partitions to table')
    #add stop flag to actual cell
    for i in range(len(partition_table)):
        for j in range(len(partition_table)):
            if i==0:
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    partition_table[i][j].append('stop')
                    k=1
            elif k>0 :
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    if partition_table[i-2][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-2][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                        
                if isStopCondition(partition_table[i+1][j],all_classValues)==True:
                    if partition_table[i-2][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-2][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                k=k*-1
                i=i+2    
            elif k<0 :
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    if partition_table[i-4][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-4][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                        
                if isStopCondition(partition_table[i+1][j],all_classValues)==True:
                    if partition_table[i-4][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-4][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                k=k*-1
                i=i+2    
    print('added flags to table')
    #calculate gain using tabular logic find parent and sibling for each stop
    gains=[]
    partitions=[]
    for i in range(len(partition_table)):
        for j in range(len(partition_table)):
            if i==0:
                if  partition_table[i][0][-1]=='stop' and partition_table[i][1][-1]=='stop':
                    partitions.append(partition_table[i][0][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i][1][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])
                    gains.append(ig)
                    gains.append('n/a')
                    j=j+1
                    k=1
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])
                    gains.append(ig)
                    k=1
            elif k>0 :
                if partition_table[i][j][-1]=='stop' and  partition_table[i+1][j][-1] =='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                    gains.append('n/a')
                    k=k*-1
                    i=i+2
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                elif partition_table[i+1][j][-1]=='stop':
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                k=k*-1
                i=i+2    
            elif k<0 :
                if partition_table[i][j][-1]=='stop' and  partition_table[i+1][j][-1] =='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                    gains.append('n/a')
                    k=k*-1
                    i=i+2
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                elif partition_table[i+1][j][-1]=='stop':
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                k=k*-1
                i=i+2    
    return partitions,gains

def meanPartition(partitionCol:list,all_classValues):
    #create table to hold partioned sets where each r/c = A11A21 etc
    partition_table=[[0]*2]*len(partitionCol)*len(partitionCol)*10
    #patrition set until stop adding each to table
    for i in range(len(partition_table)):
        for j in range(len(partition_table)):
            if i ==0:
                k=1
                partition_table[i][0]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]<util.partitionMean(partitionCol)]#A1
                partition_table[i][1]=[partitionCol[i] for i in range(len(partitionCol)) if partitionCol[i][1]>util.partitionMean(partitionCol) or partitionCol[i][1]==util.partitionMean(partitionCol)]#A2
            elif k>0:
                if len(partition_table[i-2][j])!=1:
                    partition_table[i][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]<util.partitionMean(partition_table[i-1][j])]
                    partition_table[i+1][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]>util.partitionMean(partition_table[i-1][j]) or partition_table[i-1][j][i][1]==util.partitionMean(partition_table[i-1][j])]
                    i=i+2#inc rows
                    k=k*-1
                else:
                    i=i+2#inc rows
                    k=k*-1
            elif k<0:
                if len(partition_table[i-4][j]!=1):
                    partition_table[i][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]<util.partitionMean(partition_table[i-1][j])]
                    partition_table[i+1][j]=[partition_table[i-1][j][i] for i in range(len(partition_table[i-1][j])) if partition_table[i-1][j][i][1]>util.partitionMean(partition_table[i-1][j]) or partition_table[i-1][j][i][1]==util.partitionMean(partition_table[i-1][j])]
                    i=i+2#inc rows
                    k=k*-1
                else:
                    i=i+2#inc rows
                    k=k*-1
    #add stop flag to actual cell
    for i in range(len(partition_table)):
        for j in range(len(partition_table)):
            if i==0:
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    partition_table[i][j].append('stop')
                    k=1
            elif k>0 :
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    if partition_table[i-2][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-2][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                        
                if isStopCondition(partition_table[i+1][j],all_classValues)==True:
                    if partition_table[i-2][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-2][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                k=k*-1
                i=i+2    
            elif k<0 :
                if isStopCondition(partition_table[i][j],all_classValues)==True:
                    if partition_table[i-4][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-4][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                        
                if isStopCondition(partition_table[i+1][j],all_classValues)==True:
                    if partition_table[i-4][j][-1]=='stop':
                        partition_table[i][j].append('void')
                        
                    elif partition_table[i-4][j][-1]=='void':
                        partition_table[i][j].append('void')
                        
                    else:
                        partition_table[i][j].append('stop')
                k=k*-1
                i=i+2    
    #calculate gain using tabular logic find parent and sibling for each stop
    gains=[]
    partitions=[]
    for i in range(len(partition_table)):
        for j in range(len(partition_table)):
            if i==0:
                if  partition_table[i][0][-1]=='stop' and partition_table[i][1][-1]=='stop':
                    partitions.append(partition_table[i][0][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i][1][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])
                    gains.append(ig)
                    gains.append('n/a')
                    j=j+1
                    k=1
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partitionCol),partition_table[i][0],partition_table[i][1])
                    gains.append(ig)
                    k=1
            elif k>0 :
                if partition_table[i][j][-1]=='stop' and  partition_table[i+1][j][-1] =='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                    gains.append('n/a')
                    k=k*-1
                    i=i+2
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                elif partition_table[i+1][j][-1]=='stop':
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-2][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                k=k*-1
                i=i+2    
            elif k<0 :
                if partition_table[i][j][-1]=='stop' and  partition_table[i+1][j][-1] =='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                    gains.append('n/a')
                    k=k*-1
                    i=i+2
                elif partition_table[i][j][-1]=='stop':
                    partitions.append(partition_table[i][j][:len(partition_table[i][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                elif partition_table[i+1][j][-1]=='stop':
                    partitions.append(partition_table[i+1][j][:len(partition_table[i+1][j])-1])
                    ig=info_gain(len(partition_table[i-4][j]),partition_table[i][j],partition_table[i+1][j])
                    gains.append(ig)
                k=k*-1
                i=i+2    
    return partitions,gains

def entropy_discretization(attributeValues:list):
    partitionCols=[]
    partitions=[]
    classValues=attributeValues[0]
    for col in range(1,len(attributeValues)):
        partitionCols.append(createPartionColumn(attributeValues[col],classValues))
    print('partion columns created')
    for i in range(len(partitionCols)):
        #do med
        med_parts,med_gains=medianPartition(partitionCols[i],classValues)
        print('med '+str(i)+' run done')
        #cal total med gain
        t_med_gain=0
        for gain in med_gains:
            if gain!='n/a':
                t_med_gain=t_med_gain+gain
        #do mean
        mean_parts,mean_gains=meanPartition(partitionCols[i],classValues)
        print('mean '+str(i)+' run done')
        #calc total mean gain
        t_mean_gain=0
        for gain in mean_gains:
            if gain!='n/a':
                t_mean_gain=t_mean_gain+gain
        #add max gain partitions to partitions
        if t_med_gain>t_mean_gain:
            partitions.append(med_parts)
        else:
            partitions.append(mean_parts)
    #discretize
    for i in range(len(partitions)):
        inc=1
        for part in partitions[i]:
            part[1]=[inc for i in range(len(part[1]))]
            inc=inc+1
    finpartitionCols=[]
    print('discretization done')
    #collapse partitions together
    for i in range(len(partitions)):
        helper_arr=[]
        for part in partitions[i]:
            helper_arr=helper_arr+part
        finpartitionCols.append(helper_arr)        
    #sort partition
    for col in finpartitionCols:
        for i in range(len(finpartitionCols[col])):
            for j in range(i+1,len(finpartitionCols[col])):
                if finpartitionCols[col][i][0] > finpartitionCols[col][j][0]:
                    finpartitionCols[col][i], finpartitionCols[col][j] = finpartitionCols[col][j], finpartitionCols[col][i]
    print('sort done')
    #clean collumns together
    discretizedCols=[]
    discretizedCols=discretizedCols+classValues#addAtribute0
    for i in range(len(finpartitionCols)):
        discretizedCols=discretizedCols+finpartitionCols[i][1]
    print('return ready')
    return discretizedCols,util.values_to_records(discretizedCols)