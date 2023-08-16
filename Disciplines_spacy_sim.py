import spacy
import numpy as np
import matplotlib.pyplot as plt
import string


nlp = spacy.load("de_core_news_lg")

# 1.
cc_keywords_tokenized = [ 'Biologie', 'Geografie', 'Physik' ]
gc_keywords_tokenized = [ 'Energien','Sonnenenergie','Elektrotechnik beschäftigen' ]

# 2.
#cc_keywords_tokenized = [ 'Informatik', 'Medienbildung' ]
#gc_keywords_tokenized = [ 'Informatik', 'Mathematik', 'Naturwissenschaften' ]

# 3.
#cc_keywords_tokenized = [ 'Mathematik' ]
#gc_keywords_tokenized = [ 'Mathematik', 'Physik', 'Geometrie' ]


# 5.
#cc_keywords_tokenized = [ 'Geografie','Ethik','Politik' ]
#gc_keywords_tokenized = ['Gesellschaftskunde', 'Nachhaltigkeit', 'Politik']



def remove_punctuation(text):
    for p in string.punctuation:
        text = text.replace(p, " ")
    return text
    
cc_cleaned=[]
for cc in cc_keywords_tokenized:
    np_punct_text1 = remove_punctuation(cc)
    doc1 = nlp(np_punct_text1)
    cc_cleaned.append( doc1 )
    
gc_cleaned=[]
for gc in gc_keywords_tokenized:
    np_punct_text2 = remove_punctuation(gc)
    doc2 = nlp(np_punct_text2)
    gc_cleaned.append( doc2 )

paths=[]
for doc1 in cc_cleaned:
    path_row = []
    for doc2 in gc_cleaned:
        similarity_score = doc1.similarity(doc2)
        path_row.append( similarity_score )
    paths.append( path_row )


# Print matches and exclude lowest scores

similarities = np.array(paths)

max_args = []
for i in range(len(cc_keywords_tokenized)):
    max_arg = similarities[i].argmax()
    if similarities[i][max_arg] != 0:
        max_args.append( max_arg )
        print( cc_keywords_tokenized[i] , " <-> ", gc_keywords_tokenized[ max_arg ], ":", float("{:.3f}".format(similarities[i][max_arg]))  )

score = np.abs(similarities.max(axis = 1)).sum()/len( cc_keywords_tokenized )
print()
print("Score:", score)

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
plt.savefig("Keywords_spacy_sim.png", dpi=150)
