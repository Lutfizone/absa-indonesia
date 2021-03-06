import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

class CategoryFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, sentences):
        file_path = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.abspath(os.path.join(file_path, os.path.pardir))

        features = np.recarray(shape=(len(sentences),),
                               dtype=[('sentence', object), ('word2vec', object), ('glove', object), ('lda', object)], )
        word2vec_cluster = self.read_word_embedding_cluster(
            os.path.join(project_path, "../data/word_embedding/word2vec_cluster_5000.txt"))
        glove_cluster = self.read_word_embedding_cluster(
            os.path.join(project_path, "../data/word_embedding/glove_cluster_5000.txt"))
        lda_cluster = self.read_word_embedding_cluster(
            os.path.join(project_path, "../data/word_embedding/lda100_cluster_5000.txt"))
        for i, text in enumerate(sentences):
            features[i]['sentence'] = text
            features[i]['word2vec'] = self.get_word_embedding(text, word2vec_cluster)
            features[i]['glove'] = self.get_word_embedding(text, glove_cluster)
            features[i]['lda'] = self.get_word_embedding(text, lda_cluster)
        return features

    def get_word_embedding(self, sentence, cluster_dict):
        tokens = sentence.split()
        result = ""
        for token in tokens:
            if token in cluster_dict:
                result += cluster_dict[token] + " "
            else:
                result += "0 "
        return result[:-1]

    def read_word_embedding_cluster(self, filename):
        cluster_dict = {}
        with open(filename, "r") as f:
            for line in f:
                line = line.rstrip()
                tokens = line.split()
                cluster_dict[tokens[0]] = tokens[1]
        return cluster_dict
