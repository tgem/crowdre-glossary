# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:34:43 2017

@author: Tim G
"""

from nltk.corpus import stopwords
 
# Simplification

def terms_filter(terms, term_index, remove_stopwords=True):
    undesired_beginnings = ['certain',"'s","'", 'which','what','other','one','much','more','me','i']
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
    else:
        stop_words = set([])
    reduced_terms = []
    for term in terms:
        red_term = []
        if len(term)>=1:
            if not(term[0] in undesired_beginnings) and not(term[0] in stop_words) and not(is_int(term[0])):
                red_term.append(term[0])
            for element in term[1:]: 
                if not(element in stop_words) and not(is_int(element)):
                    red_term.append(element)
        reduced_terms.append(red_term)
    terms = reduced_terms
    return terms, term_index

def is_int(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True