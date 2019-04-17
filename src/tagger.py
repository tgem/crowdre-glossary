# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:28:55 2017

@author: Tim G
"""

from nltk.corpus import treebank
from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger, tnt

import os, pickle

# POS tagging

def train_tagger(tagger_name):    
    train_sents = treebank.tagged_sents()[:5000]
    if tagger_name=="TnT" or tagger_name=='tagger':
        trained_tagger = tnt.TnT()
        trained_tagger.train(train_sents)
    else:
        tagger1 = DefaultTagger('NN')
        tagger2 = TrigramTagger(train_sents, backoff=tagger1)
        tagger3 = BigramTagger(train_sents,backoff=tagger2)
        trained_tagger = UnigramTagger(train_sents, backoff=tagger3)
    return trained_tagger

def save_tagger(tagger, tagger_name):
    with open(f'..{os.sep}temp{os.sep}'+tagger_name+'.pickle','wb') as f:
        pickle.dump(tagger,f)
        
def load_tagger(tagger_name):
    with open(f'..{os.sep}temp{os.sep}'+tagger_name+'.pickle','rb') as f:
        return pickle.load(f)

def reqs_tag(reqs,ids,mode='load',tagger_name='tagger'):
    if mode=='load':
        with open(f'..{os.sep}temp{os.sep}tagged_reqs.pickle','rb') as f:
            tagged_reqs = pickle.load(f)
    else:
        if mode=='load tagger':
            tagger = load_tagger(tagger_name)
        else:
            tagger = train_tagger(tagger_name)
            save_tagger(tagger, tagger_name)
        tagged_reqs = [tagger.tag(req) for req in reqs]
    return tagged_reqs, ids
