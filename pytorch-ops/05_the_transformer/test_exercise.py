"""
Tests for The Transformer (Exercise 05).

All data is synthetic — no external files needed.
"""

import unittest
import torch
import torch.nn as nn

from .exercise import (
    TransformerConfig,
    TransformerBlock,
    MiniTransformer,
    compute_loss,
    count_parameters,
)


class TestTransformerConfig(unittest.TestCase):
    """Tests for TransformerConfig."""

    def _make_config(self):
        try:
            config = TransformerConfig()
            # Check that at least one expected attribute exists
            if not hasattr(config, "vocab_size"):
                return None
            return config
        except TypeError:
            return None

    def test_config_instantiates(self):
        config = self._make_config()
        self.assertIsNotNone(config, "TransformerConfig() returned None or failed — not yet implemented")

    def test_default_vocab_size(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.vocab_size, 1000)

    def test_default_d_model(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.d_model, 64)

    def test_default_n_heads(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.n_heads, 4)

    def test_default_d_ff(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.d_ff, 256)

    def test_default_n_layers(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.n_layers, 2)

    def test_default_max_seq_len(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.max_seq_len, 128)

    def test_default_dropout(self):
        config = self._make_config()
        if config is None:
            self.skipTest("Not yet implemented")
        self.assertAlmostEqual(config.dropout, 0.1)

    def test_custom_values(self):
        try:
            config = TransformerConfig(vocab_size=500, d_model=128)
            if not hasattr(config, "vocab_size"):
                self.skipTest("Not yet implemented")
        except TypeError:
            self.skipTest("Not yet implemented")
        self.assertEqual(config.vocab_size, 500)
        self.assertEqual(config.d_model, 128)


class TestTransformerBlock(unittest.TestCase):
    """Tests for TransformerBlock."""

    def _make_block(self):
        try:
            config = TransformerConfig()
            if not hasattr(config, "vocab_size"):
                return None
            block = TransformerBlock(config)
            # Check if forward is implemented (not just pass)
            x = torch.randn(2, 10, config.d_model)
            out = block(x)
            if out is None:
                return None
            return block, config
        except (TypeError, AttributeError):
            return None

    def test_returns_not_none(self):
        result = self._make_block()
        self.assertIsNotNone(result, "TransformerBlock forward returned None — not yet implemented")

    def test_output_shape(self):
        result = self._make_block()
        if result is None:
            self.skipTest("Not yet implemented")
        block, config = result
        batch, seq_len = 2, 10
        x = torch.randn(batch, seq_len, config.d_model)
        out = block(x)
        self.assertEqual(out.shape, (batch, seq_len, config.d_model))

    def test_with_mask(self):
        result = self._make_block()
        if result is None:
            self.skipTest("Not yet implemented")
        block, config = result
        seq_len = 8
        x = torch.randn(1, seq_len, config.d_model)
        # Causal mask: upper triangle is -inf
        mask = torch.triu(torch.ones(seq_len, seq_len) * float("-inf"), diagonal=1)
        out = block(x, mask=mask)
        self.assertEqual(out.shape, (1, seq_len, config.d_model))

    def test_different_batch_sizes(self):
        result = self._make_block()
        if result is None:
            self.skipTest("Not yet implemented")
        block, config = result
        for batch in [1, 4, 8]:
            x = torch.randn(batch, 6, config.d_model)
            out = block(x)
            self.assertEqual(out.shape[0], batch)


