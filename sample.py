from sklearn.cross_validation import train_test_split
from gensim.models.word2vec import Word2Vec
import numpy as np
from sklearn.preprocessing import scale
from sklearn.linear_model import SGDClassifier
import os

model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
vector = []


def odd(words):
	for word in words:

		if word not in model:
			return word

		vector.append(model[word] / np.linalg.norm(model[word]))
	mean = np.array(vector).mean(axis=0)
	mean = mean / np.linalg.norm(mean)

	dists = [np.linalg.norm(v - mean) for v in vector]
	return words[np.argmax(dists)]


def main():
	print 'Input:'
	while (True):
		words = raw_input('=').lower().split(' ')
		print 'Odd one out:', odd(words)


if __name__ == '__main__':
	main()