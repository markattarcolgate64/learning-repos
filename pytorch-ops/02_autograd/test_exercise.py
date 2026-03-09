"""
Tests for Autograd & Computation Graphs (Exercise 02).
"""

import unittest
import torch
import torch.nn as nn
from .exercise import (
    manual_gradient_check,
    gradient_accumulation,
    detach_and_no_grad,
    custom_function,
    higher_order_gradients,
)


class TestManualGradientCheck(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)

    def test_returns_not_none(self):
        result = manual_gradient_check(3.0)
        self.assertIsNotNone(result, "manual_gradient_check returned None — not yet implemented")

    def test_has_required_keys(self):
        result = manual_gradient_check(3.0)
        if result is None:
            self.skipTest("Not implemented")
        for key in ("y", "grad", "analytical"):
            self.assertIn(key, result)

    def test_y_value(self):
        # y = x^3 - 2x^2 + x at x=3: 27 - 18 + 3 = 12
        result = manual_gradient_check(3.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["y"], 12.0, places=4)

    def test_grad_matches_analytical(self):
        result = manual_gradient_check(3.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["grad"], result["analytical"], places=4)

    def test_analytical_value(self):
        # dy/dx = 3x^2 - 4x + 1 at x=3: 27 - 12 + 1 = 16
        result = manual_gradient_check(3.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["analytical"], 16.0, places=4)

    def test_different_input(self):
        # x=0: y=0, grad=1
        result = manual_gradient_check(0.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["y"], 0.0, places=4)
        self.assertAlmostEqual(result["grad"], 1.0, places=4)


class TestGradientAccumulation(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.model = nn.Linear(4, 1)
        # Create 3 small batches
        self.X_batches = [torch.randn(8, 4) for _ in range(3)]
        self.y_batches = [torch.randn(8, 1) for _ in range(3)]

    def test_returns_not_none(self):
        result = gradient_accumulation(self.model, self.X_batches, self.y_batches)
        self.assertIsNotNone(result, "gradient_accumulation returned None — not yet implemented")

    def test_has_required_keys(self):
        result = gradient_accumulation(self.model, self.X_batches, self.y_batches)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("loss", result)
        self.assertIn("grad_norm", result)

    def test_loss_is_positive(self):
        result = gradient_accumulation(self.model, self.X_batches, self.y_batches)
        if result is None:
            self.skipTest("Not implemented")
        self.assertGreater(result["loss"], 0.0)

    def test_grad_norm_is_positive(self):
        result = gradient_accumulation(self.model, self.X_batches, self.y_batches)
        if result is None:
            self.skipTest("Not implemented")
        self.assertGreater(result["grad_norm"], 0.0)


class TestDetachAndNoGrad(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.x = torch.randn(3, 3, requires_grad=True)

    def test_returns_not_none(self):
        result = detach_and_no_grad(self.x)
        self.assertIsNotNone(result, "detach_and_no_grad returned None — not yet implemented")

    def test_has_required_keys(self):
        result = detach_and_no_grad(self.x)
        if result is None:
            self.skipTest("Not implemented")
        for key in ("detached", "no_grad_result", "requires_grad_detached", "requires_grad_no_grad"):
            self.assertIn(key, result)

    def test_detached_no_grad(self):
        result = detach_and_no_grad(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertFalse(result["requires_grad_detached"])

    def test_no_grad_result_no_grad(self):
        result = detach_and_no_grad(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertFalse(result["requires_grad_no_grad"])

    def test_detached_shares_data(self):
        result = detach_and_no_grad(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertTrue(torch.equal(result["detached"], self.x.detach()))

    def test_no_grad_result_value(self):
        result = detach_and_no_grad(self.x)
        if result is None:
            self.skipTest("Not implemented")
        expected = self.x.detach() * 2
        self.assertTrue(torch.allclose(result["no_grad_result"], expected))


class TestCustomFunction(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)

    def test_returns_not_none(self):
        x = torch.randn(5, requires_grad=True)
        result = custom_function(x)
        self.assertIsNotNone(result, "custom_function returned None — not yet implemented")

    def test_has_required_keys(self):
        x = torch.randn(5, requires_grad=True)
        result = custom_function(x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("output", result)
        self.assertIn("grad", result)

    def test_relu_behavior(self):
        x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0], requires_grad=True)
        result = custom_function(x)
        if result is None:
            self.skipTest("Not implemented")
        expected = torch.tensor([0.0, 0.0, 0.0, 1.0, 2.0])
        self.assertTrue(torch.equal(result["output"], expected))

    def test_grad_values(self):
        x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0], requires_grad=True)
        result = custom_function(x)
        if result is None:
            self.skipTest("Not implemented")
        # Gradient of clamp: 1 where x > 0, 0 where x < 0, 0 at x=0
        expected_grad = torch.tensor([0.0, 0.0, 0.0, 1.0, 1.0])
        self.assertTrue(torch.equal(result["grad"], expected_grad))


class TestHigherOrderGradients(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)

    def test_returns_not_none(self):
        result = higher_order_gradients(2.0)
        self.assertIsNotNone(result, "higher_order_gradients returned None — not yet implemented")

    def test_has_required_keys(self):
        result = higher_order_gradients(2.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("first", result)
        self.assertIn("second", result)

    def test_first_derivative(self):
        # dy/dx = 4x^3, at x=2: 4*8 = 32
        result = higher_order_gradients(2.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["first"], 32.0, places=4)

    def test_second_derivative(self):
        # d2y/dx2 = 12x^2, at x=2: 12*4 = 48
        result = higher_order_gradients(2.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["second"], 48.0, places=4)

    def test_at_x_equals_one(self):
        # dy/dx = 4, d2y/dx2 = 12
        result = higher_order_gradients(1.0)
        if result is None:
            self.skipTest("Not implemented")
        self.assertAlmostEqual(result["first"], 4.0, places=4)
        self.assertAlmostEqual(result["second"], 12.0, places=4)


if __name__ == "__main__":
    unittest.main()
