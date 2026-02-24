"""
TF-IDF Vectorizer - Solution

Implements a TF-IDF vectorizer from scratch. Learns vocabulary and IDF weights
from a training corpus, then transforms documents into dense TF-IDF vectors.
"""

import math
import string
from collections import Counter


class TfidfVectorizer:
    """A TF-IDF vectorizer that learns vocabulary and IDF weights from a
    corpus and transforms documents into dense TF-IDF vectors.
    """

    def __init__(self, max_features: int = None, lowercase: bool = True):
        """Initialise the vectorizer.

        Args:
            max_features: If not None, keep only the top max_features terms
                          ordered by document frequency. If None, keep all.
            lowercase: Whether to convert documents to lowercase before
                       tokenising.
        """
        self.max_features = max_features
        self.lowercase = lowercase
        self.vocabulary_ = {}
        self.idf_ = {}

    def _tokenize(self, document: str) -> list:
        """Tokenise a document into a list of terms.

        Splits on whitespace, strips leading/trailing punctuation from each
        token, and optionally lowercases.

        Args:
            document: A single document string.

        Returns:
            A list of cleaned token strings (empty tokens are discarded).
        """
        if self.lowercase:
            document = document.lower()
        tokens = document.split()
        tokens = [tok.strip(string.punctuation) for tok in tokens]
        tokens = [tok for tok in tokens if tok]
        return tokens

    def fit(self, documents: list) -> 'TfidfVectorizer':
        """Learn vocabulary and IDF weights from a list of documents.

        IDF(t) = log(N / df(t)) + 1

        Args:
            documents: A list of document strings.

        Returns:
            self, to allow method chaining.
        """
        N = len(documents)

        # Compute document frequency for each term
        df = Counter()
        for doc in documents:
            tokens = self._tokenize(doc)
            unique_terms = set(tokens)
            for term in unique_terms:
                df[term] += 1

        # If max_features is set, keep only top-N terms by document frequency
        if self.max_features is not None:
            # Sort by df descending, then alphabetically for ties
            top_terms = sorted(df.keys(), key=lambda t: (-df[t], t))
            top_terms = top_terms[:self.max_features]
        else:
            top_terms = list(df.keys())

        # Build vocabulary sorted alphabetically
        sorted_terms = sorted(top_terms)
        self.vocabulary_ = {term: idx for idx, term in enumerate(sorted_terms)}

        # Compute IDF for each term in vocabulary
        self.idf_ = {}
        for term in self.vocabulary_:
            self.idf_[term] = math.log(N / df[term]) + 1

        return self

    def transform(self, documents: list) -> list:
        """Transform documents into TF-IDF vectors.

        TF(t, d)  = count(t in d) / total_terms_in_d
        TF-IDF    = TF * IDF

        Args:
            documents: A list of document strings.

        Returns:
            A list of lists (dense matrix) of shape (n_documents, n_features).
        """
        matrix = []
        vocab_size = len(self.vocabulary_)

        for doc in documents:
            tokens = self._tokenize(doc)
            total_terms = len(tokens)
            counts = Counter(tokens)

            vector = [0.0] * vocab_size
            if total_terms > 0:
                for term, idx in self.vocabulary_.items():
                    if term in counts:
                        tf = counts[term] / total_terms
                        vector[idx] = tf * self.idf_[term]

            matrix.append(vector)

        return matrix

    def fit_transform(self, documents: list) -> list:
        """Fit the vectorizer and transform the documents in one step.

        Args:
            documents: A list of document strings.

        Returns:
            A list of lists (dense matrix) of TF-IDF vectors.
        """
        return self.fit(documents).transform(documents)

    def get_feature_names(self) -> list:
        """Return the list of feature (term) names in vocabulary order.

        Returns:
            A list of strings sorted alphabetically, matching the column
            order of the vectors returned by transform().
        """
        return sorted(self.vocabulary_, key=self.vocabulary_.get)
