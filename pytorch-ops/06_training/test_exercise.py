"""
Tests for Exercise 06: Training at Scale
"""

import unittest
import torch
import torch.nn as nn
import math

from .exercise import (
    gradient_clipping_demo,
    learning_rate_schedules,
    gradient_accumulation_training,
    mixed_precision_concepts,
    weight_decay_comparison,
    cosine_annealing_with_restarts,
)


class TestGradientClipping(unittest.TestCase):
    """Tests for gradient_clipping_demo"""

    def setUp(self):
        torch.manual_seed(42)
        self.model = nn.Linear(4, 1)
        # Use large values to ensure gradients exceed max_norm
        self.X = torch.randn(32, 4) * 10.0
        self.y = torch.randn(32, 1) * 10.0

    def test_returns_not_none(self):
        result = gradient_clipping_demo(self.model, self.X, self.y, max_norm=1.0)
        self.assertIsNotNone(result, "gradient_clipping_demo returned None")

    def test_returns_dict_with_expected_keys(self):
        result = gradient_clipping_demo(self.model, self.X, self.y, max_norm=1.0)
        if result is None:
            self.skipTest("gradient_clipping_demo returned None")
        self.assertIn('grad_norm_before', result)
        self.assertIn('grad_norm_after', result)
        self.assertIn('loss', result)

    def test_grad_norm_after_is_clipped(self):
        result = gradient_clipping_demo(self.model, self.X, self.y, max_norm=1.0)
        if result is None:
            self.skipTest("gradient_clipping_demo returned None")
        self.assertLessEqual(result['grad_norm_after'], 1.0 + 1e-5,
                             "Gradient norm after clipping should be <= max_norm")

    def test_grad_norm_before_exceeds_max(self):
        """With large inputs, gradient norm before clipping should exceed 1.0."""
        result = gradient_clipping_demo(self.model, self.X, self.y, max_norm=1.0)
        if result is None:
            self.skipTest("gradient_clipping_demo returned None")
        self.assertGreater(result['grad_norm_before'], 1.0,
                           "With large inputs, grad norm before clipping should exceed max_norm")

    def test_loss_is_positive(self):
        result = gradient_clipping_demo(self.model, self.X, self.y, max_norm=1.0)
        if result is None:
            self.skipTest("gradient_clipping_demo returned None")
        self.assertGreater(result['loss'], 0.0)