class TestMiniTransformer(unittest.TestCase):
    """Tests for MiniTransformer."""

    def _make_model(self):
        try:
            config = TransformerConfig()
            if not hasattr(config, "vocab_size"):
                return None
            model = MiniTransformer(config)
            token_ids = torch.randint(0, config.vocab_size, (2, 10))
            out = model(token_ids)
            if out is None:
                return None
            return model, config
        except (TypeError, AttributeError):
            return None

    def test_returns_not_none(self):
        result = self._make_model()
        self.assertIsNotNone(result, "MiniTransformer forward returned None — not yet implemented")

    def test_output_shape(self):
        result = self._make_model()
        if result is None:
            self.skipTest("Not yet implemented")
        model, config = result
        batch, seq_len = 3, 12
        token_ids = torch.randint(0, config.vocab_size, (batch, seq_len))
        logits = model(token_ids)
        self.assertEqual(logits.shape, (batch, seq_len, config.vocab_size))

    def test_with_mask(self):
        result = self._make_model()
        if result is None:
            self.skipTest("Not yet implemented")
        model, config = result
        seq_len = 8
        token_ids = torch.randint(0, config.vocab_size, (2, seq_len))
        mask = torch.triu(torch.ones(seq_len, seq_len) * float("-inf"), diagonal=1)
        logits = model(token_ids, mask=mask)
        self.assertEqual(logits.shape, (2, seq_len, config.vocab_size))

    def test_output_is_float(self):
        result = self._make_model()
        if result is None:
            self.skipTest("Not yet implemented")
        model, config = result
        token_ids = torch.randint(0, config.vocab_size, (1, 5))
        logits = model(token_ids)
        self.assertTrue(logits.dtype in (torch.float32, torch.float64))

    def test_eval_mode(self):
        """Model should work in eval mode (no dropout)."""
        result = self._make_model()
        if result is None:
            self.skipTest("Not yet implemented")
        model, config = result
        model.eval()
        token_ids = torch.randint(0, config.vocab_size, (1, 5))
        with torch.no_grad():
            logits = model(token_ids)
        self.assertEqual(logits.shape, (1, 5, config.vocab_size))


class TestComputeLoss(unittest.TestCase):
    """Tests for compute_loss."""

    def test_returns_not_none(self):
        logits = torch.randn(2, 5, 100)
        targets = torch.randint(0, 100, (2, 5))
        loss = compute_loss(logits, targets)
        self.assertIsNotNone(loss, "compute_loss returned None — not yet implemented")

    def test_loss_is_scalar(self):
        logits = torch.randn(2, 5, 100)
        targets = torch.randint(0, 100, (2, 5))
        loss = compute_loss(logits, targets)
        if loss is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(loss.dim(), 0, "Loss should be a scalar (0-dim tensor)")

    def test_loss_is_positive(self):
        logits = torch.randn(4, 8, 50)
        targets = torch.randint(0, 50, (4, 8))
        loss = compute_loss(logits, targets)
        if loss is None:
            self.skipTest("Not yet implemented")
        self.assertGreater(loss.item(), 0.0)

    def test_perfect_prediction_low_loss(self):
        """If logits strongly predict the correct class, loss should be low."""
        batch, seq_len, vocab_size = 2, 4, 10
        targets = torch.randint(0, vocab_size, (batch, seq_len))
        # Create logits that strongly predict the correct targets
        logits = torch.full((batch, seq_len, vocab_size), -10.0)
        for b in range(batch):
            for s in range(seq_len):
                logits[b, s, targets[b, s]] = 10.0
        loss = compute_loss(logits, targets)
        if loss is None:
            self.skipTest("Not yet implemented")
        self.assertLess(loss.item(), 0.1)


class TestCountParameters(unittest.TestCase):
    """Tests for count_parameters."""

    def test_returns_not_none(self):
        model = nn.Linear(10, 5)
        result = count_parameters(model)
        self.assertIsNotNone(result, "count_parameters returned None — not yet implemented")

    def test_linear_layer(self):
        model = nn.Linear(10, 5)  # 10*5 + 5 = 55
        result = count_parameters(model)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result, 55)

    def test_frozen_params_excluded(self):
        model = nn.Linear(10, 5)
        for p in model.parameters():
            p.requires_grad = False
        result = count_parameters(model)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertEqual(result, 0)

    def test_mini_transformer_params(self):
        """Verify count_parameters works on the full model."""
        try:
            config = TransformerConfig()
            if not hasattr(config, "vocab_size"):
                self.skipTest("TransformerConfig not yet implemented")
            model = MiniTransformer(config)
            test_input = torch.randint(0, config.vocab_size, (1, 5))
            out = model(test_input)
            if out is None:
                self.skipTest("MiniTransformer not yet implemented")
        except (TypeError, AttributeError):
            self.skipTest("TransformerConfig or MiniTransformer not yet implemented")
        result = count_parameters(model)
        if result is None:
            self.skipTest("Not yet implemented")
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main()
