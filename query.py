#!/bin/env python
from collections import deque
import os, glob, os.path
import sys
import re

if len(sys.argv) != 2:
  print >> sys.stderr, 'usage: python query.py index_dir' 
  os._exit(-1)

def merge_posting (postings1, postings2):
  new_posting = []
  # provide implementation for merging two postings lists
  print >> sys.stderr, 'you must provide implementation'
  return new_posting

# file locate of all the index related files
index_dir = sys.argv[1]
index_f = open(index_dir+'/corpus.index', 'r')
word_dict_f = open(index_dir+'/word.dict', 'r')
doc_dict_f = open(index_dir+'/doc.dict', 'r')
posting_dict_f = open(index_dir+'/posting.dict', 'r')

word_dict = {}
doc_id_dict = {}
file_pos_dict = {}
doc_freq_dict = {}

print >> sys.stderr, 'loading word dict'
for line in word_dict_f.readlines():
  parts = line.split('\t')
  word_dict[parts[0]] = int(parts[1])
print >> sys.stderr, 'loading doc dict'
for line in doc_dict_f.readlines():
  parts = line.split('\t')
  doc_id_dict[int(parts[1])] = parts[0]
print >> sys.stderr, 'loading index'
for line in posting_dict_f.readlines():
  parts = line.split('\t')
  term_id = int(parts[0])
  file_pos = int(parts[1])
  doc_freq = int(parts[2])
  file_pos_dict[term_id] = file_pos
  doc_freq_dict[term_id] = doc_freq

def read_posting(term_id):
  index_f.seek(file_pos_dict[term_id] + len(str(term_id)) + 1)
  temp = index_f.readline()
  posting_list = temp.strip().split(',')
  return [int(p) for p in posting_list]
  # provide implementation for posting list lookup for a given term
  # a useful function to use is index_f.seek(file_pos), which does a disc seek to 
  # a position offset 'file_pos' from the beginning of the file

def popLeftOrNone(p):
 if len(p) > 0:
   posting = p.popleft()
 else:
   posting = None
 return posting

# read query from stdin
while True:
  input = sys.stdin.readline()
  input = input.strip()
  if len(input) == 0: # end of file reached
    break
  input_parts = input.split()
  input_parts_ids = []

  aNoneFound = False
  for word in input_parts:
    id = word_dict.get(word)
    if id == None:
      aNoneFound = True
      break
    else:
      input_parts_ids.append(id)

  if aNoneFound:
    print >> sys.stdout, 'no results found'

  else:  
    posting_lists = []
    for id in input_parts_ids:
      posting_lists.append(read_posting(id))

    posting_lists = sorted(posting_lists, key=len)

    final_list = posting_lists[0]
    for list in posting_lists[1:]:
      deque1 = deque(final_list)
      deque2 = deque(list)

      p1 = popLeftOrNone(deque1)
      p2 = popLeftOrNone(deque2)

      while p1 is not None and p2 is not None:
        if p1 == p2:
          p1 = popLeftOrNone(deque1)
          p2 = popLeftOrNone(deque2)
        elif p1 < p2:
          final_list.remove(p1)
          p1 = popLeftOrNone(deque1)
        else:
          p2 = popLeftOrNone(deque2)

      if p1 is not None:
        index = final_list.index(p1)
        final_list = final_list[:index]

    if final_list:
      final_doc_list = [doc_id_dict[doc] for doc in final_list]
      final_doc_list = sorted(final_doc_list)
      for doc in final_doc_list:
        print >> sys.stdout, doc
    else:
      print >> sys.stdout, 'no results found'

  # you need to translate words into word_ids
  # don't forget to handle the case where query contains unseen words
  # next retrieve the postings list of each query term, and merge the posting lists
  # to produce the final result

  # posting = read_posting(word_id)

  # don't forget to convert doc_id back to doc_name, and sort in lexicographical order
  # before printing out to stdout
