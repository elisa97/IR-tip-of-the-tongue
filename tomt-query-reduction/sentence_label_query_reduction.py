import sys
import os
from pathlib import Path
sys.env.append((Path(__file__) / '..').abspath())


class QueryReduction():
    def reduce_tomt_query(tomt_query):
        raise ValueError('Please implement this.')


class SentenceLevelQueryReduction():
    def __init__(self, labels=None):
        self.labels = self.labels.split(',') if labels and type(labels) == str else labels

