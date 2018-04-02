# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 09:21:36 2018

@author: Tim G
"""

"""
Glossary term extraction
"""

import reader
import tokenizer
import tagger
import chunker
import termsfilter
import lemmatizer
import buildindex
import indexfilter
import export

"""
Actual pipeline
"""

def glossary_extraction(reqs=[],ids=[],tags=[],max_lines=-1,lemmatize_mode='lemmatize',capitalization_mode='lower',threshold_coverage=5,output='memory',remove_stopwords=True,tokenize_mode="standard",tag_mode="load",tagger_name="tagger",chunk_mode="statistical",filter_mode=["threshold","specificity"]):
    if reqs==[]:
        reqs, ids, tags = reader.reqs_read(read_tags=True,max_lines=max_lines)
    full_reqs = reqs
    reqs, ids = tokenizer.reqs_tokenize(reqs,ids,tokenize_mode=tokenize_mode)
    tagged_reqs, ids = tagger.reqs_tag(reqs,ids,mode=tag_mode,tagger_name=tagger_name)
    """
    In this phase, the leading data structure is terms (list of tuples), which contains
    one entry for each glossary term candidate. Moreover, term_index (list of lists) contains
    the ids of the requirements related to a given glossary term. The relation
    between terms and term_index is established by using the same index for a term in
    terms and term_index
    """
    terms, term_index = chunker.reqs_chunk(tagged_reqs,ids,chunk_mode=chunk_mode)
    terms, term_index = lemmatizer.terms_lemmatize(terms, term_index,lemmatize_mode,capitalization_mode)
    terms, term_index = termsfilter.terms_filter(terms, term_index, remove_stopwords)
    """
    From this point, the leading data structure is index, a dictionary that
    maps glossary term candidates (tuples of strings) to a list of ids of the related
    requirements. terms and term_index have no further use after construction of index
    """
    index = buildindex.index_from_terms(terms,term_index)
    global tag_index
    tag_index = buildindex.tag_index(tags)
    index = indexfilter.index_filter(index,no_reqs=len(reqs),threshold_coverage=threshold_coverage,filter_mode=filter_mode)
    tag_index = indexfilter.index_filter(tag_index,no_reqs=len(tags),threshold_coverage=threshold_coverage,filter_mode="threshold")
    if output=='file':
        export.save_index_as_text(index)
        export.save_index_as_xlsx(index, full_reqs, ids)
    return index, reqs, ids, tag_index
