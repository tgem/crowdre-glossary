# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 09:27:09 2017

@author: Tim G
"""

import csv
from nltk.stem import WordNetLemmatizer

# Read in all requirements and store each as a separate complete sentence

def gt_read(max_lines=-1):
    gt = []
    i = 0
    with open('..\\data\\ground_truth.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gt.append(process_tags(row['manual terms']))
            i=i+1
            if max_lines>-1 and i>=max_lines:
                break
    return gt

def reqs_read(read_tags=False,max_lines=-1):
    reqs = []
    ids = []
    tags = []
    i = 0
    with open('..\\data\\requirements.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reqs.append('As a '+row['role']+' I want '+row['feature']+ " so that "+row['benefit']+".")
            ids.append(row['id'])
            tags.append(process_tags(row['tags']))
            i=i+1
            if max_lines>-1 and i>=max_lines:
                break
    if read_tags:
        return reqs, ids, tags
    else:
        return reqs, ids

def process_tags(tagstring,lower_case=True):
    tags = []
    lemmatizer = WordNetLemmatizer()
    tagstring = tagstring.replace('/',',')
    tag_list = tagstring.split(',')
    for tag in tag_list:
        tag = tag.replace(".","")
        tag = lemmatizer.lemmatize(tag)
        tag = tag.strip()
        if lower_case:
            tag = tag.lower()
        words = tag.split(" ")
        tags.append(tuple(word for word in words))
    return tags
