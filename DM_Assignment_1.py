import csv
import util
def identifyOutliers(dataTable:util.DataTable):#identify outliers and Highlight rows to be romoved on figure
    attributeValues=dataTable.currentAttributeValues
    std_devs=[]
    #for each attribute
    for col in range(len(attributeValues)):
        #calculate standard deviiation 
        std_dev=util.std_dev(attributeValues[col])
        std_devs.append(std_dev)
    outliers=[]
    #determine outliers
    for col in range(len(attributeValues)):
        for val in range(len(attributeValues[col])):
            if attributeValues[col][val] > std_devs[col]*2 or attributeValues[col][val] < -std_devs[col]*2:
                #add to outliers list
                outliers.append([col,val])
    dataTable.outliers=outliers
    #highlight outlighters on figure (hightlight outliers and their attributes)
    