class TestLearningRateSchedules(unittest.TestCase):
    """Tests for learning_rate_schedules"""

    def test_returns_not_none(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        self.assertIsNotNone(result, "learning_rate_schedules returned None")

    def test_returns_correct_keys(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        self.assertIn('cosine', result)
        self.assertIn('linear', result)

    def test_correct_length(self):
        result = learning_rate_schedules(total_steps=500, warmup_steps=50)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        self.assertEqual(len(result['cosine']), 500)
        self.assertEqual(len(result['linear']), 500)

    def test_warmup_starts_at_zero(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        self.assertAlmostEqual(result['cosine'][0], 0.0, places=6)
        self.assertAlmostEqual(result['linear'][0], 0.0, places=6)

    def test_peak_lr_at_warmup_end(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        # At step=warmup_steps, LR should be at or very near peak
        peak_lr = 0.001
        self.assertAlmostEqual(result['cosine'][100], peak_lr, places=5)
        self.assertAlmostEqual(result['linear'][100], peak_lr, places=5)

    def test_cosine_ends_near_zero(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        self.assertAlmostEqual(result['cosine'][-1], 0.0, places=5)

    def test_linear_ends_near_zero(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        self.assertAlmostEqual(result['linear'][-1], 0.0, places=5)

    def test_warmup_is_increasing(self):
        result = learning_rate_schedules(total_steps=1000, warmup_steps=100)
        if result is None:
            self.skipTest("learning_rate_schedules returned None")
        for i in range(1, 100):
            self.assertGreaterEqual(result['cosine'][i], result['cosine'][i - 1])


class TestGradientAccumulation(unittest.TestCase):
    """Tests for gradient_accumulation_training"""

    def setUp(self):
        torch.manual_seed(42)
        self.model = nn.Linear(4, 1)
        self.batches = [(torch.randn(8, 4), torch.randn(8, 1)) for _ in range(16)]

    def test_returns_not_none(self):
        result = gradient_accumulation_training(self.model, self.batches,
                                                accumulation_steps=4)
        self.assertIsNotNone(result, "gradient_accumulation_training returned None")

    def test_returns_correct_keys(self):
        result = gradient_accumulation_training(self.model, self.batches,
                                                accumulation_steps=4)
        if result is None:
            self.skipTest("gradient_accumulation_training returned None")
        self.assertIn('losses', result)
        self.assertIn('n_optimizer_steps', result)

    def test_correct_number_of_optimizer_steps(self):
        result = gradient_accumulation_training(self.model, self.batches,
                                                accumulation_steps=4)
        if result is None:
            self.skipTest("gradient_accumulation_training returned None")
        expected_steps = len(self.batches) // 4
        self.assertEqual(result['n_optimizer_steps'], expected_steps)

    def test_fewer_optimizer_steps_with_larger_accumulation(self):
        torch.manual_seed(42)
        model1 = nn.Linear(4, 1)
        torch.manual_seed(42)
        model2 = nn.Linear(4, 1)
        r1 = gradient_accumulation_training(model1, self.batches, accumulation_steps=2)
        r2 = gradient_accumulation_training(model2, self.batches, accumulation_steps=8)
        if r1 is None or r2 is None:
            self.skipTest("gradient_accumulation_training returned None")
        self.assertGreater(r1['n_optimizer_steps'], r2['n_optimizer_steps'])

    def test_losses_list_length(self):
        result = gradient_accumulation_training(self.model, self.batches,
                                                accumulation_steps=4)
        if result is None:
            self.skipTest("gradient_accumulation_training returned None")
        self.assertEqual(len(result['losses']), result['n_optimizer_steps'])


class TestMixedPrecisionConcepts(unittest.TestCase):
    """Tests for mixed_precision_concepts"""

    def test_returns_not_none(self):
        result = mixed_precision_concepts()
        self.assertIsNotNone(result, "mixed_precision_concepts returned None")

    def test_float32_size(self):
        result = mixed_precision_concepts()
        if result is None:
            self.skipTest("mixed_precision_concepts returned None")
        self.assertEqual(result['float32_size'], 4)

    def test_float16_size(self):
        result = mixed_precision_concepts()
        if result is None:
            self.skipTest("mixed_precision_concepts returned None")
        self.assertEqual(result['float16_size'], 2)

    def test_bfloat16_size(self):
        result = mixed_precision_concepts()
        if result is None:
            self.skipTest("mixed_precision_concepts returned None")
        self.assertEqual(result['bfloat16_size'], 2)

    def test_bfloat16_has_larger_range(self):
        result = mixed_precision_concepts()
        if result is None:
            self.skipTest("mixed_precision_concepts returned None")
        self.assertGreater(result['bfloat16_max'], result['float16_max'],
                           "bfloat16 should have a larger max value than float16")


class TestWeightDecayComparison(unittest.TestCase):
    """Tests for weight_decay_comparison"""

    def setUp(self):
        torch.manual_seed(42)
        self.X = torch.randn(64, 4)
        self.y = torch.randn(64, 1)

    def test_returns_not_none(self):
        result = weight_decay_comparison(self.X, self.y, steps=200)
        self.assertIsNotNone(result, "weight_decay_comparison returned None")

    def test_returns_correct_keys(self):
        result = weight_decay_comparison(self.X, self.y, steps=200)
        if result is None:
            self.skipTest("weight_decay_comparison returned None")
        self.assertIn('no_decay_weights', result)
        self.assertIn('with_decay_weights', result)
        self.assertIn('no_decay_norm', result)
        self.assertIn('with_decay_norm', result)

    def test_weight_decay_produces_smaller_norm(self):
        result = weight_decay_comparison(self.X, self.y, steps=200)
        if result is None:
            self.skipTest("weight_decay_comparison returned None")
        self.assertLess(result['with_decay_norm'], result['no_decay_norm'],
                        "Weight decay should produce smaller weight norms")

    def test_weights_are_tensors(self):
        result = weight_decay_comparison(self.X, self.y, steps=200)
        if result is None:
            self.skipTest("weight_decay_comparison returned None")
        self.assertIsInstance(result['no_decay_weights'], torch.Tensor)
        self.assertIsInstance(result['with_decay_weights'], torch.Tensor)


class TestCosineAnnealingWithRestarts(unittest.TestCase):
    """Tests for cosine_annealing_with_restarts"""

    def test_returns_not_none(self):
        result = cosine_annealing_with_restarts(total_steps=400, T_0=100)
        self.assertIsNotNone(result, "cosine_annealing_with_restarts returned None")

    def test_correct_length(self):
        result = cosine_annealing_with_restarts(total_steps=400, T_0=100)
        if result is None:
            self.skipTest("cosine_annealing_with_restarts returned None")
        self.assertEqual(len(result), 400)

    def test_starts_at_peak(self):
        result = cosine_annealing_with_restarts(total_steps=400, T_0=100)
        if result is None:
            self.skipTest("cosine_annealing_with_restarts returned None")
        self.assertAlmostEqual(result[0], 0.001, places=5)

    def test_restarts_spike_back_up(self):
        """LR at step T_0 should be back at peak (restart)."""
        result = cosine_annealing_with_restarts(total_steps=400, T_0=100)
        if result is None:
            self.skipTest("cosine_annealing_with_restarts returned None")
        # At step 100, 200, 300 the LR should restart to peak
        self.assertAlmostEqual(result[100], 0.001, places=5)
        self.assertAlmostEqual(result[200], 0.001, places=5)

    def test_decays_within_period(self):
        """LR should decrease within each restart period."""
        result = cosine_annealing_with_restarts(total_steps=400, T_0=100)
        if result is None:
            self.skipTest("cosine_annealing_with_restarts returned None")
        # Middle of first period should be less than peak
        self.assertLess(result[50], 0.001)


if __name__ == '__main__':
    unittest.main()
