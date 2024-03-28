import PySimpleGUI as sg
import DM_Assignment_1 as dm
import util

sg.theme('BrightColors')

#tab menues
#Part1
"""
Identify Outliers
Remove Outliers (show removal pop up)
Entropy Based Discretization
Threshold Selector (median vs value)
"""
p1_tab=[
    [sg.Frame('Outliers', layout=[
        [sg.Button('Identify Outliers',key='p1B0')],
        [sg.Button('Remove Outliers',key='p1B1')] #removal popup
    ])],

    [sg.Frame('Redundancies', layout=[
        [sg.Text('Enter Correlation Threshold')],
        [sg.Input(key='p2I2')],
        [sg.Button('Identify Redundant Attributes',key='p2B2')],
        [sg.Button('Show Correlation Matrix',key='p2B3')],
        [sg.Button('Remove Highly Correlated Attributes',key='p2B4')]#removal value
    ])],

    [sg.Frame('Discretization', layout=[
        [sg.Button('Run (Entropy-Based)',key='p1B3')],
        [sg.Button('Remove Duplicate Data',key='p1B2')],
        [sg.Button('Show Unnamed Discrete Value Table',key='p2B6')],
        [sg.Button('Show Named Discrete Value Table',key='p2B7')]
    ])]
]
#Part2

"""
Split file (split canvas view)
Identify reduncancies (show correlation matrix)
threshold selector (value slider)
Remove higly corelated vales (show removal pop up)
generate Association Rules: show named and unnamed discrete value tables,
frequent itemsets, show removed itemsets, show rules in plain english, 
format 1 and format 2 lists
"""
p2_tab=[
    [sg.Frame('Data Split', layout=[
        [sg.Text('Enter Training Set Filename')],
        [sg.Input('Econ-TRAIN.csv',key='p2I0')],
        [sg.Text('Enter Testing Set Filename')],
        [sg.Input('Econ-TEST.csv',key='p2I1')],
        [sg.Button('Run Train/Test Split',key='p2B0')],
        [sg.Button('Download Data',key='p2B1')]
    ])],



    [sg.Frame('Associations', layout=[
        [sg.Button('Show Identified Frequent Itemsets',key='p2B8')],
        [sg.Button('Clean Itemsets',key='p2B9')], #removal popup
        [sg.Text('Enter Confidence Treshold')],
        [sg.Input(key='p2I3')],
        [sg.Button('Generate Rules',key='p2B5')],
        [sg.Button('Show All Rules',key='p2B10')],
        [sg.Text('Select Format')],
        [sg.Radio('None',0,key='p2R0')],
        [sg.Radio('Format-1',0,key='p2R1')],
        [sg.Radio('Format-2',0,key='p2R2')],
        [sg.Button('Show Survived Rules',key='p2B11')]#removal popup
    ])]

]
#Part3
"""
set dependent variable
create format 1 rules (show removal popup)
"""
p3_tab=[
    [sg.Frame('Settings',layout=[
        [sg.Text('Enter Dependent Variable')],
        [sg.Input(key='p3I0')]
    ])],

    [sg.Frame('Predictions', layout=[
        [sg.Button('Make Predictions',key='p3B2')]
    ])]


]

#The control panel (tab group)
left=[
    [sg.TabGroup([
        [sg.Tab('Part 1',p1_tab,background_color='CYAN'),sg.Tab('Part 2',p2_tab,background_color='tomato'),sg.Tab('Part 3',p3_tab,background_color='YELLOW')]
    ])]
]
#anything dealing with data loading, downloading

""" 
load csv
show removed values (and itemsets, format 1 rules) + reason why removed
reset
"""
top=[
    [sg.Input(key='tI0', visible=False, enable_events=True),sg.FileBrowse('Load',key='tB0',target='tI0'),sg.Button('Run All',key='rA')]
]

#all tables
"""
Original Data Table
Split data sets (train/test)
Association Rules (show named and unnamed discrete value tables,
frequent itemsets + removal items, show rules in plain english , format 1 and format 2 lists)
prediction (format 1 rules, prediction matrix, correct prediction calculation)
"""
right=[
   
   
    [sg.Col([[sg.Input(visible=False),sg.Input(visible=False)]], key='tds0')]

]

#window
layout=[
    [top],
    [sg.Column(left,justification='left'),sg.Column(right, element_justification='center',justification='right')]
]
window=sg.Window('Datamining Assignment', layout)

