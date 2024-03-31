import DM_Assignment_1 as dm
import util
def Apriori(namedTable, records, headers,threshold=2):
    itemset=dm.getItemset(namedTable)
    records=dm.ConvertRecord_to_itemsets(namedTable,records,headers)
    flat_records=[record[i] for record in records for i in range(len(record))]
    c1=itemset
    L1=[([c1[i]],flat_records.count(c1[i])) for i in range(len(c1)) if flat_records.count(c1[i])>threshold or flat_records.count(c1[i])==threshold]
    Lset=[]
    Lset.append(L1)
    while len(Lset[-1])>0:
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
