"""
Tests for Exercise 07: Inference & Generation
"""

import unittest
import torch
import torch.nn.functional as F

from .exercise import (
    temperature_scaling,
    top_k_filtering,
    top_p_filtering,
    greedy_decode,
    kv_cache_attention,
    sample_with_strategy,
)


class TestTemperatureScaling(unittest.TestCase):
    """Tests for temperature_scaling"""

    def setUp(self):
        torch.manual_seed(42)
        self.logits = torch.randn(10)

    def test_returns_not_none(self):
        result = temperature_scaling(self.logits, temperature=1.0)
        self.assertIsNotNone(result, "temperature_scaling returned None")

    def test_returns_correct_keys(self):
        result = temperature_scaling(self.logits, temperature=1.0)
        if result is None:
            self.skipTest("temperature_scaling returned None")
        self.assertIn('scaled_logits', result)
        self.assertIn('probs', result)

    def test_preserves_shape(self):
        result = temperature_scaling(self.logits, temperature=0.5)
        if result is None:
            self.skipTest("temperature_scaling returned None")
        self.assertEqual(result['scaled_logits'].shape, self.logits.shape)
        self.assertEqual(result['probs'].shape, self.logits.shape)

    def test_probs_sum_to_one(self):
        result = temperature_scaling(self.logits, temperature=0.5)
        if result is None:
            self.skipTest("temperature_scaling returned None")
        self.assertAlmostEqual(result['probs'].sum().item(), 1.0, places=5)

    def test_low_temp_is_peaky(self):
        """Low temperature should produce a more peaked distribution."""
        low = temperature_scaling(self.logits, temperature=0.1)
        high = temperature_scaling(self.logits, temperature=10.0)
        if low is None or high is None:
            self.skipTest("temperature_scaling returned None")
        # Max prob under low temp should be higher than under high temp
        self.assertGreater(low['probs'].max().item(), high['probs'].max().item())

    def test_high_temp_is_more_uniform(self):
        """High temperature should produce more uniform distribution."""
        high = temperature_scaling(self.logits, temperature=100.0)
        if high is None:
            self.skipTest("temperature_scaling returned None")
        # All probs should be close to 1/vocab_size
        expected = 1.0 / len(self.logits)
        for p in high['probs']:
            self.assertAlmostEqual(p.item(), expected, places=1)

    def test_temperature_one_matches_softmax(self):
        result = temperature_scaling(self.logits, temperature=1.0)
        if result is None:
            self.skipTest("temperature_scaling returned None")
        expected = F.softmax(self.logits, dim=-1)
        self.assertTrue(torch.allclose(result['probs'], expected, atol=1e-5))


class TestTopKFiltering(unittest.TestCase):
    """Tests for top_k_filtering"""

    def setUp(self):
        self.logits = torch.tensor([1.0, 5.0, 3.0, 7.0, 2.0, 6.0, 4.0])

    def test_returns_not_none(self):
        result = top_k_filtering(self.logits, k=3)
        self.assertIsNotNone(result, "top_k_filtering returned None")

    def test_keeps_exactly_k_values(self):
        result = top_k_filtering(self.logits, k=3)
        if result is None:
            self.skipTest("top_k_filtering returned None")
        finite_count = (result > -float('inf')).sum().item()
        self.assertEqual(finite_count, 3)

    def test_preserves_top_k_values(self):
        result = top_k_filtering(self.logits, k=3)
        if result is None:
            self.skipTest("top_k_filtering returned None")
        # Top 3 values are 7.0, 6.0, 5.0 at indices 3, 5, 1
        self.assertEqual(result[3].item(), 7.0)
        self.assertEqual(result[5].item(), 6.0)
        self.assertEqual(result[1].item(), 5.0)

    def test_non_top_k_are_neg_inf(self):
        result = top_k_filtering(self.logits, k=2)
        if result is None:
            self.skipTest("top_k_filtering returned None")
        # Only indices 3 (7.0) and 5 (6.0) should remain
        for i in [0, 1, 2, 4, 6]:
            self.assertEqual(result[i].item(), -float('inf'))

    def test_preserves_shape(self):
        result = top_k_filtering(self.logits, k=3)
        if result is None:
            self.skipTest("top_k_filtering returned None")
        self.assertEqual(result.shape, self.logits.shape)


