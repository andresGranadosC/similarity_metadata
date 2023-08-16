import wn
import nltk
import numpy as np
import matplotlib.pyplot as plt
from wn.similarity import path

#tokens = nltk.word_tokenize("Der Katze isst ein Fisch", 'german')
hyde = wn.Wordnet("hyde")
#Sonnenenergie = odenet.synsets('Sonnenenergie')[0]
#path(Sonnenenergie, odenet.synsets('Solarenergie')[0])
cc_keywords_tokenized = [ 'Planet-Schule','Sonnenenergie', 'Solarenergie', 'Solarzelle', 'Solarthermie', 'Solarthermisches Kraftwerk' ]
gc_keywords_tokenized = [ 'Solarenergie', 'Solarkollektoren', 'Solarzellen', 'Solarthermie-Kraftwerke' ]
paths=[]
for cc in cc_keywords_tokenized:
    path_row = []
    for gc in gc_keywords_tokenized:
        cc_p = hyde.synsets(cc)
        gc_p = hyde.synsets(gc)
        p = 0
        if len(cc_p) > 0 and len(gc_p) > 0:
        	p = path( cc_p[0], gc_p[0], simulate_root=True )
        path_row.append( p )
    paths.append( path_row )

paths = np.array(paths)

# Print matches and exclude lowest scores

similarities = np.array(paths)

max_args = []
for i in range(len(cc_keywords_tokenized)):
    max_arg = similarities[i].argmax()
    if similarities[i][max_arg] != 0:
        max_args.append( max_arg )
        print( cc_keywords_tokenized[i] , " <-> ", gc_keywords_tokenized[ max_arg ], ":", similarities[i][max_arg] )
            
score = similarities.max(axis = 1).sum()/len( cc_keywords_tokenized )
print()
print("Score:", score)
        
# Plot everything

fig, ax = plt.subplots()
im = ax.imshow(paths)
ax.set_xticks(np.arange(len(gc_keywords_tokenized)), labels=gc_keywords_tokenized)
ax.set_yticks(np.arange(len(cc_keywords_tokenized)), labels=cc_keywords_tokenized)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
for i in range(len(cc_keywords_tokenized)):
    for j in range(len(gc_keywords_tokenized)):
        text = ax.text(j, i, float("{:.2f}".format(paths[i, j])),
                       ha="center", va="center", color="w")
ax.set_title("Keywords path distance")
fig.tight_layout()
fig.colorbar(im, orientation='vertical')
#plt.savefig("wordnet_keywords_PS.png", dpi=150)
plt.show()