# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:37:16 2017

@author: Tim G
"""


def index_from_terms(terms,term_index):
    # transform lists to tuples so that they can be used as dict indices
    term_tuples = []
    for term in terms:
        term_tuples.append(tuple(word for word in term))    
    # create dictionary
    index = {}
    for i, term_tuple in enumerate(term_tuples):
        if (term_tuple in index) and (index[term_tuple] is not None):
            if not(term_index[i] in index[term_tuple]):
                index[term_tuple]=index[term_tuple]+[term_index[i]]
        else:
            index[term_tuple]=[term_index[i]]        
    return index

def tag_index(tags):
    index = {}
    for i, tag_list in enumerate(tags):
        for tag in tag_list:
            if (tag in index) and (index[tag] is not None):
                index[tag]=index[tag]+[i]
            else:
                index[tag]=[i]
    return index