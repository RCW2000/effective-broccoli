import util
import DM_Assignment_1 as dm
#k means clustering
def k_meansSeeds(partition_col):
    small_seed=min([row[1] for row in partition_col])
    med_seed=(util.median([row[1] for row in partition_col]))
    large_seed=max([row[1] for row in partition_col])
    return[small_seed,med_seed,large_seed]

def clustering(part_col,k):
    seeds=k_meansSeeds(part_col)
    init_seeds=seeds.copy()
    old_cluster=None
    new_cluster=[]
    while new_cluster!=old_cluster:
        old_cluster=new_cluster
        new_cluster=[[],[],[]]
        for i in range(len(part_col)):
            dists=[abs(part_col[i][1]-seeds[j]) for j in range(len(seeds))]
            cluster_num=dists.index(min(dists))
            new_cluster[cluster_num].append(part_col[i])
            seeds[cluster_num]=util.mean([seeds[cluster_num]]+[part_col[i][1]])
    return init_seeds,new_cluster
        
            

def k_means(dataTable:util.DataTable,attribute_cols,headers,k=3):
    #partition cols for each attribute
    part_cols=[dm.createPartionColumn(attribute_cols[i],attribute_cols[0]) for i in range(1,len(attribute_cols))] 
    init_seeds=[]
    clusters_sets=[]
    for part in part_cols:
        s,c=clustering(part,k)
        init_seeds.append(s)
        clusters_sets.append(c)
    ranges=[i for i in list(set(attribute_cols[0]))]
    clust_set=["L","M","H"]
    names=[headers[0] for i in list(set(attribute_cols[0]))]
    disVals=[i for i in list(set(attribute_cols[0]))]

    for cSet in range(len(clusters_sets)):
        ind=0
        for cluster in range(len(clusters_sets[cSet])):
            names.append(headers[cSet+1])
            range_helper=[]
            for value in clusters_sets[cSet][cluster]:
                range_helper.append(value[1])
                value[1]=clust_set[ind]
            disVals.append(clust_set[ind])
            ranges.append(range_helper)
            ind=ind+1
    disRecords=[]
    for i in range(len(names)):
        if i <len(list(set(attribute_cols[0]))):
            disRecords.append([names[i],disVals[i],ranges[i]])
        else:
            disRecords.append([names[i],disVals[i],str(min(ranges[i]))+" - "+str(max(ranges[i]))])
    
    dataTable.partitions=clusters_sets
    dataTable.unNamedDistTbl=disRecords
    print('discretization done')
    #collapse partitions together
    finpartitionCols=clusters_sets
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
            discretizedCols.append(attribute_cols[0])
        else: 
            discretizedCols.append([data[1] for data in CollapsePartitions[i-1]])

    
    
    return discretizedCols,util.values_to_records(discretizedCols),init_seeds

    
def generateClusterTable(dataTable:util.DataTable):
    txt="Attribute Name [ Low Seed | Med Seed | High Seed ]\n"
    for i in range(1,len(dataTable.currentHeaders)):
        txt+=dataTable.currentHeaders[i]+"  "+str(dataTable.initCSeeds[i-1])+"\n"
    txt+="Attribute Name | Discrete Value | Range\n"
    for i in range(len(dataTable.unNamedDistTbl)):
        txt=txt+str(dataTable.unNamedDistTbl[i])+"\n"
    return txt

def tt_split(percentage,records):
    train=records[:int(len(records)*percentage)]
    test=records[int(len(records)*percentage):]
    return train,test

