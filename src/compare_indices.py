# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:29:47 2017

@author: Tim G
"""

import analyze_coverage
from matplotlib import pyplot as plt

def agreement_of_terms(index1,index2):
    global unique1
    unique1 = []
    global unique2
    unique2 = []
    total = 0
    agreed = 0
    for term in index1:
        total = total + 1
        if term in index2:
            agreed = agreed + 1
        else:
            unique1 = unique1 + [term]
    for term in index2:
        if term not in index1:
            total = total + 1
            unique2 = unique2 + [term]
    return agreed/total

def analyze_index(index,reqs,ids,description="Index analysis"):
    print()
    print(description)
    print("Size: ",len(index.keys()))
    coverage=list(range(5))
    for i in range(5):
        coverage[i],_ = analyze_coverage.analyze_coverage(index,reqs,ids,threshold=i+1) 
        coverage[i] = coverage[i]*100
        print("Percentage of requirements covered by at least "+str(i+1)+" glossary term(s): ",coverage[i])
    plt.clf()
    plt.bar(range(1,6),coverage)
    plt.xlabel('Number of glossary terms')
    plt.ylabel('Percentage of requirements covered')
    plt.title('Requirements coverage by at least a given number of glossary terms')
    plt.savefig("../target/coverage_by_number_of_glossary_terms.pdf",format="pdf")

def compare_indices(index1,index2,description="Difference between index 1 and 2"):
    print()
    print(description)
    print("Size of first index: ",len(index1.keys()))
    print("Size of second index: ",len(index2.keys()))
    print("Size change from first to second: ",(len(index2.keys())-len(index1.keys()))/len(index1.keys()))    
    print("Agreement:", agreement_of_terms(index1,index2))
    return unique1, unique2