#logic
while True:  # Event Loop

    event, values = window.read()
    #print(event, values)

    if event == sg.WIN_CLOSED or event in ('Close', None):
        break
    elif event == 'rA':
        while True:
            try:
                # identify outliers
                dm.identifyOutliers(dataTable)
                # highlight outlier cells
                out_records = dataTable.outliers
                aff_rows = []
                for i in range(len(dataTable.outliers)):
                    aff_rows.append(dataTable.outliers[i][1])
                aff_rows = list(set(aff_rows))
                dataTable.outlierRecords = aff_rows
                rc = []
                for row in aff_rows:
                    rc.append((row, 'Cyan'))
                window['OG_Table'].update(row_colors=rc)
            except Exception:
                continue
            break

        while True:
            try:
                # remove outliers
                dataTable.dataNoOutliers = [dataTable.OriginalRecords[i] for i in range(len(dataTable.OriginalRecords)) if
                                            i not in dataTable.outlierRecords]
                dataTable.currentAttributeValues = util.record_to_values(dataTable.dataNoOutliers)
                # create outlier table
                # switch scene to data w/o outlier table
                window['OG_Table'].update(values=dataTable.dataNoOutliers)
                # pop out outlier removal report
                util.generate_Outlier_Report(dataTable)
                sg.popup_scrolled(dataTable.outlierRemovalReport, title="Outlier Removal Report", size=(100, 125))
            except Exception:
                continue
            break

        while True:
            try:
                # discretized values
                dataTable.currentAttributeValues, dataTable.discretizedRecords = dm.entropy_discretization(dataTable.currentAttributeValues, dataTable)
                # update table
                window['OG_Table'].update(values=dataTable.discretizedRecords)
            except Exception as e:
                print(e.with_traceback())
                continue
            break

        while True:
            try:
                # remove dupes
                dataTable.discretizedNoDups = []
                dontadd = ['n/a']
                for i in range(len(dataTable.discretizedRecords)):
                    if dataTable.discretizedRecords[i] not in dontadd:
                        if dataTable.discretizedRecords.count(dataTable.discretizedRecords[i]) == 1:
                            dataTable.discretizedNoDups.append(dataTable.discretizedRecords[i])
                        else:
                            dataTable.discretizedNoDups.append(dataTable.discretizedRecords[i])
                            dontadd.append(dataTable.discretizedRecords[i])

                dataTable.dupedRecords = dontadd[1:]
                dataTable.currentAttributeValues = util.record_to_values(dataTable.discretizedNoDups)
                window['OG_Table'].update(values=dataTable.discretizedNoDups)
                util.generate_Discretization_Report(dataTable)
                sg.popup_scrolled(dataTable.discretizationText, title="Discretization Duplicate Removal Report",
                                  size=(100, 125))
            except Exception:
                continue
            break

        while True:
            try:
                # train/test Split
                dataTable.trainData, dataTable.testData = dm.TTSplit(dataTable.discretizedRecords, 0.10)
                dataTable.currentAttributeValues = util.record_to_values(dataTable.trainData)
                window['OG_Table'].update(values=dataTable.trainData)
            except Exception:
                continue
            break

        correlation=sg.popup_get_text('Enter Correlation Threshold')
        if correlation!="":
            while True:
                try:
                    #identify redundancies
                    dataTable.CorelationMatrix, dataTable.redundantAttr = dm.IdentifyRedundancies(
                        dataTable.currentAttributeValues[1:], float(correlation))
                    sg.popup_scrolled(util.generate_Corelation_Matrix_Report(dataTable, float(correlation)),
                                      title='Correlation Matrix Report', size=(100, 300))
                except Exception:
                    continue
                break
        else:
            break

        while True:
            try:
                #remove redundancies
                rmv = dm.removeRedundancies(dataTable.redundantAttr, len(dataTable.columnHeaders) - 1)
                nonRedundantVal = [dataTable.currentAttributeValues[i] for i in range(len(dataTable.currentAttributeValues)) if
                                   i not in rmv]
                nonRedundantrecords = [dataTable.trainData[i] for i in range(len(dataTable.trainData))]
                print(rmv)
                for j in nonRedundantrecords:
                    for i in rmv:
                        j.pop(i)
                new_headers = dataTable.columnHeaders
                for i in rmv:
                    del new_headers[i]
                # print(nonRedundantrecords)
                dataTable.currentAttributeValues = nonRedundantVal
            except Exception:
                continue
            break

        while True:
            try:
                # show frq itemsets
                Fits = dm.Apriori(dataTable.namedDisTbl, nonRedundantrecords, new_headers)
                sg.popup_scrolled(dm.generateItemset(Fits), title='Frequent Itemset', size=(100, 300))
            except Exception:
                continue
            break

        while True:
            try:
                #clean set
                cleanSet, txt = dm.cleanFreqItemSet(Fits, nonRedundantrecords)

                # clean itemsets
                sg.popup_scrolled(txt, title='Cleaned Frequent Itemset', size=(100, 300))
            except Exception:
                continue
            break

        confidence=sg.popup_get_text('Enter Confidence Threshold')
        if confidence != "":
            while True:
                try:
                    # generate rules
                    r, sr, t = dm.GenerateAssociationRules(cleanSet, float(confidence), dataTable.namedDisTbl,
                                                           nonRedundantrecords, new_headers)
                except Exception:
                    continue
                break
        else:
            break
        # show rules
        sg.popup_scrolled(t, title='All Rules', size=(100, 300))

        format=sg.popup_get_text('Enter Format (None, Format-1, Format-2)')
        if format != "":
            while True:
                try:
                    # show survived rules
                    srwftxt = dm.generateSurvRules(sr, dataTable.namedDisTbl, format, confidence, nonRedundantrecords)
                    sg.popup_scrolled(srwftxt, title='Survived Rules ' + str(format), size=(100, 300))
                except Exception:
                    continue
                break
        else:
            break


        name=sg.popup_get_text('Enter Name of Dependent Variable ')
        if name != "":
            while True:
                try:
                    #prediction
                    predtxt = dm.predict(sr, name, dataTable.testData, dataTable.namedDisTbl, dataTable.columnHeaders)
                    sg.popup_scrolled(predtxt, title='prediction ', size=(100, 300))
                except Exception:
                    continue
                break
        else:
            break

    elif event=='tI0':
        #create data object
        originalData=util.Generate_Table_From_CSV(values['tB0'])
        dataTable=util.DataTable(originalData)
        #load figure into original data
        window.extend_layout(window['tds0'],[[dataTable.OriginalTable]])
    elif event=='p1B0':
        #identify outliers
        dm.identifyOutliers(dataTable)
        #highlight outlier cells
        out_records= dataTable.outliers
        aff_rows=[]
        for i in range(len(dataTable.outliers)):
            aff_rows.append(dataTable.outliers[i][1])
        aff_rows=list(set(aff_rows))
        dataTable.outlierRecords=aff_rows
        rc=[]
        for row in aff_rows:
            rc.append((row,'Cyan'))
        window['OG_Table'].update(row_colors=rc)
    elif event=='p1B1':
        #remove outliers
        dataTable.dataNoOutliers=[dataTable.OriginalRecords[i] for i in range(len(dataTable.OriginalRecords)) if i not in dataTable.outlierRecords ]
        dataTable.currentAttributeValues=util.record_to_values(dataTable.dataNoOutliers)
        #create outlier table
        #switch scene to data w/o outlier table
        window['OG_Table'].update(values=dataTable.dataNoOutliers)
        #pop out outlier removal report
        util.generate_Outlier_Report(dataTable)
        sg.popup_scrolled(dataTable.outlierRemovalReport,title="Outlier Removal Report",size=(100,125))
    elif event=='p1B2':
        #remove dupes
        dataTable.discretizedNoDups=[]
        dontadd=['n/a']
        for i in range(len(dataTable.discretizedRecords)):
            if dataTable.discretizedRecords[i] not in dontadd:
                if dataTable.discretizedRecords.count(dataTable.discretizedRecords[i])==1:
                    dataTable.discretizedNoDups.append(dataTable.discretizedRecords[i])
                else:
                    dataTable.discretizedNoDups.append(dataTable.discretizedRecords[i])
                    dontadd.append(dataTable.discretizedRecords[i])

        dataTable.dupedRecords=dontadd[1:]
        dataTable.currentAttributeValues=util.record_to_values(dataTable.discretizedNoDups)
        dataTable.currentRecords=dataTable.discretizedNoDups
        display_Records = util.display_Records(dataTable, rmv)
        window['OG_Table'].update(values=display_Records)
        util.generate_Discretization_Report(dataTable)
        sg.popup_scrolled(dataTable.discretizationText,title="Discretization Duplicate Removal Report",size=(100,125))
    elif event=='p1B3':
        #discretized values
        dataTable.currentAttributeValues,dataTable.discretizedRecords=dm.entropy_discretization(dataTable.currentAttributeValues,dataTable)
        #update table
        dataTable.currentRecords=dataTable.discretizedRecords
        display_Records = util.display_Records(dataTable, rmv)
        window['OG_Table'].update(values=display_Records)
    elif event=='p2B0':
        #train/test Split
       dataTable.trainData,dataTable.testData=dm.TTSplit(dataTable.currentRecords,0.10)
       dataTable.currentAttributeValues=util.record_to_values(dataTable.trainData)
       display_Records=util.display_Records(dataTable,rmv)
       window['OG_Table'].update(display_Records)
    elif event=='p2B1':
       util.DownloadData(dataTable.trainData,dataTable.columnHeaders,values['p2I0'])     
       util.DownloadData(dataTable.testData,dataTable.columnHeaders,values['p2I1'])  
    elif event=='p2B2':
        dataTable.CorelationMatrix,dataTable.redundantAttr=dm.IdentifyRedundancies(dataTable.currentAttributeValues[1:],float(values['p2I2']))
        cm=util.generate_Corelation_Matrix_Report(dataTable,float(values['p2I2']))
        sg.popup_scrolled(cm, title='Correlation Matrix Report',size=(100,300))
    elif event=='p2B3':
        sg.popup_scrolled(cm, title='Correlation Matrix Report',size=(100,300))
    elif event=='p2B4':
        rmv=dm.removeRedundancies(dataTable.redundantAttr)
        if rmv !=None:
            nonRedundantVal=[dataTable.currentAttributeValues[i] for i in range(len(dataTable.currentAttributeValues)) if i not in rmv]
            nonRedundantrecords=util.values_to_records(nonRedundantVal)
            new_headers=dataTable.columnHeaders.copy()
            new_headers=[new_headers[i] for i in range(len(new_headers)) if i not in rmv]
            dataTable.currentHeaders=new_headers
            print(new_headers)
            #print(nonRedundantrecords)
            dataTable.currentAttributeValues=nonRedundantVal
            dataTable.currentRecords=nonRedundantrecords
            display_Records = util.display_Records(dataTable, rmv)
            window['OG_Table'].Widget.configure(displaycolumns=new_headers)
            window['OG_Table'].update(values=display_Records)
        #sg.popup_scrolled(util.textTable(nonRedundantrecords,new_headers),title='Data Table',size=(100,100))
    elif event=='p2B6':
        sg.popup_scrolled(dm.generateUnNamedTable(dataTable),title='Unnamed Discrete Value Table',size=(100,300))
    elif event=='p2B7':
        sg.popup_scrolled(dm.generateNamedTable(dataTable),title='Named Discrete Value Table',size=(100,300))
    elif event=='p2B5':
        r, sr, t=dm.GenerateAssociationRules(cleanSet,float(values['p2I3']),dataTable.namedDisTbl,nonRedundantrecords,new_headers)
        #generate rules
    elif event=='p2B8':
        #show frq itemsets
        Fits=dm.Apriori(dataTable.namedDisTbl,dataTable.currentRecords,dataTable.currentHeaders)
        sg.popup_scrolled(dm.generateItemset(Fits),title='Frequent Itemset',size=(100,300))
    elif event=='p2B9':
        cleanSet,txt=dm.cleanFreqItemSet(Fits,nonRedundantrecords)
        #clean itemsets
        sg.popup_scrolled(txt,title='Cleaned Frequent Itemset',size=(100,300))
    elif event=='p2B10':
        #show rules
        sg.popup_scrolled(t,title='All Rules',size=(100,300))
    elif event=='p2B11':
        #show survived rules
        if values['p2R0']==True:
            format='None'
        elif values['p2R1']==True:
            format='Format-1'
        elif values['p2R2']==True:
            format='Format-2'
        srwftxt=dm.generateSurvRules(sr,dataTable.namedDisTbl,format,values['p2I3'],nonRedundantrecords)
        sg.popup_scrolled(srwftxt,title='Survived Rules '+str(format),size=(100,300))
    elif event=='p3B2':
        predtxt=dm.predict(sr,values['p3I0'],dataTable.testData,dataTable.namedDisTbl,dataTable.columnHeaders)
        sg.popup_scrolled(predtxt, title='prediction ', size=(100, 300))
    
        
        

window.close()