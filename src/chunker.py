# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:31:50 2017

@author: Tim G
"""

# Chunking

from nltk.chunk import ChunkParserI, RegexpParser
from nltk.chunk.util import tree2conlltags, conlltags2tree
from nltk.tag import UnigramTagger, BigramTagger
from nltk.corpus import treebank_chunk

def backoff_tagger(train_sents, tagger_classes, backoff=None):
    for cls in tagger_classes:
        backoff = cls(train_sents, backoff=backoff)
    return backoff

def conll_tag_chunks(chunk_sents):
    tagged_sents = [tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in sent] for sent in tagged_sents]

class TagChunker(ChunkParserI):
    def __init__(self, train_chunks, tagger_classes=[UnigramTagger,
                                                     BigramTagger]):
        train_sents = conll_tag_chunks(train_chunks)
        self.tagger = backoff_tagger(train_sents, tagger_classes)
    
    def parse(self, tagged_sent):
        if not tagged_sent: return None
        (words, tags) = zip(*tagged_sent)
        chunks = self.tagger.tag(tags)
        wtc = zip(words, chunks)
        return conlltags2tree([(w,t,c) for (w,(t,c)) in wtc])

def reqs_chunk(tagged_reqs,ids,chunk_mode="statistical"):
    if chunk_mode=="statistical":
        terms, term_index = statistical_reqs_chunk(tagged_reqs,ids)
    else:
        terms, term_index = rule_based_reqs_chunk(tagged_reqs,ids)
    return terms, term_index

def statistical_reqs_chunk(tagged_reqs,ids):
    train_chunks = treebank_chunk.chunked_sents()[:100]
    chunker = TagChunker(train_chunks)
    terms=[]
    term_index=[]
    for i, t in enumerate(tagged_reqs):
        s=chunker.parse(t)
        for c in s:
            if not isinstance(c,tuple):
                if c.label()=='NP':
                    term=[]
                    for tagged_word in c:
                        if (tagged_word[1]!='DT') and (tagged_word[1]!='PRP$'):
                            term=term+[tagged_word[0]]
                    terms.append(term)
                    term_index.append(i)
    return terms, term_index

# ruleset from Youngja Park, Roy J. Byrd, Branimir K. Boguraev 2002, only the <VB> removed to avoid false positives
ruleset = r'''
NP:
{<DT>?(<JJ>(<CC><JJ>)*|(<NN>|<NP>|<NPS>))*(<NN>|<NP>|<NPS>)}
'''

def rule_based_reqs_chunk(tagged_reqs,ids):
    chunker = RegexpParser(ruleset)
    terms=[]
    term_index=[]
    for i, t in enumerate(tagged_reqs):
        s=chunker.parse(t)
        for c in s:
            if not isinstance(c,tuple):
                if c.label()=='NP':
                    term=[]
                    for tagged_word in c:
                        if (tagged_word[1]!='DT') and (tagged_word[1]!='PRP$'):
                            term=term+[tagged_word[0]]
                    terms.append(term)
                    term_index.append(i)
    return terms, term_index
