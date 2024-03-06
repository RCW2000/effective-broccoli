import csv
import util
def identifyOutliers(dataTable:util.DataTable):#identify outliers and Highlight rows to be romoved on figure
    attributeValues=dataTable.currentAttributeValues
    print(attributeValues[3])
    std_devs=[]
    #for each attribute
    for col in range(len(attributeValues)):
        #calculate standard deviiation 
        std_dev=util.std_dev(attributeValues[col])
        std_devs.append(std_dev)
    outliers=[]
    print(std_devs[3])
    #determine outliers
    for i in range(1,len(attributeValues)):
        #print(len(attributeValues))
        for j in range(len(attributeValues[i])):
            #print(len(attributeValues[col]))
            if attributeValues[i][j] > std_devs[i]*2 or attributeValues[i][j]< -std_devs[i]*2:
                #print(attributeValues[i][j])
                #print(std_devs[i]*2)
                #add to outliers list
                outliers.append([i,j])
    dataTable.outliers=outliers
    print(outliers)
    