class TestTopPFiltering(unittest.TestCase):
    """Tests for top_p_filtering"""

    def setUp(self):
        # Create logits where probs are clearly ordered
        self.logits = torch.tensor([1.0, 5.0, 2.0, 8.0, 0.5])

    def test_returns_not_none(self):
        result = top_p_filtering(self.logits, p=0.9)
        self.assertIsNotNone(result, "top_p_filtering returned None")

    def test_preserves_shape(self):
        result = top_p_filtering(self.logits, p=0.9)
        if result is None:
            self.skipTest("top_p_filtering returned None")
        self.assertEqual(result.shape, self.logits.shape)

    def test_always_keeps_top1(self):
        """Even with very small p, the top token should be kept."""
        result = top_p_filtering(self.logits, p=0.01)
        if result is None:
            self.skipTest("top_p_filtering returned None")
        top_idx = self.logits.argmax().item()
        self.assertGreater(result[top_idx].item(), -float('inf'))

    def test_p_one_keeps_all(self):
        """p=1.0 should keep all tokens."""
        result = top_p_filtering(self.logits, p=1.0)
        if result is None:
            self.skipTest("top_p_filtering returned None")
        finite_count = (result > -float('inf')).sum().item()
        self.assertEqual(finite_count, len(self.logits))

    def test_small_p_keeps_fewer(self):
        """Smaller p should keep fewer tokens."""
        r_small = top_p_filtering(self.logits, p=0.5)
        r_large = top_p_filtering(self.logits, p=0.99)
        if r_small is None or r_large is None:
            self.skipTest("top_p_filtering returned None")
        count_small = (r_small > -float('inf')).sum().item()
        count_large = (r_large > -float('inf')).sum().item()
        self.assertLessEqual(count_small, count_large)


class TestGreedyDecode(unittest.TestCase):
    """Tests for greedy_decode"""

    def _simple_logits_fn(self, token_ids):
        """Returns logits that always favor token (last_token + 1) % 5."""
        vocab_size = 5
        logits = torch.zeros(vocab_size)
        next_token = (token_ids[-1] + 1) % vocab_size
        logits[next_token] = 10.0
        return logits

    def test_returns_not_none(self):
        result = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        self.assertIsNotNone(result, "greedy_decode returned None")

    def test_returns_correct_keys(self):
        result = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        if result is None:
            self.skipTest("greedy_decode returned None")
        self.assertIn('token_ids', result)
        self.assertIn('length', result)

    def test_starts_with_start_token(self):
        result = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        if result is None:
            self.skipTest("greedy_decode returned None")
        self.assertEqual(result['token_ids'][0], 0)

    def test_deterministic_output(self):
        """Greedy decoding should always produce the same output."""
        r1 = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        r2 = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        if r1 is None or r2 is None:
            self.skipTest("greedy_decode returned None")
        self.assertEqual(r1['token_ids'], r2['token_ids'])

    def test_respects_max_len(self):
        result = greedy_decode(self._simple_logits_fn, start_token=0, max_len=7)
        if result is None:
            self.skipTest("greedy_decode returned None")
        self.assertLessEqual(result['length'], 7)

    def test_stops_at_eos(self):
        """Should stop when eos_token is generated."""
        def eos_logits_fn(token_ids):
            logits = torch.zeros(5)
            if len(token_ids) >= 3:
                logits[2] = 10.0  # eos token
            else:
                logits[1] = 10.0
            return logits

        result = greedy_decode(eos_logits_fn, start_token=0, max_len=10, eos_token=2)
        if result is None:
            self.skipTest("greedy_decode returned None")
        self.assertLessEqual(result['length'], 10)
        # The last token should be eos or sequence stopped
        self.assertIn(2, result['token_ids'])

    def test_length_matches_token_ids(self):
        result = greedy_decode(self._simple_logits_fn, start_token=0, max_len=5)
        if result is None:
            self.skipTest("greedy_decode returned None")
        self.assertEqual(result['length'], len(result['token_ids']))


