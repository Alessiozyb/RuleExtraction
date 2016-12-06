"""
entry of the program, usage:
python main.py <INTEGRATED-DATASET.csv> <minSupp> <minConf>
"""
from apriori import *
import csv
import sys

#IN_FILE_NAME = "INTEGRATED-DATASET.csv"
OUT_FILE_NAME = 'output.txt'

def main():
    # read arguments
    if len(sys.argv) != 4:
        print "Please enter enough arguments"
        sys.exit(2)
    try:
        inFile = file(sys.argv[1], "rb")
    except IOError:
        print "Can not open file %s " % sys.argv[1]
        sys.exit(1)
    minSupp = float(sys.argv[2])
    minConf = float(sys.argv[3])
    # get the list of all the transactions and items
    reader = csv.reader(inFile, delimiter=',')
    transactionList = []
    itemList = []
    for row in reader:
        transactionList.append(row)
        for item in row:
            itemList.append(item)
    # extract the association rules by a-priori algorithm
    items, rules = extractRules(transactionList, itemList, minSupp, minConf)
    # write the result to the file
    writeFile(items, rules, minSupp, minConf, OUT_FILE_NAME)

if __name__=="__main__":
    main()