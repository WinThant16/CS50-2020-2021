import csv
from cs50 import get_string
from sys import argv, exit


argc = len(argv)
if argc != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)


# storing dnasequence in a string
dnatype = []

# dict to store dna sequences that match/count
countsequence = {}

# STR groups for dna

dnastrtypes = {"AGATC": 0,
               "TTTTTTCT": 0,
               "AATG": 0,
               "TCTAG": 0,
               "GATA": 0,
               "TATC": 0,
               "GAAA": 0,
               "TCTG": 0}
          

# each row corresponds to person, each column corresponds to a particular STR
# reading  dna sequence from file to a list:
with open(argv[1], 'r') as dnafile:
    database = csv.reader(dnafile)
    line = 0
    for row in database:
        
        # removing 'name' from database(and adding str types to list called dnatype)
        if line == 0:
            for col in row:
                
                if col[2].islower() and col != 'name':
                    break
                elif col == 'name':
                    continue
                else:
                    dnatype.append(col)
            line = line + 1
            
        # database is added to a dictionary, with max number of each STR as a list for each person
        else:
            r = 0
            for col in row:
                if r == 0:
                    countsequence[col] = []
                    r += 1
                else:
                    countsequence[row[0]].append(col)
                    
    
# creating variable for sequence as a string called s (using this to compare to dictionary database)
s = ""

# opening the sample sequence txt file and placing it inside string s
with open(argv[2], 'r') as sample:
    for c in sample:
        s = s + c
        

# comparing sample seq with strings in dnatype
for key in dnastrtypes:
    # max count of sequence
    maxCount = 0
    # current count sequence
    cur_count = 0
    length = len(key)
    i = 0
    # looking through samples (samples are stored in string s)
    while i < len(s):
        if s[i:(i+length)] == key:
            cur_count += 1  # counts str
            # repeat until sequence sample end is reached
            if ((i+length) < len(s)):
                i = i + length
            continue
        # when end is reached
        else:
            if cur_count > maxCount:
                maxCount = cur_count
                
            else:
                cur_count = 0
        i += 1
    dnastrtypes[key] = maxCount
    

# finding name of person
# referred to https://www.geeksforgeeks.org/python-list-index/#:~:text=index()%20is%20an%20inbuilt,index%20where%20the%20element%20appears.
# and https://docs.python.org/3/tutorial/introduction.html#lists to find functions for lists, such as index

#comparing dict and maxcount of str to see if there is a match
match = True
match_name = ''
for keys in countsequence:
    match = True
    for entry in dnatype:
        x = dnatype.index(entry)
        y = dnastrtypes.get(entry)
        yes = int(countsequence.get(keys)[x])
        if (y != yes):
            match = False
    if match == True:
        match_name = keys
        break
if match_name != '':
    print(match_name)
else:
    print("No match")