class TestKVCacheAttention(unittest.TestCase):
    """Tests for kv_cache_attention"""

    def setUp(self):
        torch.manual_seed(42)
        self.batch, self.heads, self.d_k = 2, 4, 16

    def test_returns_not_none(self):
        Q = torch.randn(self.batch, self.heads, 1, self.d_k)
        K = torch.randn(self.batch, self.heads, 1, self.d_k)
        V = torch.randn(self.batch, self.heads, 1, self.d_k)
        result = kv_cache_attention(Q, K, V)
        self.assertIsNotNone(result, "kv_cache_attention returned None")

    def test_returns_correct_keys(self):
        Q = torch.randn(self.batch, self.heads, 1, self.d_k)
        K = torch.randn(self.batch, self.heads, 1, self.d_k)
        V = torch.randn(self.batch, self.heads, 1, self.d_k)
        result = kv_cache_attention(Q, K, V)
        if result is None:
            self.skipTest("kv_cache_attention returned None")
        self.assertIn('output', result)
        self.assertIn('K_cache', result)
        self.assertIn('V_cache', result)

    def test_no_cache_shapes(self):
        """Without cache, output should match query sequence length."""
        Q = torch.randn(self.batch, self.heads, 3, self.d_k)
        K = torch.randn(self.batch, self.heads, 3, self.d_k)
        V = torch.randn(self.batch, self.heads, 3, self.d_k)
        result = kv_cache_attention(Q, K, V)
        if result is None:
            self.skipTest("kv_cache_attention returned None")
        self.assertEqual(result['output'].shape,
                         (self.batch, self.heads, 3, self.d_k))

    def test_cache_grows_in_seq_dimension(self):
        """KV cache should grow as new tokens are processed."""
        K1 = torch.randn(self.batch, self.heads, 3, self.d_k)
        V1 = torch.randn(self.batch, self.heads, 3, self.d_k)
        Q1 = torch.randn(self.batch, self.heads, 3, self.d_k)
        r1 = kv_cache_attention(Q1, K1, V1)
        if r1 is None:
            self.skipTest("kv_cache_attention returned None")

        # Now add 1 more token using cache
        K2 = torch.randn(self.batch, self.heads, 1, self.d_k)
        V2 = torch.randn(self.batch, self.heads, 1, self.d_k)
        Q2 = torch.randn(self.batch, self.heads, 1, self.d_k)
        r2 = kv_cache_attention(Q2, K2, V2,
                                K_cache=r1['K_cache'], V_cache=r1['V_cache'])
        if r2 is None:
            self.skipTest("kv_cache_attention returned None")

        # Cache should now have seq_len = 3 + 1 = 4
        self.assertEqual(r2['K_cache'].shape[-2], 4)
        self.assertEqual(r2['V_cache'].shape[-2], 4)

    def test_output_shape_with_cache(self):
        """Output seq dim should match query, not cache."""
        K_cache = torch.randn(self.batch, self.heads, 5, self.d_k)
        V_cache = torch.randn(self.batch, self.heads, 5, self.d_k)
        Q = torch.randn(self.batch, self.heads, 1, self.d_k)
        K_new = torch.randn(self.batch, self.heads, 1, self.d_k)
        V_new = torch.randn(self.batch, self.heads, 1, self.d_k)
        result = kv_cache_attention(Q, K_new, V_new, K_cache, V_cache)
        if result is None:
            self.skipTest("kv_cache_attention returned None")
        # Output should have seq_len = 1 (matching Q)
        self.assertEqual(result['output'].shape[-2], 1)


class TestSampleWithStrategy(unittest.TestCase):
    """Tests for sample_with_strategy"""

    def setUp(self):
        torch.manual_seed(42)
        self.logits = torch.randn(100)

    def test_returns_not_none_greedy(self):
        result = sample_with_strategy(self.logits, strategy='greedy')
        self.assertIsNotNone(result, "sample_with_strategy returned None")

    def test_greedy_returns_argmax(self):
        result = sample_with_strategy(self.logits, strategy='greedy')
        if result is None:
            self.skipTest("sample_with_strategy returned None")
        expected = self.logits.argmax().item()
        self.assertEqual(result, expected)

    def test_returns_valid_index(self):
        result = sample_with_strategy(self.logits, strategy='sample',
                                      temperature=1.0)
        if result is None:
            self.skipTest("sample_with_strategy returned None")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLess(result, len(self.logits))

    def test_sample_returns_int(self):
        result = sample_with_strategy(self.logits, strategy='sample',
                                      temperature=0.5, top_k=10)
        if result is None:
            self.skipTest("sample_with_strategy returned None")
        self.assertIsInstance(result, int)

    def test_low_temp_sample_favors_argmax(self):
        """With very low temperature, sampling should almost always pick argmax."""
        argmax_idx = self.logits.argmax().item()
        count = 0
        for _ in range(20):
            result = sample_with_strategy(self.logits, strategy='sample',
                                          temperature=0.01)
            if result is None:
                self.skipTest("sample_with_strategy returned None")
            if result == argmax_idx:
                count += 1
        self.assertGreater(count, 15,
                           "Very low temperature should almost always pick argmax")

    def test_top_k_restricts_output(self):
        """With top_k=1, result should always be argmax."""
        result = sample_with_strategy(self.logits, strategy='sample',
                                      temperature=1.0, top_k=1)
        if result is None:
            self.skipTest("sample_with_strategy returned None")
        self.assertEqual(result, self.logits.argmax().item())


if __name__ == '__main__':
    unittest.main()
