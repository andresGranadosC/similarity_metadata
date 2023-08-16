import wn
import nltk
import numpy as np
import matplotlib.pyplot as plt
from wn.similarity import wup


hyde = wn.Wordnet("hyde")

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
        	p = wup( cc_p[0], gc_p[0], simulate_root=True )
        path_row.append( p )
    paths.append( path_row )

paths = np.array(paths)

fig, ax = plt.subplots()
im = ax.imshow(paths)
ax.set_xticks(np.arange(len(gc_keywords_tokenized)), labels=gc_keywords_tokenized)
ax.set_yticks(np.arange(len(cc_keywords_tokenized)), labels=cc_keywords_tokenized)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
for i in range(len(cc_keywords_tokenized)):
    for j in range(len(gc_keywords_tokenized)):
        text = ax.text(j, i, float("{:.4f}".format(paths[i, j])),
                       ha="center", va="center", color="w")
ax.set_title("Keywords wup similarity")
fig.tight_layout()
plt.savefig("wordnet_keywords_wup.png", dpi=150)
plt.show()