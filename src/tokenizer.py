# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:24:36 2017

@author: Tim G
"""

import nltk
import re

# Tokenize using nltk standard tokenizer
# NB: This tokenizer splits contraction without expansion, i.e. "can't" becomes ["ca","n't"]

def reqs_tokenize(reqs,ids,tokenize_mode="standard"):
    if tokenize_mode=="expand contractions":
        for i, req in enumerate(reqs):
            m = re.search("can't",req)
            if not m is None:
                reqs[i] = req[:m.start()]+"cannot"+req[m.end():]
            m = re.search("won't",reqs[i])
            if not m is None:
                reqs[i] = reqs[i][:m.start()]+"will not"+reqs[i][m.end():]
            m = re.search("n't",reqs[i])
            if not m is None:
                reqs[i] = reqs[i][:m.start()]+"not"+reqs[i][m.end():]
            m = re.search("I'm",reqs[i])
            if not m is None:
                reqs[i] = reqs[i][:m.start()]+"I am"+reqs[i][m.end():]
            m = re.search("'re",reqs[i])
            if not m is None:
                reqs[i] = reqs[i][:m.start()]+" are"+reqs[i][m.end():]                
    reqs = [nltk.word_tokenize(req) for req in reqs]
    return reqs, ids
