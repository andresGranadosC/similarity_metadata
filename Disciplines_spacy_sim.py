import spacy
import numpy as np
import matplotlib.pyplot as plt
import string


nlp = spacy.load("de_core_news_lg")

# Example
cc_keywords_tokenized = [ 'Biologie', 'Geografie', 'Physik' ]
gc_keywords_tokenized = [ 'Energien','Sonnenenergie','Elektrotechnik beschäftigen' ]



def remove_punctuation(text):
    for p in string.punctuation:
        text = text.replace(p, " ")
    return text
    
cc_=[]
for cc in cc_keywords_tokenized:
    np_punct_text1 = remove_punctuation(cc)
    doc1 = nlp(np_punct_text1)
    cc_.append( doc1 )
    
gc_=[]
for gc in gc_keywords_tokenized:
    np_punct_text2 = remove_punctuation(gc)
    doc2 = nlp(np_punct_text2)
    gc_.append( doc2 )


# Generalised Recall test. Print matches and exclude lowest scores

def gen_recall(cc_cleaned, gc_cleaned):
    paths=[]
    for doc1 in cc_cleaned:
        path_row = []
        for doc2 in gc_cleaned:
            similarity_score = doc1.similarity(doc2)
            path_row.append( np.abs( similarity_score ) )
        paths.append( path_row )
    similarities = np.array(paths)
    max_args = []
    for i in range(len(cc_keywords_tokenized)):
        max_arg = similarities[i].argmax()
        if similarities[i][max_arg] != 0:
            max_args.append( max_arg )
            print( cc_keywords_tokenized[i] , " <-> ", gc_keywords_tokenized[ max_arg ], ":", float("{:.3f}".format(similarities[i][max_arg]))  )
    
    recall = similarities.max(axis = 1).sum()/len( cc_cleaned )
    return similarities, recall

similarities, generalised_recall = gen_recall(cc_, gc_)
print()
print("Generalized recall score:{:.3f}".format(generalised_recall))
print()


# SOFT PRECISION, RECALL, F-SCORE
# Count function

def count_set(A, i):
    sim_A_i = 0
    doc1 = A[i]
    for j in range(len( A )):
        doc2 = A[j]
        sim_A_i = sim_A_i + np.abs( doc1.similarity(doc2) )
    return 1/sim_A_i
    
# Cardinality function

def card(A):
    return np.sum( [ count_set(A, i) for i in range(len(A)) ] ) 

# Soft precision, recall, F-score

def soft_precision(G, P):
    intersection = card(G) + card(P) - card(G+P)
    return intersection/card(P)

def soft_recall(G, P):
    intersection = card(G) + card(P) - card(G+P)
    return intersection/card(G)

def soft_fscore(G, P):
    intersection = card(G) + card(P) - card(G+P)
    return 2*intersection/( card(G) + card(P) )

print()
print("Soft precision: {:.3f}".format( soft_precision(cc_, gc_) ))
print("Soft recall: {:.3f}".format( soft_recall(cc_, gc_) ))
print("Soft F-score: {:.3f}".format( soft_fscore(cc_, gc_) ))

# Plot everything


fig, ax = plt.subplots()
im = ax.imshow(similarities, vmin=-1, vmax=1)
ax.set_xticks(np.arange(len(gc_keywords_tokenized)), labels=gc_keywords_tokenized)
ax.set_yticks(np.arange(len(cc_keywords_tokenized)), labels=cc_keywords_tokenized)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
for i in range(len(cc_keywords_tokenized)):
    for j in range(len(gc_keywords_tokenized)):
        text = ax.text(j, i, float("{:.3f}".format(similarities[i, j])),
                       ha="center", va="center", color="w")
ax.set_title("Disciplines spacy similarity")
fig.tight_layout()
fig.colorbar(im)
plt.savefig("Disciplines_spacy_sim.png", dpi=150)
