# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:35:37 2017

@author: Tim G
"""

# Lemmatization

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

def terms_lemmatize(terms, term_index, lemmatize_mode='lemmatize', capitalization_mode='lower'):
    if capitalization_mode=='lower':
        terms, term_index = enforce_lowercase(terms, term_index)
    if lemmatize_mode=='lemmatize':
        terms, term_index = wordnet_lemmatize(terms,term_index)
    else:
        if lemmatize_mode=='porter':
            terms, term_index = porter_stem(terms,term_index)
    return terms, term_index

def enforce_lowercase(terms, term_index):
    lowercase_terms = []
    for term in terms:
        lowc_term = [word.lower() for word in term]
        lowercase_terms.append(lowc_term)
    terms = lowercase_terms
    return terms, term_index

def wordnet_lemmatize(terms, term_index):
    lemmatizer = WordNetLemmatizer()
    lemmatized_terms = []
    for term in terms:
        lem_term = []
        for word in term:
            if word=='less': # workaround for known problem, lemmatizer wrongly reduces 'less' to 'le'
                lem_term = lem_term + [word]
            else:
                lem_term = lem_term + [lemmatizer.lemmatize(word)]
        lemmatized_terms.append(lem_term)
    terms = lemmatized_terms
    return terms, term_index

def porter_stem(terms, term_index):
    stemmer = PorterStemmer()
    lemmatized_terms = []
    for term in terms:
        lem_term = [stemmer.stem(word) for word in term]
        lemmatized_terms.append(lem_term)
    terms = lemmatized_terms
    return terms, term_index
