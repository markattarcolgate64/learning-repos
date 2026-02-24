"""
Tests for TF-IDF Vectorizer.

Run with:
    python -m unittest 08_tf_idf_vectorizer.test_exercise -v
"""

import unittest
import math
from .exercise import TfidfVectorizer


class TestTfidfVectorizer(unittest.TestCase):
    """Comprehensive tests for the TfidfVectorizer."""

    # ------------------------------------------------------------------
    # Shared small corpus used across many tests
    # ------------------------------------------------------------------

    CORPUS = ["the cat sat", "the cat", "the dog sat"]

    # ------------------------------------------------------------------
    # 1. Vocabulary: correct set of terms extracted after fit
    # ------------------------------------------------------------------

    def test_vocabulary_terms(self):
        """fit() should build a vocabulary containing exactly the unique terms."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        expected_terms = {"the", "cat", "sat", "dog"}
        self.assertEqual(set(vec.vocabulary_.keys()), expected_terms)

    # ------------------------------------------------------------------
    # 2. get_feature_names: returns sorted list
    # ------------------------------------------------------------------

    def test_get_feature_names_sorted(self):
        """get_feature_names should return terms sorted alphabetically."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        names = vec.get_feature_names()
        self.assertEqual(names, sorted(names))
        self.assertEqual(names, ["cat", "dog", "sat", "the"])

    # ------------------------------------------------------------------
    # 3. TF calculation: verify on known small example
    # ------------------------------------------------------------------

    def test_tf_values(self):
        """TF for 'cat' in 'the cat sat' should be 1/3."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        matrix = vec.transform(["the cat sat"])
        feature_names = vec.get_feature_names()
        cat_idx = feature_names.index("cat")
        # TF("cat", "the cat sat") = 1/3
        # TF-IDF = TF * IDF; we verify TF portion indirectly via the ratio
        # "cat" appears in 2/3 docs, "the" appears in 3/3 docs
        # IDF("cat") = log(3/2) + 1, IDF("the") = log(3/3) + 1 = 1.0
        the_idx = feature_names.index("the")
        expected_tf_cat = 1.0 / 3.0
        expected_tf_the = 1.0 / 3.0
        idf_cat = math.log(3 / 2) + 1
        idf_the = math.log(3 / 3) + 1  # = 1.0
        self.assertAlmostEqual(matrix[0][cat_idx], expected_tf_cat * idf_cat, places=6)
        self.assertAlmostEqual(matrix[0][the_idx], expected_tf_the * idf_the, places=6)

    # ------------------------------------------------------------------
    # 4. IDF calculation: common terms get lower IDF than rare terms
    # ------------------------------------------------------------------

    def test_idf_ordering(self):
        """'the' (in all 3 docs) should have lower IDF than 'dog' (in 1 doc)."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        self.assertLess(vec.idf_["the"], vec.idf_["dog"])
        # "the" appears in all docs -> IDF = log(3/3) + 1 = 1.0
        self.assertAlmostEqual(vec.idf_["the"], math.log(3 / 3) + 1, places=6)
        # "dog" appears in 1 doc -> IDF = log(3/1) + 1
        self.assertAlmostEqual(vec.idf_["dog"], math.log(3 / 1) + 1, places=6)

    # ------------------------------------------------------------------
    # 5. TF-IDF scores: manual calculation verification
    # ------------------------------------------------------------------

    def test_tfidf_manual_calculation(self):
        """Verify full TF-IDF scores against hand-computed values."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        matrix = vec.transform(self.CORPUS)
        names = vec.get_feature_names()

        N = 3
        # Document 0: "the cat sat" -> tokens: [the, cat, sat], total=3
        # df: cat=2, dog=1, sat=2, the=3
        doc0 = matrix[0]
        for term, tf_count, df in [("cat", 1, 2), ("dog", 0, 1),
                                    ("sat", 1, 2), ("the", 1, 3)]:
            idx = names.index(term)
            total_terms = 3
            tf = tf_count / total_terms
            idf = math.log(N / df) + 1
            expected = tf * idf
            self.assertAlmostEqual(doc0[idx], expected, places=6,
                                   msg=f"TF-IDF mismatch for '{term}' in doc 0")

    # ------------------------------------------------------------------
    # 6. max_features limits vocabulary size
    # ------------------------------------------------------------------

    def test_max_features(self):
        """Setting max_features should limit the vocabulary to top-N by df."""
        vec = TfidfVectorizer(max_features=2)
        vec.fit(self.CORPUS)
        self.assertEqual(len(vec.vocabulary_), 2)
        # top-2 by df: "the" (df=3) and one of "cat"/"sat" (df=2 each)
        self.assertIn("the", vec.vocabulary_)
        matrix = vec.transform(["the cat"])
        self.assertEqual(len(matrix[0]), 2)

    # ------------------------------------------------------------------
    # 7. Lowercasing: "The" and "the" treated as same
    # ------------------------------------------------------------------

    def test_lowercasing(self):
        """With lowercase=True (default), 'The' and 'the' should be the same token."""
        vec = TfidfVectorizer(lowercase=True)
        vec.fit(["The Cat", "the cat"])
        self.assertIn("the", vec.vocabulary_)
        self.assertIn("cat", vec.vocabulary_)
        self.assertNotIn("The", vec.vocabulary_)
        self.assertNotIn("Cat", vec.vocabulary_)

    # ------------------------------------------------------------------
    # 8. fit_transform equals fit then transform
    # ------------------------------------------------------------------

    def test_fit_transform_equals_fit_then_transform(self):
        """fit_transform(docs) should produce the same result as fit(docs).transform(docs)."""
        corpus = self.CORPUS

        vec1 = TfidfVectorizer()
        result1 = vec1.fit_transform(corpus)

        vec2 = TfidfVectorizer()
        vec2.fit(corpus)
        result2 = vec2.transform(corpus)

        self.assertEqual(len(result1), len(result2))
        for row_a, row_b in zip(result1, result2):
            for val_a, val_b in zip(row_a, row_b):
                self.assertAlmostEqual(val_a, val_b, places=10)

    # ------------------------------------------------------------------
    # 9. Transform unseen docs: terms not in vocab get 0
    # ------------------------------------------------------------------

    def test_unseen_terms_get_zero(self):
        """Terms not in the training vocabulary should get TF-IDF score of 0."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        matrix = vec.transform(["elephant runs fast"])
        # None of these terms are in the vocabulary
        for val in matrix[0]:
            self.assertAlmostEqual(val, 0.0)

    # ------------------------------------------------------------------
    # 10. Empty tokens from punctuation-only words handled
    # ------------------------------------------------------------------

    def test_punctuation_only_tokens(self):
        """Punctuation-only tokens should be stripped and discarded."""
        vec = TfidfVectorizer()
        vec.fit(["hello ... world", "hello !!! test"])
        # "..." and "!!!" should not appear in vocabulary
        self.assertNotIn("...", vec.vocabulary_)
        self.assertNotIn("!!!", vec.vocabulary_)
        self.assertNotIn("", vec.vocabulary_)
        self.assertIn("hello", vec.vocabulary_)

    # ------------------------------------------------------------------
    # Extra: output shape is correct
    # ------------------------------------------------------------------

    def test_transform_output_shape(self):
        """transform should return n_docs rows, each with n_vocab columns."""
        vec = TfidfVectorizer()
        vec.fit(self.CORPUS)
        matrix = vec.transform(self.CORPUS)
        self.assertEqual(len(matrix), len(self.CORPUS))
        vocab_size = len(vec.vocabulary_)
        for row in matrix:
            self.assertEqual(len(row), vocab_size)


if __name__ == "__main__":
    unittest.main()
