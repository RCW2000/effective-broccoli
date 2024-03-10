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

    [sg.Frame('Discretization', layout=[
        [sg.Button('Calculate Median',key='p1B2'),sg.Text(key='p1T0')],#median value
        [sg.Text('Enter Threshold Value')],
        [sg.Input(key='p1I0')],
        [sg.Button('Run (Entropy-Based)',key='p1B3')],
        [sg.Button('Show Discretized Data',key='p1B4')]#popup
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
        [sg.Input(key='p2I0')],
        [sg.Text('Enter Testing Set Filename')],
        [sg.Input(key='p2I1')],
        [sg.Button('Run Train/Test Split',key='p2B0')],
        [sg.Button('Download Data',key='p2B1')]
    ])],

    [sg.Frame('Redundancies', layout=[
        [sg.Text(key='p2T0')],#train set filename
        [sg.Text('Enter Correlation Threshold')],
        [sg.Input(key='p2I2')],
        [sg.Button('Identify Redundancies',key='p2B2')],
        [sg.Button('Show Correlation Matrix',key='p2B3')],
        [sg.Button('Remove Highly Correlated Attributes',key='p2B4')]#removal value
    ])],

    [sg.Frame('Associations', layout=[
        [sg.Text('Enter Confidence Treshold')],
        [sg.Input(key='p2I3')],
        [sg.Button('Generate Rules',key='p2B5')],
        [sg.Button('Show Unnamed Discrete Value Table',key='p2B6')],
        [sg.Button('Show Named Discrete Value Table',key='p2B7')],
        [sg.Button('Show Identified Frequent Itemsets',key='p2B8')],
        [sg.Button('Clean Itemsets',key='p2B9')], #removal popup
        [sg.Button('Show All Rules',key='p2B10')],
        [sg.Text('Select Format')],
        [sg.Radio('None',0,key='p2R0')],
        [sg.Radio('Format-1',0,key='p2R1')],
        [sg.Radio('Format-2',0,key='p2R2')],
        [sg.Button('Show Survived Rules',key='p2B11')]#removal popup
    ])],

    [sg.Button('Generate Report',key='p2B12')]
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
        [sg.Button('Finalize Format-1-Rules',key='p3B0')], #rules popup
        [sg.Button('Show Format-1-Rules',key='p3B1')],
        [sg.Button('Make Predictions',key='p3B2')],
        [sg.Button('Show Prediction Matrix',key='p3B3')]
    ])],

    [sg.Button('Generate Report',key='p3B4')]
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
    [sg.Input(key='tI0', visible=False, enable_events=True),sg.FileBrowse('Load',key='tB0',target='tI0'),sg.Button('Show All Removed Values',key='tB1'), sg.Button('Reset',key='tB2')]
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
   
   
    [sg.Col([[sg.Input(visible=False),sg.Input(visible=False)]], key='tds0')],
    [sg.Frame('Reports',
        [
        [sg.Button('Original Data',key='rB0'), sg.Button('Data w/o outliers',key='rB1'), sg.Button('Discretized Data',key='rB2')],
        [sg.Button('Training Set',key='rB3'),sg.Button('Testing Set',key='rB4')],
        [sg.Button('Association Report',key='rB5'), sg.Button('Prediction Report',key='rB6')]
        ],size=(375,120),element_justification='CENTER')
    ]
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
        dataTable.currentAttributeValues=dataTable.dataNoOutliers
        #create outlier table
        #switch scene to data w/o outlier table
        window['OG_Table'].update(values=dataTable.dataNoOutliers)
        #pop out outlier removal report
        util.generate_Outlier_Report(dataTable)
        sg.popup_scrolled(dataTable.outlierRemovalReport,title="Outlier Removal Report",size=(100,125))
    elif event=='p1B2':
        #calculate Median
        medians=[]
        for col in dataTable.currentAttributeValues:
            medians.append(util.median(col))
        print(medians)
        
        window['p1T0'].update(values=(str(medians)))
window.close()