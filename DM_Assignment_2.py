import util
import DM_Assignment_1 as dm
#k means clustering
def k_meansSeeds(partition_col):
    small_seed=min(partition_col[1])
    med_seed=(util.median(partition_col[1]))
    large_seed=max(partition_col[1])
    return[small_seed,med_seed,large_seed]

def clustering(part_col,k):
    seeds=k_meansSeeds(part_col)
    init_seeds=seeds
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