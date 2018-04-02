# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:43:23 2018

@author: Tim G
"""

def analyze_tags(index,tag_index,name="tag"):
    print(" Number of glossary terms: "+str(len(index.keys())))
    print(" Number of "+name+": "+str(len(tag_index.keys())))
    # how many glossary terms are tags?
    no_terms_as_tags = 0
    no_terms_as_tag_parts = 0
    no_tags_as_term_parts = 0
    global terms_as_tags
    terms_as_tags = []
    global terms_as_tag_parts
    terms_as_tag_parts = []
    for term in index.keys():
        if (term in tag_index.keys()) and (tag_index[term] is not None):
            no_terms_as_tags = no_terms_as_tags + 1
            terms_as_tags = terms_as_tags + [term]
        else:
            for tag in tag_index.keys():
                if contained(term,tag):
                    no_terms_as_tag_parts = no_terms_as_tag_parts + 1
                    terms_as_tag_parts = terms_as_tag_parts + [(term,tag)]
                    break
            for tag in tag_index.keys():
                if contained(tag,term):
                    no_tags_as_term_parts = no_tags_as_term_parts + 1
                    break
    print("Number of terms also used as "+name+"s: "+str(no_terms_as_tags));
    print("Number of terms that are part of, but not identical to "+name+"s: "+str(no_terms_as_tag_parts))
    print("Number of "+name+"s that are part of, but not identical to terms: "+str(no_tags_as_term_parts))
    no_identical_terms = 0
    global identical_terms
    identical_terms = []
    no_contained_terms = 0
    global contained_terms
    contained_terms = []
    global contained_term_tuples
    contained_term_tuples = []
    no_contained_tags = 0
    global contained_tags
    contained_tags = []
    global contained_tag_tuples
    contained_tag_tuples = []
    for term in index.keys():
        for tag in tag_index.keys():
            term_in_tag = contained(index[term],tag_index[tag])
            tag_in_term = contained(tag_index[tag],index[term])
            if term_in_tag and tag_in_term:
                no_identical_terms = no_identical_terms + 1
                identical_terms = identical_terms + [term]
                break
            else:
                if contained(index[term],tag_index[tag]):
                    no_contained_terms = no_contained_terms + 1
                    contained_terms = contained_terms + [term]
                    contained_term_tuples = contained_term_tuples + [(term,tag)]
                    break
                if contained(tag_index[tag],index[term]):
                    no_contained_tags = no_contained_tags + 1
                    contained_tags = contained_tags + [tag]
                    contained_tag_tuples = contained_tag_tuples + [(tag,term)]
                    break
    print("Number of terms where the requirements list matches exactly the requirements list of a "+name+":"+str(no_identical_terms))
    print("Number of terms where the requirements list is contained in the requirements list of a "+name+":"+str(no_contained_terms))
    print("Number of "+name+"s where the requirements list is contained in the requirements list of a term:"+str(no_contained_tags))

def contained(tuple1,tuple2):
    for element in tuple1:
        if not element in tuple2:
            return False
    return True    