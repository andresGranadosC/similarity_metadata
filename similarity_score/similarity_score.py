#import spacy
import numpy as np
import string
import de_core_news_lg

class Similarity:
    
    def __init__(self, ground_truth, generic_crawler):
        self.nlp = de_core_news_lg.load()
        self.gt = ground_truth
        self.gc = generic_crawler
        self.clean_texts()
        
    # Delete
    def compute_score(self):
        print("Printing args", self.gt, self.gc)

    def remove_punctuation(self, text):
        for p in string.punctuation:
            text = text.replace(p, " ")
        return text
        
    def clean_texts(self):
        cc_=[]
        for cc in self.gt:
            np_punct_text1 = self.remove_punctuation(cc)
            doc1 = self.nlp(np_punct_text1)
            cc_.append( doc1 )
        self.cc_cleaned = cc_
        
        gc_=[]
        for gc in self.gc:
            np_punct_text2 = self.remove_punctuation(gc)
            doc2 = self.nlp(np_punct_text2)
            gc_.append( doc2 )
        self.gc_cleaned = gc_
        
    def gen_recall(self):
        paths=[]
        for doc1 in self.cc_cleaned:
            path_row = []
            for doc2 in self.gc_cleaned:
                similarity_score = doc1.similarity(doc2)
                path_row.append( np.abs( similarity_score ) )
            paths.append( path_row )
        similarities = np.array(paths)
        max_args = []
        for i in range(len(self.gt)):
            max_arg = similarities[i].argmax()
            if similarities[i][max_arg] != 0:
                max_args.append( max_arg )
                #print( self.gt[i] , " <-> ", self.gc[ max_arg ], ":", float("{:.3f}".format(similarities[i][max_arg]))  )
    
        recall = similarities.max(axis = 1).sum()/len( self.cc_cleaned )
        return similarities, recall
        
    
    
    def count_set(self, A, i):
        sim_A_i = 0
        doc1 = A[i]
        for j in range(len( A )):
            doc2 = A[j]
            sim_A_i = sim_A_i + np.abs( doc1.similarity(doc2) )
        return 1/sim_A_i
    
    # Cardinality function

    def card(self, A):
        return np.sum( [ self.count_set(A, i) for i in range(len(A)) ] ) 

    # Soft precision, recall, F-score

    def soft_precision(self):
        G, P = self.cc_cleaned, self.gc_cleaned
        intersection = self.card(G) + self.card(P) - self.card(G+P)
        return intersection/self.card(P)

    def soft_recall(self):
        G, P = self.cc_cleaned, self.gc_cleaned
        intersection = self.card(G) + self.card(P) - self.card(G+P)
        return intersection/self.card(G)

    def soft_fscore(self):
        G, P = self.cc_cleaned, self.gc_cleaned
        intersection = self.card(G) + self.card(P) - self.card(G+P)
        return 2*intersection/( self.card(G) + self.card(P) )
        
        
