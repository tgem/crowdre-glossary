# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 16:25:50 2017

@author: miconzelmann
"""
import nltk
from nltk.corpus import stopwords
import nltk.collocations
import crowdre_reader
import crowdre_tokenizer
import crowdre_tagger
import crowdre_chunker
import crowdre_termsfilter
import crowdre_lemmatizer
import crowdre_buildindex
import crowdre_indexfilter
import pandas as pd
import crowdre_reader as cr

def glossary_extraction(lemmatize_mode='lemmatize',threshold_coverage=5,mode = 'threshold'):
    reqs, ids = crowdre_reader.reqs_read()
    reqs, ids = crowdre_tokenizer.reqs_tokenize(reqs,ids)
    tagged_reqs, ids = crowdre_tagger.reqs_tag(reqs,ids)

    terms, term_index = crowdre_chunker.reqs_chunk(tagged_reqs,ids)
    terms, term_index = crowdre_termsfilter.terms_filter(terms, term_index)
    terms, term_index = crowdre_lemmatizer.terms_lemmatize(terms, term_index,lemmatize_mode)

    if mode == 'threshold':
        index = crowdre_buildindex.index_from_terms(terms,term_index)
        index = crowdre_indexfilter.index_filter(index,threshold_coverage=threshold_coverage)
    elif mode == 'basic':
        index = crowdre_buildindex.index_from_terms(terms,term_index)
    elif mode == 'stopword':
        index = crowdre_buildindex.index_from_terms(terms,term_index)
        
    return index, reqs, ids

def getKeywords(lMode='lemmatize',tCover=5,kMode = 'threshold'):
    #returns a reduced list of terms and their frequency as dataframes
    
    #get candidates from nlp pipeline
    index,_,_ = glossary_extraction(threshold_coverage = tCover,lemmatize_mode = lMode,mode = kMode)
    oIndex = pd.DataFrame(columns=['keyword','frequency'])
    wordsRemoved = pd.DataFrame(columns=['keyword','frequency'])
    
    #get stopwords from nltk 
    stopWords = set(stopwords.words('english'))
    i = k = 0
    for term in index:
        termstring = ""
        for element in term:
            termstring = termstring + element + " "
        termstring = termstring[0:len(termstring)-1]
        if termstring not in stopWords:
            n=len(index[term])
            oIndex.loc[i] = [termstring,n]
            i += 1
        else:
            n=len(index[term])
            wordsRemoved.loc[k] = [termstring,n]
            k += 1
    oIndex = oIndex.sort_values('frequency',ascending=False)
    return oIndex,wordsRemoved

def keyToReq(keywords):
    reqs,ids = cr.reqs_read()
    oReq = pd.DataFrame(reqs,columns = ['req'])
    oReq['keywords'] = ''
    
    for key in keywords['keyword']:
        ind = oReq['req'].str.contains(key)
        oReq['keywords'][ind]=oReq['keywords'][ind] + "," + key
    tags = pd.read_csv('..\\..\\..\\data\\requirements.csv')
    tags = tags[['tags']]
    oReq['tags']=tags
    return oReq

def DistinctTags(writeTags = False,load = False,loadFile = 'unique Tags.xlsx'):
    if load:
        dTags = pd.read_excel(loadFile)
    else:
        tags = pd.read_csv('..\\..\\..\\data\\requirements.csv')
        tags = tags[['tags']]
        dTags = pd.DataFrame(columns=['tag','freq'])
        from nltk.stem import WordNetLemmatizer
    
        lemmatizer = WordNetLemmatizer()
        wordCount = 0
        for tag in tags['tags']:
            subTags = str(tag).replace('/',',')
            subTags = subTags.split(',')
            for subT in subTags:
                subT.replace(".","")
                subT = lemmatizer.lemmatize(subT)
                if not subT == "":
                    while subT[0]==" " and len(subT) > 1: subT=subT[1:len(subT)]
                    while subT[len(subT)-1]==" " and len(subT) > 1: subT=subT[0:len(subT)-1]
                    ind = dTags['tag'].str.strip()==subT
                    if sum(ind) == 0:
                        dTags.loc[wordCount] = [subT,1]
                        wordCount += 1
                    else:
                        dTags['freq'][ind] += 1
        dTags = dTags.sort_values('freq',ascending = False)
        if writeTags :
            writer = pd.ExcelWriter('unique Tags.xlsx')
            dTags.to_excel(writer,'Tags')
            writer.save()
    return dTags
    