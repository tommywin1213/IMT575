# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 18:08:11 2022

@author: Tommy
"""

import json

class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        for line in data:
            record = json.loads(line)
            mapper(record)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        #jenc = json.JSONEncoder(encoding='latin-1')
        jenc = json.JSONEncoder()
        for item in self.result:
            print(jenc.encode(item))
            
#Word Count
import sys

# Part 0
filename = "books.json"  # modify this if needed

# Part 1
mr = MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, 1)

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Part 4
inputdata = open(filename)
mr.execute(inputdata, mapper, reducer)

#Problem 1: Inverted Index
# Part 0
filename = "inverted_index.json"

with open('matrix.json', 'r') as f2:
    data = f2.read()
    print(data)
# Part 1
mr = MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    key = record[1]
    

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of document ids containing word
    # WRITE YOUR CODE HERE

# Part 4
inputdata = open(filename)
mr.execute(inputdata, mapper, reducer)

