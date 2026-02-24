"""
TF-IDF Vectorizer
=================
Category   : ML Engineering
Difficulty : ** (2/5)

Problem
-------
Implement a TF-IDF (Term Frequency -- Inverse Document Frequency) vectorizer
from scratch using only Python standard library modules.  The vectorizer
learns a vocabulary and IDF weights from a training corpus, then transforms
documents into dense TF-IDF vectors.

TF-IDF is a foundational technique in information retrieval and natural
language processing.  It surfaces words that are important to a document
relative to the whole corpus by down-weighting terms that appear everywhere.

Real-world motivation
---------------------
Search engines, document classifiers, and recommendation systems all rely on
TF-IDF or its successors.  Understanding how it works from first principles
builds intuition for more advanced embeddings (Word2Vec, BERT) and teaches
you to think about sparsity, vocabulary management, and numerical
representation of text.

Formulas
--------
    TF(t, d)  = count(t in d) / total_terms_in_d
    IDF(t)    = log(N / df(t)) + 1
    TF-IDF    = TF * IDF

where N is the total number of documents and df(t) is the number of documents
that contain term t.

Hints
-----
1. Tokenise by splitting on whitespace and stripping punctuation with
   str.strip(string.punctuation).
2. Build the vocabulary from the training corpus in fit().  Sort it
   alphabetically so feature indices are deterministic.
3. If max_features is set, keep only the top-N terms by document frequency.
4. In transform(), compute TF and multiply by the stored IDF for each term.
5. Return a list of lists (dense matrix), not a sparse representation.

Run command
-----------
    pytest 08_tf_idf_vectorizer/test_exercise.py -v
"""

import math
import re
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
                          ordered by document frequency.  If None, keep all.
            lowercase: Whether to convert documents to lowercase before
                       tokenising.
        """
        # TODO: Store max_features and lowercase.
        # TODO: Initialise vocabulary_ (dict mapping term -> index) and
        #       idf_ (dict mapping term -> IDF value) to empty dicts.
        # Hint: These will be populated during fit().
        pass

    def _tokenize(self, document: str) -> list:
        """Tokenise a document into a list of terms.

        Splits on whitespace, strips leading/trailing punctuation from each
        token, and optionally lowercases.

        Args:
            document: A single document string.

        Returns:
            A list of cleaned token strings (empty tokens are discarded).
        """
        # TODO: Optionally lowercase the document.
        # TODO: Split on whitespace.
        # TODO: Strip punctuation from each token using
        #       token.strip(string.punctuation).
        # TODO: Discard empty strings.
        # Hint: [tok.strip(string.punctuation) for tok in doc.split()]
        #       then filter out empty strings.
        pass

    def fit(self, documents: list) -> 'TfidfVectorizer':
        """Learn vocabulary and IDF weights from a list of documents.

        IDF(t) = log(N / df(t)) + 1

        where N is the number of documents and df(t) is the number of
        documents containing term t.

        Args:
            documents: A list of document strings.

        Returns:
            self, to allow method chaining.
        """
        # TODO: Tokenise every document.
        # TODO: Compute document frequency (df) for each term -- the number
        #       of documents that contain the term (count each term once per
        #       document, not once per occurrence).
        # TODO: If max_features is set, keep only the top-N terms by df.
        # TODO: Build vocabulary_ as a dict mapping term -> column index,
        #       sorted alphabetically.
        # TODO: Compute idf_ for each term in the vocabulary.
        # Hint: Use set(tokens) per document to avoid double-counting.
        #       idf[term] = math.log(N / df[term]) + 1
        pass

    def transform(self, documents: list) -> list:
        """Transform documents into TF-IDF vectors using the fitted
        vocabulary and IDF weights.

        TF(t, d)  = count(t in d) / total_terms_in_d
        TF-IDF    = TF * IDF

        Args:
            documents: A list of document strings.

        Returns:
            A list of lists (dense matrix) of shape
            (n_documents, n_features).  Each inner list has one float per
            vocabulary term.
        """
        # TODO: For each document:
        #   1. Tokenise.
        #   2. Count term frequencies.
        #   3. Compute TF = count / total_terms.
        #   4. Multiply TF by the stored IDF for each vocabulary term.
        #   5. Build a vector of length len(vocabulary_), defaulting to 0.0
        #      for terms not present in the document.
        # Hint: total_terms = len(tokens)
        #       tf = count / total_terms
        #       tfidf = tf * self.idf_[term]
        pass

    def fit_transform(self, documents: list) -> list:
        """Fit the vectorizer and transform the documents in one step.

        Args:
            documents: A list of document strings.

        Returns:
            A list of lists (dense matrix) of TF-IDF vectors.
        """
        # TODO: Call fit then transform.
        # Hint: return self.fit(documents).transform(documents)
        pass

    def get_feature_names(self) -> list:
        """Return the list of feature (term) names in vocabulary order.

        Returns:
            A list of strings sorted alphabetically, matching the column
            order of the vectors returned by transform().
        """
        # TODO: Return the vocabulary terms sorted by their index.
        # Hint: sorted(self.vocabulary_, key=self.vocabulary_.get)
        pass
