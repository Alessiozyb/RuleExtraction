"""
constains all the methods to process the original dataset, usage:
python <filename>
"""
import sys
import csv

OUT_FILE_NAME = "INTEGRATED-DATASET.csv"

def transformCSV(filename1, filename2):
    """
    transform the csv file into our integrated dataset
    :param filename1: a string of input file name
    :param filename2: a string of output file name
    """
    try:
        inFile = file(filename1, "rb")
        outFile = file(filename2, "wb")
    except IOError:
        print "Can not open file %s or %s" % (filename1, filename2)
        sys.exit(1)
    data = []
    reader = csv.reader(inFile, delimiter = ',')
    for row in reader:
        data.append(row)
    inFile.close()
    # modify the original data
    removeAttr(data, 'Job ID')
    removeAttr(data, 'Work Location 1')
    removeAttr(data, 'Recruitment Contact')
    removeAttr(data, 'Post Until')
    removeAttr(data, 'Posting Updated')
    removeAttr(data, 'Process Date')
    removeAttr(data, 'Title Code No')
    removeAttr(data, 'Work Location')
    removeAttr(data, '# Of Positions')
    removeAttr(data, 'Salary Range To')
    removeAttr(data, 'Job Description')
    removeAttr(data, 'Minimum Qual Requirements')
    removeAttr(data, 'Preferred Skills')
    removeAttr(data, 'To Apply')
    removeAttr(data, 'Additional Information')
    removeAttr(data, 'Hours/Shift')
    #removeAttr(data, 'Posting Type')
    removeAttr(data, 'Salary Frequency')
    removeAttr(data, 'Residency Requirement')
    removeAttr(data, 'Posting Date')

    #formatDate(data, 'Posting Date')
    formateSalary(data, 'Salary Range From')

    print data[0]
    writer = csv.writer(outFile)
    for row in data[1:]:
        writer.writerow(row)

    outFile.close()

def formatDate(data, attr):
    """
    For data of datetime, retain only the information of year
    :param data: a list of all the transactions
    :param attr: a string of the name of the attribution
    """
    try:
        index = data[0].index(attr)
        for row in data[1:]:
            date = row[index].split('/')
            if(len(date) >= 3):
                newDate = date[2][0:4]
                row[index] = newDate
    except ValueError:
        print "The attribute doesn't exist."

def formateSalary(data, attr):
    """
    For salary attribution, divide it into two categories, i.e. above 50k or below 50k
    :param data: a list of all the transactions
    :param attr: a string of the name of the attribution
    """
    try:
        index = data[0].index(attr)
        for row in data[1:]:
            salary = int(row[index])
            if salary > 50000:
                salary = "Above 50K"
            else:
                salary = "Below 50K"
            row[index] = salary
    except ValueError:
        print "The attribute doesn't exist."

def removeAttr(data, attr):
    """
    remove the specific attribute from the data
    :param data: a list of all the transactions
    :param attr: a string of the name of the attribution
    """
    try:
        index = data[0].index(attr)
        for row in data:
            row.pop(index)
    except ValueError:
        print "The attribute doesn't exist."


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Please enter enough arguments"
        sys.exit(2)

    transformCSV(sys.argv[1], OUT_FILE_NAME)