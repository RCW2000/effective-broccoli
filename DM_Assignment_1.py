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


def createPartionColumn(attributeCol:list,classValues:list):
    PartitionColumn=[]
    classValues=classValues
    for val_ind in range(len(attributeCol)):
        PartitionColumn.append([val_ind,attributeCol[val_ind],classValues[val_ind]])
    return PartitionColumn

def entropy_discretization(attributeValues:list,dataTable:util.DataTable):
    partitionCols=[]
    partitions=[]
    headers=dataTable.columnHeaders
    classValues=attributeValues[0]
    for col in range(1,len(attributeValues)):
        partitionCols.append(createPartionColumn(attributeValues[col],classValues))
    print('partion columns created')
    for i in range(len(partitionCols)):
            partitions.append(pt.PartitionTree(partitionCols[i]).finPartitions)

    dataTable.partitions=partitions
    #number of parts for each attr
    numParts=[]
    #unique discrete values
    unqDistValues=[]
    #ranges per each discrete value
    ranges=[]
    classes=[]
    unNamedRecord=[]
    NamedRecord=[]
    for i in range(len(list(set(classValues)))):
        unqDistValues.append(list(set(classValues))[i])
    for i in range(len(list(set(classValues)))):
        numParts.append(headers[0])
    for i in range(len(list(set(classValues)))):
        classes.append('Class Value')

    for i in range(len(dataTable.partitions)):#all 7 fin parts
        inc=1
        for j in range(len(dataTable.partitions[i])): #each part in a given fin part
            print(inc)
            numParts.append(headers[i+1])
            rangersHelper=[]
            for k in range(len(dataTable.partitions[i][j])): #the second val in each part
                rangersHelper.append(dataTable.partitions[i][j][k][1])
                dataTable.partitions[i][j][k][1]=inc
            unqDistValues.append(inc)    
            ranges.append(rangersHelper)
            inc=inc+1
        
    for i in range(len(list(set(classValues)))):
        unNamedRecord.append([numParts[i],unqDistValues[i],classes[i]])
        NamedRecord.append([numParts[i],unqDistValues[i],"I"+str(i+1),classes[i]])
    for i in range(len(list(set(classValues))),len(numParts)):
        unNamedRecord.append([numParts[i],unqDistValues[i],str(min(ranges[i-len(list(set(classValues)))]))+" - "+str(max(ranges[i-len(list(set(classValues)))]))])
        NamedRecord.append([numParts[i],unqDistValues[i],"I"+str(i+1),str(min(ranges[i-len(list(set(classValues)))]))+" - "+str(max(ranges[i-len(list(set(classValues)))]))])
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

    
    
    return discretizedCols,util.values_to_records(discretizedCols)
def setVal(inc):
    return inc
def TTSplit(records:list, percent):
    data0=[records[i] for i in range(len(records)) if records[i][0]==0.0] 
    data1=[records[i] for i in range(len(records)) if records[i][0]==1.0] 
    data0num=int(len(data0)*percent)
    data1num=int(len(data1)*percent)
    testData=random.sample(data0,data0num)+random.sample(data1,data1num)
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
    remaining=redundantArr.copy()
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

def getItemset(namedTable):
    return [item[2] for item in namedTable]

def ConvertRecord_to_itemsets(namedTable,records,headers):
    itsRecords=records.copy()
    for i in range(len(itsRecords)):
        for j in range(len(itsRecords[i])):
            # find header
            header=headers[j]
            # find number
            value=itsRecords[i][j]
            for k in range(len(namedTable)):
                if header in namedTable[k] and value in namedTable[k]:
                    # get name
                    name=namedTable[k][2]
            # set value to name
            itsRecords[i][j]=name
    #output attribute records
    return itsRecords



def generateItemset(itemset):
    txt=""
    for i in range(len(itemset)):
        txt=txt+str(itemset[i])+"\n"
    return txt
from itertools import chain
def Apriori(namedTable, records, headers,threshold=2):
    itemset=getItemset(namedTable)
    records=ConvertRecord_to_itemsets(namedTable,records,headers)
    Lset=[]
    c1=itemset
    flat_records = list(chain.from_iterable(records))
    L1=[([c1[i]],flat_records.count(c1[i])) for i in range(len(c1)) if flat_records.count(c1[i])>threshold or flat_records.count(c1[i])==threshold]
    Lset.append(L1)
    inc=0
    while True:
        inc=inc+1
        if len(Lset)==1:
            #create c
            c=[tup[0] for tup in Lset[-1]]
            #concat c
            concat_c=[]
            for i in range(len(c)-1):
                for j in range(i+inc,len(c)):
                    concat_c.append(c[i]+c[j])
            #create l
            counts=[]

            for i in range(len(concat_c)):
                count=0
                flag = True
                for record in records:
                    for j in range(len(concat_c[i])):
                        if concat_c[i][j] not in record:
                            flag = False
                    if flag==True:
                        count=count+1
                counts.append(count)
            l=[(concat_c[i],counts[i]) for i in range(len(concat_c)) if counts[i] > threshold or counts[i] == threshold]
            #add l if not empty
            Lset.append(l)
            #if empty stop
        else:
            # create c
            c = [tup[0] for tup in Lset[-1]]
            # concat c
            concat_c = []
            for i in range(len(c) - 1):
                if i+inc < len(c):
                    for j in range(i + inc, len(c)):
                        concat_c.append(c[i] +[c[j][0]])
                else:
                    return c
            # create l
            counts = []

            for i in range(len(concat_c)):
                count = 0
                flag = True
                for record in records:
                    for j in range(len(concat_c[i])):
                        if concat_c[i][j] not in record:
                            flag = False
                        else:
                            flag=True
                    if flag == True:
                        count = count + 1
                counts.append(count)
            l = [(concat_c[i], counts[i]) for i in range(len(concat_c)) if
                 counts[i] > threshold or counts[i] == threshold]
            # add l if not empty
            if len(l)>0:
                Lset.append(l)
            # if empty stop
            else:
                break

    return [tup[0] for tup in Lset[-1]]

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

