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

# main script

def key_figures(filter_mode=["threshold","specificity"],description="",threshold_coverage=1):
    global gt_index
    index, reqs, ids, tag_index = glossary_extraction(filter_mode=filter_mode)
    compare_indices.analyze_index(index,reqs,ids,description=description)
    short_index, reqs, ids, tag_index = glossary_extraction(threshold_coverage=threshold_coverage,
                                                            max_lines=100,
                                                            tag_mode="load tagger",
                                                            filter_mode=filter_mode)
    gt = reader.gt_read(max_lines=100)
    gt_index = buildindex.tag_index(gt)
    gt_index = indexfilter.index_filter(gt_index,100,threshold_coverage=threshold_coverage,filter_mode=filter_mode)
    analyze_tags.analyze_tags(short_index,gt_index,name="ground truth term",silent=True)
    print("Number of glossary terms extracted from first 100 reqs:",len(short_index.keys()))
    print("Number of ground truth terms extracted from first 100 reqs:",len(gt_index.keys()))
    print("Recall (regarding ground truth, including partial matches): ",
          (analyze_tags.no_terms_as_tags+analyze_tags.no_terms_as_tag_parts
           +analyze_tags.no_tags_as_term_parts)/
          len(gt_index.keys()))
    print("Precision (regarding ground truth, including partial matches): ",
          (analyze_tags.no_terms_as_tags+analyze_tags.no_terms_as_tag_parts
           +analyze_tags.no_tags_as_term_parts)/
          len(short_index.keys()))

def key_figures_by_threshold(threshold_coverage=5):
    print("Analysis for threshold value of",threshold_coverage)
    key_figures(filter_mode=[],description="Only linguistic",threshold_coverage=threshold_coverage)
    key_figures(filter_mode=["specificity"],description="Only specificity",threshold_coverage=threshold_coverage)
    key_figures(filter_mode=["threshold"],description="Only relevance",threshold_coverage=threshold_coverage)
    key_figures(filter_mode=["threshold","specificity"],description="Relevance & specificity",threshold_coverage=threshold_coverage)
    print()
    print()

key_figures_by_threshold(threshold_coverage=1)
key_figures_by_threshold(threshold_coverage=3)
key_figures_by_threshold(threshold_coverage=5)
    

