"""
constains all the methods of the a-priori algorithm
"""
import collections
import itertools
import sys

def extractRules(transactionList, itemList, minSupp, minConf):
    """
    extract frequent itemsets and association rules from the transactionList and itemList
    :param transactionList: a list of "market basket" including all the transactions
    :param itemList: a list including all the items
    :param minSupp: the threshold of support
    :param minConf: the threshold of confidence
    :return: a dictionary of itemsets with high support and a dictionary of rules with high-confidence
    """
    # call the a-priori algorithm to get the final itemsets with high support
    itemsets, itemCounter = apriori(transactionList, itemList, minSupp)
    # get the frequent itemsets
    freqItems = []
    for key, value in itemsets.items():
        for item in value:
            support = float(itemCounter[item])/len(transactionList)
            freqItems.extend([(list(item), support)])
    # get all the association rules
    rules = []
    for key, value in itemsets.items():
        for item in value:
            support = float(itemCounter[item])/len(transactionList)
            item = list(item)
            for v in item:
                temp = item[:]
                if len(temp) > 1:
                    temp.remove(v)
                    # ensure exactly one item on the right side
                    lhs = temp
                    rhs = v
                    confidence = support/(float(itemCounter[tuple(lhs)])/len(transactionList))
                    if (confidence >= minConf):
                        rules.append(((lhs, [rhs]),confidence, support))
    return freqItems, rules


def apriori(transactionList, itemList, minSupp):
    """
    implementation of a-priori algorithm
    :param transactionList: a list of "market basket" including all the transactions
    :param itemList: a list including all the items
    :param minSupp: the threshold of support
    :return: a dictionary of itemsets with high support and a dictionary of itemsets with its count number
    """
    L1 = {}
    Lk = []
    itemsets = {}
    itemCounter = collections.defaultdict(int)
    Ck = aprioriGen(transactionList, itemList, itemCounter)
    # get the L1 itemsets
    for item, count in Ck.items():
        support = float(count)/len(transactionList)
        if support >= minSupp:
            Lk.append(item)
    TID = 0
    totNum = 0
    for transaction in transactionList:
        canidate = []
        TID = 1 + TID
        totNum = len(transaction)
        for word in transaction:
            for item in Lk:
                if word in item:
                    canidate.append(word)
                L1[TID] = canidate
    # the loop to get the kth itemsets
    k = 1
    while(k < totNum + 1):
        subsetList = []
        for key, value in L1.items():
            for subset in itertools.combinations(value, k):
                subsetList.append(subset)
        Lk = [tuple(row) for row in subsetList]
        Ck = aprioriGen(transactionList,Lk,itemCounter)
        Lk = []
        for item, count in Ck.items():
            support = float(count)/len(transactionList)
            if support >= minSupp:
                Lk.append(item)
        itemsets[k] = Lk
        k = k + 1
    return itemsets, itemCounter

def aprioriGen(transactionList, itemList, itemCounter):
    """
    this function is to generate the candidate itemsets
    :param transactionList: a list of "market basket" including all the transactions
    :param itemList: a list including all the items
    :param itemCounter: a dictionary of itemsets with its corresponding count number
    :return: a dictionary of candidate set with its count number
    """
    Ck = collections.defaultdict(int)
    for item in list(set(itemList)):
        for transaction in transactionList:
            # delete the candidates which are not in the transaction
            if (item in transaction) or isSubset(item, transaction):
                itemCounter[item] += 1
                Ck[item] += 1
    return Ck


def isSubset(Ck, transaction):
    """
    this function is to judge whether a candidate is an legible candidate
    :param Ck: a dictionary of the candidate
    :param transaction: a list of transaction
    :return: a boolean value represent the legibility of the candidate
    """
    temp = transaction[:]
    try:
        for c in Ck:
            temp.remove(c)
        return True
    except ValueError:
        return False

def writeFile(freqItems, rules, minSupp, minConf, filename):
    """
    this function is to output the frequent itemsets and association rules to a file
    :param freqItems: a dictionary of the freqItem and its support
    :param rules: a dictionary of the rules with its support and confidence
    :param minSupp: the threshold of support
    :param minConf: the threshold of confidence
    :param filename: a string of the name of the file
    """
    try:
        outFile = open(filename, 'w')
    except IOError:
        print "Can not open file %s " % filename
        sys.exit(1)
    outFile.write("\n==Frequent itemsets (min_sup = %.2f%%)\n" % (minSupp*100))
    for item, support in sorted(freqItems, key=lambda (item, support): support, reverse =True):
        outFile.write("%s , %.2f%%\n" % (str(item), support*100))
    outFile.write("\n==High-confidence association rules (min_conf= %.2f%%)\n" % (minConf*100))
    for rule, confidence, support in sorted(rules, key=lambda (rule, confidence, support): confidence, reverse =True):
        lhs, rhs = rule
        outFile.write("%s => %s (Conf: %.2f%% Supp: %.2f%%)\n" % (str(lhs), str(rhs), confidence*100, support*100))
    outFile.close()

