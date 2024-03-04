import PySimpleGUI as sg
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
        [sg.Button('Identify Outliers')],
        [sg.Button('Remove Outliers')] #removal popup
    ])],

    [sg.Frame('Discretization', layout=[
        [sg.Button('Calculate Median')],
        [sg.Text()],#median value
        [sg.Button('Run (Entropy-Based)')]
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
        [sg.Input()],
        [sg.Text('Enter Testing Set Filename')],
        [sg.Input()],
        [sg.Button('Run Train/Test Split')]
        [sg.Button('Download Data')]
    ])],

    [sg.Frame('Redundancies', layout=[
        [sg.Text()],#train set filename
        [sg.Text('Enter Correlation Threshold')]
        [sg.Input()],
        [sg.Button('Identify Redundancies')],
        [sg.Button('Show Correlation Matrix')],
        [sg.Button('Remove Highly Correlated Attributes')]#removal value
    ])],

    [sg.Frame('Associations', layout=[
        [sg.Text('Enter Confidence Treshold')]
        [sg.Input()],
        [sg.Button('Generate Rules')],
        [sg.Button('Show Unnamed Discrete Value Table')],
        [sg.Button('Show Named Discrete Value Table')],
        [sg.Button('Show Identified Frequent Itemsets')],
        [sg.Button('Clean Itemsets')], #removal popup
        [sg.Button('Show All Rules')],
        [sg.Text('Select Format')],
        [sg.Radio('None',0)],
        [sg.Radio('Format-1',0)],
        [sg.Radio('Format-2',0)],
        [sg.Button('Show Survived Rules')]#removal popup
    ])],

    [sg.Button('Generate Report')]
]
#Part3
"""
set dependent variable
create format 1 rules (show removal popup)
"""
p3_tab=[
    [sg.Frame('Settings',layout=[
        [sg.Text('Enter Dependent Variable')],
        [sg.Input()]
    ])],

    [sg.Frame('Predictions', layout=[
        [sg.Button('Finalize Format-1-Rules')] #rules popup
        [sg.Button('Show Format-1-Rules')]
        [sg.Button('Make Predictions')]
        [sg.Button('Show Prediction Matrix')]
    ])]

    [sg.Button('Generate Report')]
]

#The control panel (tab group)
left=[
    [sg.TabGroup([
        [sg.Tab('Part 1',p1_tab,background_color='BLUE'),sg.Tab('Part 2',p2_tab,background_color='RED'),sg.Tab('Part 3',p3_tab,background_color='YELLOW')]
    ])]
]
#anything dealing with data loading, downloading

""" 
load csv
show removed values (and itemsets, format 1 rules) + reason why removed
reset
"""
top=[
    [sg.FileBrowse('Load'),sg.Button('Show All Removed Values'), sg.Button('Reset')]
]

#all tables
"""
Original Data Table
Split data sets (train/test)
Association Rules (show named and unnamed discrete value tables,
frequent itemsets + removal items, show rules in plain english , format 1 and format 2 lists)
prediction (format 1 rules, prediction matrix, correct prediction calculation)
"""
right=[]