def BuildMarkov(attributeVals,headers):
    '''
    list +text
    
    '''
    print(attributeVals[0][:len(attributeVals[0])-1])
    cluster_set=["L","M","H"]
    classv=list(set(attributeVals[0]))
    classv.sort()
    class_cts=[attributeVals[0][:len(attributeVals[0])-1].count(cv) for cv in classv]
    markovList=[]
    #start
    ml_helper=[]
    for i in range(len(classv)):
        ml_helper.append(['start',classv[i],class_cts[i]/len(attributeVals[0])])
    markovList.append(ml_helper)
    #class values
    for i in range(len(classv)):
        ml_helper=[]
        for j in range(len(classv)):
            ml_helper.append([classv[i],classv[j],sum([1 for k in range(len(attributeVals[0])-2) if attributeVals[0][k]==classv[i] and attributeVals[0][k+1]==classv[j]])/class_cts[i]])
        markovList.append(ml_helper)

    
    ml_big=[]
    #other attributes
    part_cols=[dm.createPartionColumn(attributeVals[i],attributeVals[0]) for i in range(1,len(attributeVals))]
    classRNs=[]
    
    #emissions
    ems=[]
    sems=[]
    for j in range(len(classv)):
        totalsms=0
        for i in range(len(part_cols)):
            for k in range(len(cluster_set)):
                emv=0
                for l in range(len(part_cols[i])):
                    if part_cols[i][l][1]==cluster_set[k] and part_cols[i][l][2]==classv[j]:
                        emv+=1
                totalsms+=emv
                if emv!=0:
                    ems.append([headers[i+1],cluster_set[k]])
                    sems.append([classv[j],headers[i+1],cluster_set[k]])
        classRNs.append(totalsms)
   
    print(classRNs)
    union=[]
    union_helper=[union.append(em) for em in ems if em not in union]
    #propabilities
    for j in range(len(classv)):
        for i in range(len(part_cols)):
            for k in range(len(cluster_set)):
                emv=0
                for l in range(len(part_cols[i])):
                    if part_cols[i][l][1]==cluster_set[k] and part_cols[i][l][2]==classv[j]:
                        emv+=1
                if emv!=0:
                    ems.append([headers[i+1],cluster_set[k]])
                    sems.append([classv[j],headers[i+1],cluster_set[k]])
    for i in range(len(part_cols)):
        for k in range(len(cluster_set)):
            ml_helper=[]
            for j in range(len(classv)):
                emv=0
                for l in range(len(part_cols[i])):
                    if part_cols[i][l][1]==cluster_set[k] and part_cols[i][l][2]==classv[j]:
                        emv+=1
                if emv/classRNs[j]==0:
                    ml_helper.append([headers[i+1],cluster_set[k],0.0000005])
                else:
                    #print(emv)
                    ml_helper.append([headers[i+1],cluster_set[k], emv/classRNs[j]])  
            markovList.append(ml_helper)

    markovTxt=''
    markovTxt+='States and Their Transistion Probabilities\n\nStates:\nStart\n'
    for cv in classv:
        markovTxt+=str(cv)+"\n"
    markovTxt+='State Transistion Probabilities:\n'
    for i in range(2):       #start -> class
        for j in range(len(classv)):
            markovTxt+='P( '+str(markovList[i][j][1])+' | '+str(markovList[i][j][0])+") = "+str(markovList[i][j][2])+"\n"
           
    markovTxt+='\nState Emissions:\n'
    for i in range(len(sems)):
        markovTxt+=str(sems[i])+"\n"
        
    markovTxt+='\nState Emissions Probabilities:\n'
    print(markovList)
    for i in range(2,len(markovList)):
        for j in range(len(classv)):
            markovTxt+="P( "+str(markovList[i-2][j][0])+":"+str(markovList[i-2][j][1])+" | "+str(classv[j])+" ) = "+str(markovList[i-2][j][2])+"\n"
    markovTxt+="\n\nUnion of Emissions:\n"
    for i in range(len(union)):
        markovTxt+=str(union[i])+"\n"    

    return markovTxt,markovList
def markovAttrProb(attrName,ml,attrVal=None):
    results=[]
    if attrVal!=None:
        for i in range(len(ml)):
            if (attrName in ml[i])==True and (attrVal in ml[i])==True:
                results.append(ml[i])
        return results
    else:
        for i in range(len(ml)):
            if (attrName in ml[i]):
                results.append(ml[i])
        return results
def MarkovPrediction(markovList,headers,attrv,testdata):
    classv=list(set(attrv[0]))
    predictions=[]
    paths=[]
    actual=[val[0] for val in testdata]
    for i in range(len(testdata)):
        paths_helper=[]
        for j in range(1,len(testdata[i])):
            if j==1:
                #start->1st v
                start_prob=markovList[0]
                attr_probs=markovAttrProb(headers[j],markovList,testdata[i][j])
                #print(len(attr_probs))
                #pull probs
                indv=0
                maxv=0
                for i in range(len(start_prob)):
                    if start_prob[i][2] * attr_probs[i][2] > maxv:
                        maxv=start_prob[i][2] * attr_probs[i][2]
                        indv=start_prob[i][1]
                m=maxv
                ind=classv.index(indv)
                paths_helper.append(start_prob[ind])
            else:
                #check of ind changes
                ind_probs=markovAttrProb(ind,markovList)
                attr_probs=markovAttrProb(headers[j],markovList,testdata[i][j])
                paths_helper.append(attr_probs[ind])
                attr_prob=attr_probs[ind][2]
                maxv=0
                for i in range(len(ind_probs)):
                    if m * ind_probs[i][2] > maxv:
                        maxv=m * ind_probs[i][2]*attr_prob
                        indv=ind_probs[i][1]
                m=maxv
                ind=classv.index(indv)
        predictions.append(indv)
        paths.append(paths_helper)
        
        
        correct=[]
        incorrect=[]

        for i in range(len(predictions)):
            if predictions[i]==actual[i]:
                correct.append(predictions[i])
            else:
                incorrect.append(predictions[i])

        corr_cts=[correct.count(classv[i]) for i in range(len(classv))]
        incorr_cts=[incorrect.count(classv[i]) for i in range(len(classv))]
        total_corr=len(correct)
        percent_corrPred=((corr_cts[0]+incorr_cts[0])*100)/len(testdata)
        pred_matrix=''
        pred_matrix+="Total Corect: "+str(total_corr)+" ("+str(100*(total_corr/len(testdata)))+"%)\n"
        pred_matrix+=str(classv)
        for i in range(len(predictions)):
           
            for j in range(len(classv)):
                pred_matrix+=str(classv[j])+"   "
                if j==0:
                    pred_matrix+=str(corr_cts[j])+"   "+str(incorr_cts[j])+"\n"
                else:
                    pred_matrix+=str(incorr_cts[j])+"   "+str(corr_cts[j])+"\n"

        pred_matrix+="\nPaths:\n"
        for i in range(len(paths)):
            for j in range(len(paths[i])):
                pred_matrix+=str(paths[i][j][0])+"->"
            pred_matrix+=str(predictions[i])+"\n"
    return pred_matrix
        
                