"""
Tests for Transformer Building Blocks (Exercise 04).

All data is synthetic — no external files needed.
"""

import unittest
import math
import torch
import torch.nn as nn

from .exercise import (
    token_embedding,
    positional_encoding,
    layer_norm,
    feed_forward_network,
    residual_connection,
    transformer_block_forward,
)


class TestTokenEmbedding(unittest.TestCase):
    """Tests for token_embedding."""

    def test_returns_not_none(self):
        token_ids = torch.randint(0, 100, (2, 10))
        result = token_embedding(100, 32, token_ids)
        self.assertIsNotNone(result, "token_embedding returned None — not yet implemented")

    def test_returns_dict_with_keys(self):
        token_ids = torch.randint(0, 100, (2, 10))
        result = token_embedding(100, 32, token_ids)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIn("embedding_layer", result)
        self.assertIn("embedded", result)

    def test_embedding_layer_type(self):
        token_ids = torch.randint(0, 50, (1, 5))
        result = token_embedding(50, 16, token_ids)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIsInstance(result["embedding_layer"], nn.Embedding)

    def test_output_shape(self):
        batch, seq_len, vocab_size, d_model = 4, 12, 200, 64
        token_ids = torch.randint(0, vocab_size, (batch, seq_len))
        result = token_embedding(vocab_size, d_model, token_ids)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result["embedded"].shape, (batch, seq_len, d_model))

    def test_embedding_vocab_and_dim(self):
        token_ids = torch.randint(0, 80, (2, 6))
        result = token_embedding(80, 24, token_ids)
        if result is None:
            self.skipTest("Not yet implemented")
        emb = result["embedding_layer"]
        self.assertEqual(emb.num_embeddings, 80)
        self.assertEqual(emb.embedding_dim, 24)


class TestPositionalEncoding(unittest.TestCase):
    """Tests for positional_encoding."""

    def test_returns_not_none(self):
        result = positional_encoding(10, 16)
        self.assertIsNotNone(result, "positional_encoding returned None — not yet implemented")

    def test_output_shape(self):
        result = positional_encoding(20, 32)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result.shape, (20, 32))

    def test_first_position_sin_is_zero(self):
        """At position 0, all sin terms should be 0."""
        result = positional_encoding(5, 16)
        if result is None:
            self.skipTest("Not yet implemented")
        # Even dimensions (sin) at position 0 should be sin(0)=0
        even_dims = result[0, 0::2]
        self.assertTrue(torch.allclose(even_dims, torch.zeros_like(even_dims), atol=1e-6))

    def test_first_position_cos_is_one(self):
        """At position 0, all cos terms should be 1."""
        result = positional_encoding(5, 16)
        if result is None:
            self.skipTest("Not yet implemented")
        # Odd dimensions (cos) at position 0 should be cos(0)=1
        odd_dims = result[0, 1::2]
        self.assertTrue(torch.allclose(odd_dims, torch.ones_like(odd_dims), atol=1e-6))

    def test_values_bounded(self):
        """All values should be between -1 and 1."""
        result = positional_encoding(50, 64)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertTrue(result.min() >= -1.0 - 1e-6)
        self.assertTrue(result.max() <= 1.0 + 1e-6)

    def test_different_positions_differ(self):
        """Different positions should have different encodings."""
        result = positional_encoding(10, 32)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertFalse(torch.allclose(result[0], result[1]))


