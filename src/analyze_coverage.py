# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:44:51 2017

@author: Tim G
"""

from collections import defaultdict

def analyze_coverage(index,reqs,ids,threshold=1):
    covered_reqs = defaultdict(int)
    for term in index:
        for reqid in index[term]:
            covered_reqs[reqid]=covered_reqs[reqid]+1
    covered = 0
    total = len(ids)
    not_covered = []
    for i in range(len(ids)):
        if covered_reqs[i]>=threshold:
            covered=covered+1
        else:
            not_covered = not_covered + [reqs[i]]
    return covered/total, not_covered