import csv
import util
import math
import random
import TreePartition as pt
import gc
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
    classValues=list(map(int,attributeValues[0]))
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
        classes.append(str(list(set(classValues))[i]))

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
            discretizedCols.append([data[1] for data in CollapsePartitions[i-1]])

    
    
    return discretizedCols,util.values_to_records(discretizedCols)
def setVal(inc):
    return inc
def TTSplit(records:list, percent):
    data0=[records[i] for i in range(len(records)) if records[i][0]==0] 
    data1=[records[i] for i in range(len(records)) if records[i][0]==1] 
    data0num=int(len(data0)*percent)
    data1num=int(len(data1)*percent)
    testData=util.sample(data0,data0num)+util.sample(data1,data1num)
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

def removeRedundancies(redundantArr:list):
    if len(redundantArr)==0:
        return None
    print(redundantArr)
    #sort by count
    remaining=redundantArr.copy()
    rmvInd=[]
    flat=[]
    for i in range(len(remaining)):
        for j in range(2):
            flat.append(remaining[i][j])
    counts=[]
    
    for i in range(max(list(set(flat)))+2):
        if i-1 in list(set(flat)):
            counts.append(flat.count(i-1))
        else:
            counts.append(0)
    
    #print(counts)
    rmvInd=[]
    while len(remaining)>0:
        #find and remove all refs to max count
        maximum=max(counts)
        max_ind=counts.index(maximum)#ref to remove
        if len(redundantArr)==1:
            v=max_ind-1
        else:
            v=max_ind
        counts[max_ind]=0
        if v in flat:
            rmvInd.append(max_ind)
            remaining=[pair for pair in remaining if v not in pair]
            #recount
            if len(remaining)>0:
                flat=[]
                for i in range(len(remaining)):
                    for j in range(2):
                        flat.append(remaining[i][j])  

                counts=[]
                if len(flat)>0:
                    for i in range(max(list(set(flat)))+1):
                        if i in list(set(flat)):
                            counts.append(flat.count(i))
                        else:
                            counts.append(0)             
                #loop again
        print(rmvInd)
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

def Apriori(namedTable, records, headers,threshold=2):
    itemset=getItemset(namedTable)
    records=ConvertRecord_to_itemsets(namedTable,records,headers)
    Lset=[]
    c1=itemset
    flat_records=[record[i] for record in records for i in range(len(record))]
    L1=[([c1[i]],flat_records.count(c1[i])) for i in range(len(c1)) if flat_records.count(c1[i])>threshold or flat_records.count(c1[i])==threshold]
    Lset.append(L1)
    inc=1
    while True:
        
        if len(Lset)==1:
            #create c
            c=[tup[0] for tup in Lset[-1]]
            #concat c
            concat_c = []
            for i in range(len(c)):
                for j in range(i + 1, len(c)):
                    if j>i:
                        concat_c.append(c[i] +c[j])
            #create l
            counts=[]

            for i in range(len(concat_c)):
                count=0
                
                for record in records:
                    flag = True
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
            #create blocks
            c = [tup[0] for tup in Lset[-1]]
            neighbor_tuples=[]#group like tuples together
            neighbor_helper=[]
            resident_arr=[]
            resident_helper=[]
            for i in range(1,len(c)):
                if c[i][:inc] == c[i-1][:inc]:
                    neighbor_helper.append(c[i-1][:inc+1])
                    resident_helper.append(c[i-1][-1])
                else:
                    neighbor_helper.append(c[i-1][:inc+1])
                    resident_helper.append(c[i-1][-1])
                    resident_arr.append(resident_helper)
                    neighbor_tuples.append([neighbor_helper,resident_arr])
                    neighbor_helper=[]
                    resident_arr=[]
                    resident_helper=[]
            
            
            concat_c=[]
            for block in neighbor_tuples:
                for i in range(len(block[0])-1):
                    for j in range(i+1,len(block[1][0])):
                        concat_c.append(block[0][i]+[block[1][0][j]])

            #count
            counts=[]
            for i in range(len(concat_c)):
                count=0
                for record in records:
                    flag = True
                    for j in range(len(concat_c[i])):
                        if concat_c[i][j] not in record:
                            flag = False
                    if flag==True:
                        count=count+1
                counts.append(count)
            l=[(concat_c[i],counts[i]) for i in range(len(concat_c)) if counts[i] > threshold or counts[i] == threshold]
            if len(l)==0:
                return [tup[0] for tup in Lset[-1]]
            else:
                Lset.append(l)
                inc=inc+1
                #if len(Lset)==2:
                    #del Lset[0]
                    #gc.collect()
            #if empty stop


    

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
        list=[FreqItemSet[k][i:j] for i in range(len(FreqItemSet[k])) for j in range(i+1,len(FreqItemSet[k])+1)]
        subsets.append(list)
    #Build rules
    rules=[]
    for subset in subsets:
        for i in range(len(subset)):
            if i + 1 < len(subset):
                for j in range(i + 1, len(subset)):
                    if len(set(subset[i]).intersection(subset[j]))==0:
                        rules.append([subset[i],subset[j]])
                        rules.append([subset[j],subset[i]])
            


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
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"="+str(util.nameToValue(namedTable,rules[i][0][j]))+" => "
                    else:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"="+str(util.nameToValue(namedTable,rules[i][0][j]))+" ^ "
            else:
                F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][0][0]))+"="+str(util.nameToValue(namedTable,rules[i][0][0]))+" => "
            if len(rules[i][1])>1:
                for j in range(len(rules[i][1])):
                    if j==len(rules[i][0])-1:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"="+str(util.nameToValue(namedTable,rules[i][1][j]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
                    else:
                        F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"="+str(util.nameToValue(namedTable,rules[i][1][j]))+" ^ "
            else:
                F1txt=F1txt+str(util.nameToAttribute(namedTable,rules[i][1][0]))+"="+str(util.nameToValue(namedTable,rules[i][1][0]))+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return F1txt
    elif format=='Format-2':
        for i in range(len(rules)):
            if len(rules[i][0])>1:
                for j in range(len(rules[i][0])):
                    if j==len(rules[i][0])-1:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"["+str(util.nameToRange(namedTable,rules[i][0][j]))+"]"+" => "
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][j]))+"["+str(util.nameToRange(namedTable,rules[i][0][j]))+"]" + " ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][0][0]))+"["+str(util.nameToRange(namedTable,rules[i][0][0]))+"]"+ " => "
            if len(rules[i][1])>1:
                for j in range(len(rules[i][1])):
                    if j==len(rules[i][0])-1:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"["+str(util.nameToRange(namedTable,rules[i][1][j]))+"]"+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
                    else:
                        F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][j]))+"["+str(util.nameToRange(namedTable,rules[i][1][j]))+"]"+" ^ "
            else:
                F2txt=F2txt+str(util.nameToAttribute(namedTable,rules[i][1][0]))+"["+str(util.nameToRange(namedTable,rules[i][1][0]))+"]"+ " Confidence: "+str(conf[i])+ " Support: "+str(sup[i])+"\n"
        return F2txt

