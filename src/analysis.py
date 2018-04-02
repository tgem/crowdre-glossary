# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:58:47 2017

@author: Tim G
"""

"""
Glossary term extraction
"""

import reader
import buildindex
import indexfilter
import analyze_coverage 
import analyze_tags
import compare_indices
from pipeline import glossary_extraction
from matplotlib import pyplot as plt

"""
Analysis
"""

# analyze frequency distribution of the number of requirements covered by a glossary term

def analyze_number_of_requirements_per_term(old_index, index):
    frequencies = {}
    for term in old_index:
        frequency = len(old_index[term])
        if frequency in frequencies:
            frequencies[frequency] += 1
        else:
            frequencies[frequency] = 1
    maxx=50
    x=list(range(maxx+1))
    y=[0]*(maxx+1)
    for frequency in frequencies.keys():
        if frequency<maxx+1:
            y[frequency]=frequencies[frequency]
    plt.title("How many requirements are covered by each glossary term")
    plt.xlabel('number of requirements covered per term candidate')
    plt.ylabel('number of glossary term candidates')
    plt.axis([0,maxx,0,50]) ## TODO
    plt.plot(x,y,linestyle="solid",color="b")
    plt.savefig("number_of_requirements_per_term.pdf",format='pdf')

# main script

# main pipeline results

index, reqs, ids, tag_index = glossary_extraction(output='file')
compare_indices.analyze_index(index,reqs,ids,description="Index resulting from main pipeline")
analyze_tags.analyze_tags(index,tag_index)
full_reqs, _= reader.reqs_read(read_tags=False)
coverage, not_covered = analyze_coverage.analyze_coverage(index,full_reqs,ids) 
print("Coverage: ",coverage)
print("Number of requirements not covered:",len(not_covered))
coverage, _ = analyze_coverage.analyze_coverage(index,full_reqs,ids,threshold=2) 
print("Coverage by two: ",coverage) 

# comparisons with alternative pipeline setups

index1,_,_,_ = glossary_extraction(threshold_coverage=5)
index2,reqs2,ids2,_ = glossary_extraction(threshold_coverage=0)
compare_indices.compare_indices(index1,index2,description="Removed threshold for minimum number of covered requirements")
indexfilter.analyze_index_filter(index2,reqs2,ids2,output='file')

index1,_,_,_ = glossary_extraction(lemmatize_mode='lemmatize')
index2,_,_,_ = glossary_extraction(lemmatize_mode='none')
compare_indices.compare_indices(index1,index2,description="Replaced lemmatization with no root reduction")

index3,_,_,_ = glossary_extraction(lemmatize_mode='lemmatize')
index4,_,_,_ = glossary_extraction(lemmatize_mode='porter')
compare_indices.compare_indices(index3,index4,description="Replaced lemmatization with Porter stemming")

index5,_,_,_ = glossary_extraction(capitalization_mode='lower')
index6,_,_,_ = glossary_extraction(capitalization_mode='none')
u5, u6 = compare_indices.compare_indices(index5,index6,description="Omitted conversion to lower case")
print("terms only present with lower case enforcement: ",u5)
print("terms only present without lower case enforcement: ",u6)

# The following comparison requires new POS tagging and thus quite some time
# Hence, it is disabled by default
"""
index8,_,_,_ = glossary_extraction(tokenize_mode='expand contractions',tag_mode="load tagger")
index7,_,_,_ = glossary_extraction(tokenize_mode="standard",tag_mode="load tagger")
u7, u8 = compare_indices.compare_indices(index7,index8,description="Changed tokenization")
print("terms only present with default tokenization: ",u7)
print("terms only present with changed tokenization: ",u8)
"""

index9,_,_,_ = glossary_extraction()
index10,_,_,_ = glossary_extraction(tag_mode="load",tagger_name="tagger")
u9, u10 = compare_indices.compare_indices(index9,index10,description="Changed POS tagging approach")
print("terms only present with default POS tagging: ",u9)
print("terms only present with changed POS tagging: ",u10)

index11,_,_,_ = glossary_extraction(chunk_mode="statistical")
index12,_,_,_ = glossary_extraction(chunk_mode="rule-based")
u11, u12 = compare_indices.compare_indices(index11,index12,description="Changed chunking approach")
print("terms only present with statistical chunking: ",u11)
print("terms only present with rule-based chunking: ",u12)

"""
from nltk.corpus import treebank
no_reqs=500
reqs = [" ".join(sent) for sent in treebank.sents()[:no_reqs]]
ids = list(range(no_reqs))
tags = ["" for sent in treebank.sents()[:no_reqs]]
index13,_,_,_ = glossary_extraction(tag_mode="load tagger", filter_mode="threshold")
"""

index13,_,_,_ = glossary_extraction(filter_mode=["threshold"])
index14,_,_,_ = glossary_extraction(filter_mode=["threshold","specificity"])
u13, u14 = compare_indices.compare_indices(index13,index14,description="Changed index filtering mode")
print("terms only present with pure threshold filtering: ",u13)
print("terms only present with threshold & specificity filtering: ",u14)

short_index, reqs, ids, tag_index = glossary_extraction(chunk_mode="rule-based",threshold_coverage=1,max_lines=100,tag_mode="load tagger")
gt = reader.gt_read(max_lines=100)
gt_index = buildindex.tag_index(gt)
analyze_tags.analyze_tags(short_index,gt_index,name="ground truth term")
list1, list2 = compare_indices.compare_indices(short_index,gt_index,description="Comparing to ground truth")
print("terms only present in generated index: ",list1)
print("terms only present in ground truth: ",list2)

index13,_,_,_ = glossary_extraction(filter_mode=[])
index14,_,_,_ = glossary_extraction(filter_mode=["specificity"])
u13, u14 = compare_indices.compare_indices(index13,index14,description="Changed index filtering mode")
#print("terms only present with filtering: ",u13)
#print("terms only present without filtering: ",u14)