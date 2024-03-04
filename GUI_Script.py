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
        [sg.Button('Remove Outliers')]
    ])],

    [sg.Frame('Discretization', layout=[
        [sg.Button('Calculate Median')],
        [sg.Text()],
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
        [sg.Input('Training Set Filename')],
        [sg.Input('Training Set Filename')],
        [sg.Button('Run Train/Test Split')]
        [sg.Button('Download Data')]
    ])],

    [sg.Frame('Redundancies', layout=[
        [sg.Text()],
        [sg.Input('Enter Correlation Threshold')],
        [sg.Button('Identify Redundancies')],
        [sg.Button('Show Correlation Matrix')],
        [sg.Button('Remove Highly Correlated Attributes')]
    ])],

    [sg.Frame('Associations', layout=[
        [sg.Button('Generate R')]
    ])]
]
#Part3

"""
set dependent variable
create format 1 rules (show removal popup)
"""
p3_tab=[]

#The control panel (tab group)
left=[]
#anything dealing with data loading, downloading

""" 
load csv
down load csv
show removed values (and itemsets, format 1 rules) + reason why removed
reset
"""
top=[]

#all tables
"""
Original Data Table
Split data sets (train/test)
Association Rules (show named and unnamed discrete value tables,
frequent itemsets + removal items, show rules in plain english , format 1 and format 2 lists)
prediction (format 1 rules, prediction matrix, correct prediction calculation)
"""
right=[]