class TestLayerNorm(unittest.TestCase):
    """Tests for layer_norm."""

    def test_returns_not_none(self):
        x = torch.randn(2, 5, 16)
        result = layer_norm(x)
        self.assertIsNotNone(result, "layer_norm returned None — not yet implemented")

    def test_returns_dict_with_keys(self):
        x = torch.randn(2, 5, 16)
        result = layer_norm(x)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIn("output", result)
        self.assertIn("mean", result)
        self.assertIn("std", result)

    def test_output_shape_preserved(self):
        x = torch.randn(3, 8, 32)
        result = layer_norm(x)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result["output"].shape, x.shape)

    def test_output_mean_near_zero(self):
        x = torch.randn(4, 10, 64) * 5 + 3  # offset and scaled
        result = layer_norm(x)
        if result is None:
            self.skipTest("Not yet implemented")
        output = result["output"]
        means = output.mean(dim=-1)
        self.assertTrue(torch.allclose(means, torch.zeros_like(means), atol=1e-4))

    def test_output_var_near_one(self):
        x = torch.randn(4, 10, 64) * 5 + 3
        result = layer_norm(x)
        if result is None:
            self.skipTest("Not yet implemented")
        output = result["output"]
        var = output.var(dim=-1, unbiased=False)
        self.assertTrue(torch.allclose(var, torch.ones_like(var), atol=1e-2))


class TestFeedForwardNetwork(unittest.TestCase):
    """Tests for feed_forward_network."""

    def test_returns_not_none(self):
        result = feed_forward_network(32, 128)
        self.assertIsNotNone(result, "feed_forward_network returned None — not yet implemented")

    def test_returns_sequential(self):
        result = feed_forward_network(32, 128)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIsInstance(result, nn.Sequential)

    def test_output_shape(self):
        ffn = feed_forward_network(32, 128)
        if ffn is None:
            self.skipTest("Not yet implemented")
        x = torch.randn(2, 10, 32)
        out = ffn(x)
        self.assertEqual(out.shape, (2, 10, 32))

    def test_different_d_ff(self):
        ffn = feed_forward_network(16, 64)
        if ffn is None:
            self.skipTest("Not yet implemented")
        x = torch.randn(1, 5, 16)
        out = ffn(x)
        self.assertEqual(out.shape, (1, 5, 16))


class TestResidualConnection(unittest.TestCase):
    """Tests for residual_connection."""

    def test_returns_not_none(self):
        x = torch.randn(2, 5, 16)
        sublayer_out = torch.randn(2, 5, 16)
        result = residual_connection(x, sublayer_out)
        self.assertIsNotNone(result, "residual_connection returned None — not yet implemented")

    def test_output_shape_preserved(self):
        x = torch.randn(3, 8, 32)
        sublayer_out = torch.randn(3, 8, 32)
        result = residual_connection(x, sublayer_out)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result.shape, x.shape)

    def test_output_is_normalized(self):
        x = torch.randn(2, 6, 64) * 5 + 3
        sublayer_out = torch.randn(2, 6, 64) * 2
        result = residual_connection(x, sublayer_out)
        if result is None:
            self.skipTest("Not yet implemented")
        means = result.mean(dim=-1)
        self.assertTrue(torch.allclose(means, torch.zeros_like(means), atol=1e-4))


class TestTransformerBlockForward(unittest.TestCase):
    """Tests for transformer_block_forward."""

    def test_returns_not_none(self):
        x = torch.randn(2, 5, 16)
        identity = lambda t: t
        result = transformer_block_forward(x, identity, identity)
        self.assertIsNotNone(result, "transformer_block_forward returned None — not yet implemented")

    def test_output_shape_preserved(self):
        x = torch.randn(2, 10, 32)
        identity = lambda t: t
        result = transformer_block_forward(x, identity, identity)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result.shape, x.shape)

    def test_sublayers_are_called(self):
        x = torch.randn(1, 4, 16)
        call_count = {"attn": 0, "ff": 0}

        def mock_attn(t):
            call_count["attn"] += 1
            return t * 0.5

        def mock_ff(t):
            call_count["ff"] += 1
            return t * 0.3

        result = transformer_block_forward(x, mock_attn, mock_ff)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(call_count["attn"], 1, "self_attn_fn should be called exactly once")
        self.assertEqual(call_count["ff"], 1, "ff_fn should be called exactly once")

    def test_output_is_tensor(self):
        x = torch.randn(2, 6, 24)
        identity = lambda t: t
        result = transformer_block_forward(x, identity, identity)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIsInstance(result, torch.Tensor)


if __name__ == "__main__":
    unittest.main()