def GenerateAssociationRules(FreqItemSet,threshold,namedTable,records,headers):
    txt="Association Rules\n"
    subsets=[]
    #generate all possible subsets
    for k in range(len(FreqItemSet)):
        subsets.append([FreqItemSet[k][i:j] for i in range(len(FreqItemSet[k])) for j in range(i+1,len(FreqItemSet[k])+1)])
    #Build rules
    rules=[]
    for subset in subsets:
        for i in range(len(subset) - 1):
            if i + 1 < len(subset):
                for j in range(i + 1, len(subset)):
                    if len(set(subset[i]).intersection(subset[j]))==0:
                        rules.append([subset[i],subset[j]])

    c,s=util.associationCalc(rules,ConvertRecord_to_itemsets(namedTable,records,headers))
    for i in range(len(rules)):
        txt=txt+str(rules[i][0])+" => "+str(rules[i][1])+ " Confidence: "+str(c[i])+ " Support: "+str(s[i])+"\n"
    txt=txt+"The Following Values Survived (Threshold= "+str(threshold)+"):\n"
    survivedRules=[rules[i] for i in range(len(rules)) if c[i] > threshold]
    sc,ss=util.associationCalc(survivedRules,ConvertRecord_to_itemsets(namedTable,records,headers))
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
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"["+str(util.nameToRange(namedTable,[i][0][j]))+"]"+" => "
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"["+str(util.nameToRange(namedTable,[i][0][j]))+"]" + " ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0]))+"["+str(util.nameToRange(namedTable,rules[i][0]))+"]"+ " => "
            if len(rules[i][1])>1:
                for j in range(len(rules[i][1])):
                    if j==len(rules[i][0])-1:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"["+str(util.nameToRange(namedTable,[i][1][j]))+"]"+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"["+str(util.nameToRange(namedTable,[i][1][j]))+"]"+" ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1]))+"["+str(util.nameToRange(namedTable,rules[i][1]))+"]"+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return F2txt

def predict(rules,dependentVariable,testData,nameTable,headers):
    finRules=rules.copy()
    testData=testData.copy()
    #clean rules
    for i in range(len(rules)):
        if util.nameToAttribute(nameTable,rules[i][1]) != dependentVariable or len(rules[i][1]) > 1:
            finRules.remove(rules[i])
    predValues=list(set([finRules[i][1] for i in finRules]))#values that can be predicted
    predictions=[]
    for rule in finRules:
        for record in testData:
             if set(record[0]).intersection(set(util.nameToValue(predValues)))>0:
                # check if rule applies
                if len(set([util.nameToValue(nameTable,record) for record in rule[0]]).intersection(set(record)))==len(rule[0]):
                    #check if prrediction is correct
                    if len(set(record[0]).intersection(set(util.nameToValue(nameTable,rule[1]))))==1:
                        predictions.append([True,rule[1]])
                    else:
                        predictions.append([False,rule[1],record[0]])

    total_correct=0
    total_incorrect=0
    correct=[]
    incorrect=[]

    for prediction in predictions:
        if prediction[0]==True:
            total_correct=total_correct+1
            correct.append(util.nameToValue(nameTable,prediction[1]))
        else:
            total_incorrect=total_incorrect+1
            incorrect.append([util.nameToValue(nameTable,prediction[1]),util.nameToValue(nameTable,prediction[2])])

    unq_val=list(set([record[0] for record in testData]))
    counts = [[0, 0] for i in range(len(unq_val))]

    pred_matrix="Unique Values in the |  Predicted Values  | \n"
    pred_matrix=pred_matrix+"Dependent variable    |_______________________"
    for i in range(len(predValues)):
        pred_matrix+=str(predValues[i])+"         |"
    pred_matrix+="\n(Descision Attribute) |             |           |\n"
    pred_matrix+="--------------------------------------------------------------------\n"
    for i in range(len(unq_val)):
        for j in range(i+1,len(unq_val)):
            if i==j:#correct predictions
                pred_matrix+=str(unq_val[i])+"                |"+str(correct.count(unq_val[i]))
            else:
                #incorrect thought be j
                j_count=0
                for bad in incorrect:
                    if set(bad[0]).intersection(set(unq_val[i]))>0:
                        if set(bad[1]).intersection(set(unq_val[j]))>0:
                            j_count+=1
                pred_matrix+="|         "+str(j_count)+"         |"
    pred_matrix+="\n"
    pred_matrix+="Total Correct: "+str(len(correct))+"\n"
    return pred_matrix







