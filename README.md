# Artificial Intelligence with Machine Learning Classification Techniques

This repo contains two parts,

1. Spam Classification using Naive Bayes and Decision Tree Techniques.
  
  How to run the code?
  - python spam.py mode technique dataset-directory model-file

where mode is either test or train, technique is either bayes or dt, 
dataset-directory is a directory containing two subdirectories named spam and notspam, 
each ﬁlled with documents of the corresponding type, and model-ﬁle is the ﬁlename of your trained model. 

2. Topic classification.

  How to run the code?
  -python topics.py mode dataset-directory model-file [fraction]

where mode is either test or train, dataset-directory is a directory containing directories 
for each of the topics (you can assume there are exactly 20), and model-ﬁle is the ﬁlename of your trained model. 
In training mode, an additional parameter fraction should be a number between 0.0 and 1.0 indicating the fraction of labeled training examples that your training algorithm is allowed to see.
