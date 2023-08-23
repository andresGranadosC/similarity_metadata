# similarity_metadata


This repository contains scripts to quantify the similarity of between two documents which contains one word or short sentences. This software is being tested to compare curated metadata against AI-generated metadata such as keywords and disciplines, then its use is limited to academic purposes only. 

This scripts use the standard NLP libraries as spaCy (https://spacy.io/usage/linguistic-features#vectors-similarity), wn (WordNet - https://wn.readthedocs.io/en/latest/api/wn.similarity.html) for the similarity calculation and other NLP features.

An example of the use is shown in the following plots:

![](https://github.com/andresGranadosC/similarity_metadata/blob/main/plots/Disciplines_spacy_sim_2.png)

where the horizontal axis shows the ai-generated disciplines and the vertical axis represents the curated and indexed disciplines. Each point in the matrix shows the similarity between each pair of sentences (or words).

The soft precision, recall and F-score scores are based on the following documentation: [Soft precision and recall](https://www.sciencedirect.com/science/article/pii/S0167865523000296) from Pasi Fränti,Radu and Mariescu-Istodor in Pattern Recognition Letters, Elsevier, 2023.
