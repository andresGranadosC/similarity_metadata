import spacy
import numpy as np
import matplotlib.pyplot as plt
import string


nlp = spacy.load("de_core_news_lg")

# 1.
cc_keywords_tokenized = [ 'Planet-Schule','Sonnenenergie', 'Solarenergie', 'Solarzelle', 'Solarthermie', 'Solarthermisches Kraftwerk' ]
gc_keywords_tokenized = [ 'Solarenergie', 'Solarkollektoren', 'Solarzellen', 'Solarthermie-Kraftwerke' ]

# 3.
#cc_keywords_tokenized = [ 'Aufgaben zum Volumen eines Quaders', 'Volumenberechnung', 'Räumliche Figuren', 'Geometrie', 'Mathe' ]
#gc_keywords_tokenized = [ 'Volumen', 'Quader', 'Wasser', 'LKW' ]

# 4.
#cc_keywords_tokenized = [ 'Allgemeinbildung','Allgemeinwissen','Bildung','Information','Medienangebote','Planet Schule','Reportage','Sachkenntnis','Sachverhalte','Sachwissen' ]
#gc_keywords_tokenized = [ 'Video', 'herunterladen', 'Fontane', 'Dichter' ]

# 5.
#cc_keywords_tokenized = [ 'Demonstration', 'Klimaschwankung', 'Jugendlicher', 'Protest' ]
#gc_keywords_tokenized = [ 'Klimastreik', 'Greta Thunberg', 'Fridays For Future', 'Protestbewegung' ]



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
ax.set_title("Keywords spacy similarity")
fig.tight_layout()
fig.colorbar(im)
plt.savefig("Keywords_spacy_sim.png", dpi=150)