def predict(rules,dependentVariable,testData,nameTable,headers):
    finRules=rules.copy()
    #testData=testData.copy()
    records=ConvertRecord_to_itemsets(nameTable,testData,headers)
    #clean rules
    for i in range(len(rules)):
        if len(rules[i][1]) > 1 or util.nameToAttribute(nameTable,rules[i][1][0]) != dependentVariable:
            #print(rules[i][1][0])
            #print( util.nameToAttribute(nameTable,rules[i][1][0]))
            finRules.remove(rules[i])
    predValues=list(set([finRules[i][1][0] for i in range(len(finRules))]))#values that can be predicted
    predictions=[]
    for record in records:
        actual=record[0]
        done=False
        for rule in rules:
            if done==False:
                # check if rule applies
                target=rule[1][0]
                flag=True
                for item in rule[0]:
                    if item not in record:
                        flag=False
                if flag==True:
                    #check if prrediction is correct
                    if actual==target:
                        predictions.append([True,rule[1][0]])
                        done=True
                    else:
                        predictions.append([False,rule[1][0],record[0]])
                        done=True

    total_correct=0
    total_incorrect=0
    correct=[]
    incorrect=[]

    for prediction in predictions:
        if prediction[0]==True:
            total_correct=total_correct+1
            correct.append(prediction[1])
        else:
            total_incorrect=total_incorrect+1
            incorrect.append([prediction[1],prediction[2]])

    unq_val=list(set([record[0] for record in testData]))
    perCorr = []

    pred_matrix="|Unique Values in the Dependent variable |  Predicted Values   \n"
    pred_matrix=pred_matrix+"|             (Descision Attribute)                 |"
    for i in range(len(predValues)):
        pred_matrix+="       "+str(int(util.nameToValue(nameTable,predValues[i])))+"  "
    pred_matrix+="\n---------------------------------------------------------------------------------"
    for i in range(len(unq_val)):
        pred_matrix+="\n                                                           "+str(util.nameToValue(nameTable,unq_val[i]))+"|    "
        perCorr_helper=[]
        for j in range(len(unq_val)):
            if i==j:#correct predictions
                pred_matrix+=str(correct.count(unq_val[i]))+"     "
            else:
                #incorrect thought be j
                j_count=0
                for bad in incorrect:
                    if bad[0] in unq_val[i]:
                        if bad[1] in unq_val[j]:
                            j_count+=1
                pred_matrix+=str(j_count)+"    "
                perCorr_helper.append(j_count)
        #sum j_counts
        sum=0
        for num in perCorr_helper:
            sum+=num
        perCorr.append((((correct.count(unq_val[i])+sum))/(total_correct+total_incorrect))*100)
    pred_matrix+="\n---------------------------------------------------------------------------------\n"
    for i in range(len(unq_val)):
        pred_matrix+=str(util.nameToValue(nameTable,unq_val[i]))+": Percent of Correct Prediction = "+str(perCorr[i])+"\n"
    pred_matrix+="\n---------------------------------------------------------------------------------"
    pred_matrix+="\nTotal Correct: "+str(total_correct)+"   Total Incorrect: "+str(total_incorrect)+"  ("+str((total_incorrect/(total_incorrect+total_correct))*100)+"%)"
    return pred_matrix







