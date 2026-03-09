"""
Tests for Attention from Scratch (Exercise 03).
"""

import unittest
import torch
from .exercise import (
    scaled_dot_product_attention,
    create_causal_mask,
    multi_head_split,
    multi_head_merge,
    multi_head_attention,
    attention_patterns,
)


class TestScaledDotProductAttention(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.batch, self.seq_q, self.seq_k, self.d_k, self.d_v = 2, 4, 6, 8, 8
        self.Q = torch.randn(self.batch, self.seq_q, self.d_k)
        self.K = torch.randn(self.batch, self.seq_k, self.d_k)
        self.V = torch.randn(self.batch, self.seq_k, self.d_v)

    def test_returns_not_none(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        self.assertIsNotNone(result, "scaled_dot_product_attention returned None — not yet implemented")

    def test_has_required_keys(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("output", result)
        self.assertIn("weights", result)

    def test_output_shape(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["output"].shape, (self.batch, self.seq_q, self.d_v))

    def test_weights_shape(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["weights"].shape, (self.batch, self.seq_q, self.seq_k))

    def test_weights_sum_to_one(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        if result is None:
            self.skipTest("Not implemented")
        row_sums = result["weights"].sum(dim=-1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-5))

    def test_weights_non_negative(self):
        result = scaled_dot_product_attention(self.Q, self.K, self.V)
        if result is None:
            self.skipTest("Not implemented")
        self.assertTrue((result["weights"] >= 0).all())

    def test_mask_zeros_future(self):
        # Use square attention with causal mask
        Q = torch.randn(1, 4, 8)
        K = torch.randn(1, 4, 8)
        V = torch.randn(1, 4, 8)
        mask = torch.triu(torch.ones(4, 4), diagonal=1).bool()
        result = scaled_dot_product_attention(Q, K, V, mask=mask)
        if result is None:
            self.skipTest("Not implemented")
        # After masking, weights for future positions should be ~0
        weights = result["weights"][0]
        for i in range(4):
            for j in range(i + 1, 4):
                self.assertAlmostEqual(weights[i, j].item(), 0.0, places=5)


class TestCreateCausalMask(unittest.TestCase):
    def test_returns_not_none(self):
        result = create_causal_mask(4)
        self.assertIsNotNone(result, "create_causal_mask returned None — not yet implemented")

    def test_shape(self):
        result = create_causal_mask(4)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result.shape, (4, 4))

    def test_dtype(self):
        result = create_causal_mask(4)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result.dtype, torch.bool)

    def test_diagonal_not_masked(self):
        result = create_causal_mask(4)
        if result is None:
            self.skipTest("Not implemented")
        for i in range(4):
            self.assertFalse(result[i, i].item())

    def test_upper_triangle_masked(self):
        result = create_causal_mask(4)
        if result is None:
            self.skipTest("Not implemented")
        for i in range(4):
            for j in range(i + 1, 4):
                self.assertTrue(result[i, j].item())

    def test_lower_triangle_not_masked(self):
        result = create_causal_mask(4)
        if result is None:
            self.skipTest("Not implemented")
        for i in range(1, 4):
            for j in range(i):
                self.assertFalse(result[i, j].item())


class TestMultiHeadSplit(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.batch, self.seq, self.d_model, self.n_heads = 2, 5, 16, 4
        self.x = torch.randn(self.batch, self.seq, self.d_model)

    def test_returns_not_none(self):
        result = multi_head_split(self.x, self.n_heads)
        self.assertIsNotNone(result, "multi_head_split returned None — not yet implemented")

    def test_shape(self):
        result = multi_head_split(self.x, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        d_head = self.d_model // self.n_heads
        self.assertEqual(result.shape, (self.batch, self.n_heads, self.seq, d_head))

    def test_values_preserved(self):
        result = multi_head_split(self.x, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        # First head should contain the first d_head features
        d_head = self.d_model // self.n_heads
        self.assertTrue(torch.equal(result[:, 0, :, :], self.x[:, :, :d_head]))


class TestMultiHeadMerge(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.batch, self.n_heads, self.seq, self.d_head = 2, 4, 5, 4
        self.x = torch.randn(self.batch, self.n_heads, self.seq, self.d_head)

    def test_returns_not_none(self):
        result = multi_head_merge(self.x)
        self.assertIsNotNone(result, "multi_head_merge returned None — not yet implemented")

    def test_shape(self):
        result = multi_head_merge(self.x)
        if result is None:
            self.skipTest("Not implemented")
        d_model = self.n_heads * self.d_head
        self.assertEqual(result.shape, (self.batch, self.seq, d_model))

    def test_split_merge_roundtrip(self):
        """split then merge should be identity"""
        original = torch.randn(2, 5, 16)
        split = multi_head_split(original, 4)
        if split is None:
            self.skipTest("multi_head_split not implemented")
        merged = multi_head_merge(split)
        if merged is None:
            self.skipTest("multi_head_merge not implemented")
        self.assertTrue(torch.allclose(merged, original, atol=1e-6))


class TestMultiHeadAttention(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.batch, self.seq, self.d_model, self.n_heads = 2, 6, 16, 4
        self.Q = torch.randn(self.batch, self.seq, self.d_model)
        self.K = torch.randn(self.batch, self.seq, self.d_model)
        self.V = torch.randn(self.batch, self.seq, self.d_model)

    def test_returns_not_none(self):
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads)
        self.assertIsNotNone(result, "multi_head_attention returned None — not yet implemented")

    def test_has_required_keys(self):
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("output", result)
        self.assertIn("weights", result)

    def test_output_shape(self):
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["output"].shape, (self.batch, self.seq, self.d_model))

    def test_weights_shape(self):
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(
            result["weights"].shape,
            (self.batch, self.n_heads, self.seq, self.seq),
        )

    def test_weights_sum_to_one(self):
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads)
        if result is None:
            self.skipTest("Not implemented")
        row_sums = result["weights"].sum(dim=-1)
        self.assertTrue(torch.allclose(row_sums, torch.ones_like(row_sums), atol=1e-5))

    def test_with_causal_mask(self):
        mask = torch.triu(torch.ones(self.seq, self.seq), diagonal=1).bool()
        result = multi_head_attention(self.Q, self.K, self.V, self.n_heads, mask=mask)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["output"].shape, (self.batch, self.seq, self.d_model))


class TestAttentionPatterns(unittest.TestCase):
    def setUp(self):
        self.seq_len = 8

    def test_returns_not_none(self):
        result = attention_patterns(self.seq_len)
        self.assertIsNotNone(result, "attention_patterns returned None — not yet implemented")

    def test_has_required_keys(self):
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        for key in ("causal", "sliding_window", "prefix"):
            self.assertIn(key, result)

    def test_causal_shape_and_dtype(self):
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["causal"].shape, (self.seq_len, self.seq_len))
        self.assertEqual(result["causal"].dtype, torch.bool)

    def test_causal_matches_create_causal(self):
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        expected = torch.triu(torch.ones(self.seq_len, self.seq_len), diagonal=1).bool()
        self.assertTrue(torch.equal(result["causal"], expected))

    def test_sliding_window_shape(self):
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["sliding_window"].shape, (self.seq_len, self.seq_len))

    def test_sliding_window_self_attention(self):
        """Each token should attend to itself (diagonal not masked)."""
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        for i in range(self.seq_len):
            self.assertFalse(result["sliding_window"][i, i].item())

    def test_sliding_window_blocks_future(self):
        """Future tokens should be masked in sliding window."""
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        for i in range(self.seq_len):
            for j in range(i + 1, self.seq_len):
                self.assertTrue(result["sliding_window"][i, j].item())

    def test_sliding_window_blocks_distant_past(self):
        """Tokens more than 2 positions in the past should be masked."""
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        # Token 5 should NOT attend to token 2 (distance = 3 > 2)
        self.assertTrue(result["sliding_window"][5, 2].item())
        # Token 5 SHOULD attend to token 3 (distance = 2)
        self.assertFalse(result["sliding_window"][5, 3].item())

    def test_prefix_shape(self):
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["prefix"].shape, (self.seq_len, self.seq_len))

    def test_prefix_tokens_attend_to_all(self):
        """First seq_len//4 tokens should attend to all positions."""
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        prefix_len = self.seq_len // 4  # 2
        for i in range(prefix_len):
            self.assertFalse(result["prefix"][i].any().item())

    def test_prefix_non_prefix_is_causal(self):
        """Non-prefix tokens should have causal masking (for non-prefix columns)."""
        result = attention_patterns(self.seq_len)
        if result is None:
            self.skipTest("Not implemented")
        prefix_len = self.seq_len // 4  # 2
        # Non-prefix tokens should mask future tokens
        for i in range(prefix_len, self.seq_len):
            for j in range(i + 1, self.seq_len):
                self.assertTrue(result["prefix"][i, j].item())


if __name__ == "__main__":
    unittest.main()
