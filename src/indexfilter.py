# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:37:58 2017

@author: Tim G
"""

"""
Second filter step: Filter results from the aggregated list
"""

from matplotlib import pyplot as plt
from nltk.corpus import treebank
import analyze_coverage
from pipeline import glossary_extraction
import pickle

no_comp_reqs=5000 # number of sentences from TreeBank to use for comparison

def create_filter_index():
        sents = [" ".join(sent) for sent in treebank.sents()[:no_comp_reqs]]
        ids = list(range(no_comp_reqs))
        tags = ["" for sent in sents]
        filter_index,_,_,_ = glossary_extraction(sents, ids, tags, tag_mode="load tagger", filter_mode="threshold", threshold_coverage=1)
        with open('../temp/filter_index.pickle','wb') as f:
            pickle.dump(filter_index,f)

def index_filter(index,no_reqs,threshold_coverage=5,filter_mode=["threshold"],times=1):
    if "threshold" in filter_mode:
        filtered_keys = []
        if ('I',) in index:
            filtered_keys.append(('I',)) # needs to be removed due to the user story schema used ('As a ... I want ...')
        for key in index:
            if len(key)==0:
                filtered_keys.append(key)
            if len(index[key])<threshold_coverage:
                filtered_keys.append(key)            
        for key in filtered_keys:
            index.pop(key)
    if "specificity" in filter_mode:
        filtered_keys = []
        print(filtered_keys)
        with open('../temp/filter_index.pickle','rb') as f:
            filter_index = pickle.load(f)
        global comparison_index
        comparison_index = {}
        for key in index:
            if key in filter_index:
                if len(index[key])/no_reqs<times*(len(filter_index[key])/no_comp_reqs):
                    filtered_keys = filtered_keys + [key]
                comparison_index[key] = [len(index[key])/no_reqs,len(filter_index[key])/no_comp_reqs]
            else:
                comparison_index[key] = [len(index[key])/no_reqs,0.0]
        for key in filtered_keys:
            index.pop(key)
    return index

def analyze_index_filter(index,reqs,ids,description="Analysis of index filter",covered_range=11,output='memory',filenames=['../target/number_of_glossary_terms_by_filter_threshold.pdf','../target/coverage_by_filter_threshold.pdf','../target/double_coverage_by_filter_threshold.pdf']):
    print()
    print(description)
    index_copy = index.copy()
    number = []
    coverage = []
    double_coverage = []
    for i in range(1,covered_range):
        index_copy=index_filter(index_copy,len(index_copy),threshold_coverage=i)
        number = number + [len(index_copy.keys())]
        cover, _ = analyze_coverage.analyze_coverage(index_copy,reqs,ids)
        coverage = coverage + [cover]
        cover, _ = analyze_coverage.analyze_coverage(index_copy,reqs,ids,threshold=2)
        double_coverage = double_coverage + [cover]        
    print("Size of glossary term set for coverage thresholds from 1 to 10")
    print(number)
    print(coverage)
    print(double_coverage)
    plt.title(description)
    plt.xlabel('threshold number of requirements covered\n by a glossary term to be included')
    plt.ylabel('number of glossary terms')
    plt.bar(range(1,covered_range),number)
    if output=='file':
        plt.savefig(filenames[0],format='pdf')
    else:
        plt.show()
    plt.close()
    plt.title(description)
    plt.xlabel('threshold number of requirements covered by a glossary term to be included')
    plt.ylabel('percentage of requirements covered\n by at least one glossary term')
    plt.bar(range(1,covered_range),coverage)
    if output=='file':
        plt.savefig(filenames[1],format='pdf')
    else:
        plt.show()
    plt.close()
    plt.title(description)
    plt.xlabel('threshold number of requirements covered by a glossary term to be included')
    plt.ylabel('percentage of requirements covered\n by at least two glossary terms')
    plt.bar(range(1,covered_range),double_coverage)
    if output=='file':
        plt.savefig(filenames[2],format='pdf')
    else:
        plt.show()
