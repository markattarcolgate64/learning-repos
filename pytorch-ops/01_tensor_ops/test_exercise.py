"""
Tests for Tensor Operations Bootcamp (Exercise 01).
"""

import unittest
import torch
from .exercise import (
    reshape_and_view,
    transpose_and_permute,
    broadcasting_add,
    batched_matmul,
    indexing_and_masking,
    einsum_operations,
)


class TestReshapeAndView(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.x = torch.arange(12, dtype=torch.float32)

    def test_returns_not_none(self):
        result = reshape_and_view(self.x)
        self.assertIsNotNone(result, "reshape_and_view returned None — not yet implemented")

    def test_has_required_keys(self):
        result = reshape_and_view(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("view_34", result)
        self.assertIn("reshape_26", result)

    def test_view_shape(self):
        result = reshape_and_view(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["view_34"].shape, (3, 4))

    def test_reshape_shape(self):
        result = reshape_and_view(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["reshape_26"].shape, (2, 6))

    def test_values_preserved(self):
        result = reshape_and_view(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertTrue(torch.equal(result["view_34"].flatten(), self.x))
        self.assertTrue(torch.equal(result["reshape_26"].flatten(), self.x))


class TestTransposeAndPermute(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.x = torch.randn(2, 3, 4)

    def test_returns_not_none(self):
        result = transpose_and_permute(self.x)
        self.assertIsNotNone(result, "transpose_and_permute returned None — not yet implemented")

    def test_transposed_shape(self):
        result = transpose_and_permute(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["transposed"].shape, (2, 4, 3))

    def test_permuted_shape(self):
        result = transpose_and_permute(self.x)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["permuted"].shape, (4, 2, 3))

    def test_transpose_values(self):
        result = transpose_and_permute(self.x)
        if result is None:
            self.skipTest("Not implemented")
        # x[i, j, k] == transposed[i, k, j]
        self.assertEqual(self.x[0, 1, 2].item(), result["transposed"][0, 2, 1].item())

    def test_permute_values(self):
        result = transpose_and_permute(self.x)
        if result is None:
            self.skipTest("Not implemented")
        # x[i, j, k] == permuted[k, i, j]
        self.assertEqual(self.x[1, 2, 3].item(), result["permuted"][3, 1, 2].item())


class TestBroadcastingAdd(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.a = torch.tensor([[1.0], [2.0], [3.0]])  # (3, 1)
        self.b = torch.tensor([[10.0, 20.0, 30.0, 40.0]])  # (1, 4)

    def test_returns_not_none(self):
        result = broadcasting_add(self.a, self.b)
        self.assertIsNotNone(result, "broadcasting_add returned None — not yet implemented")

    def test_shape(self):
        result = broadcasting_add(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result.shape, (3, 4))

    def test_values(self):
        result = broadcasting_add(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        expected = torch.tensor([
            [11.0, 21.0, 31.0, 41.0],
            [12.0, 22.0, 32.0, 42.0],
            [13.0, 23.0, 33.0, 43.0],
        ])
        self.assertTrue(torch.equal(result, expected))


class TestBatchedMatmul(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.a = torch.randn(4, 3, 5)
        self.b = torch.randn(4, 5, 2)

    def test_returns_not_none(self):
        result = batched_matmul(self.a, self.b)
        self.assertIsNotNone(result, "batched_matmul returned None — not yet implemented")

    def test_shape(self):
        result = batched_matmul(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result.shape, (4, 3, 2))

    def test_values_match_torch(self):
        result = batched_matmul(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        expected = torch.bmm(self.a, self.b)
        self.assertTrue(torch.allclose(result, expected, atol=1e-6))


class TestIndexingAndMasking(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.x = torch.randn(3, 4)
        self.threshold = 0.0

    def test_returns_not_none(self):
        result = indexing_and_masking(self.x, self.threshold)
        self.assertIsNotNone(result, "indexing_and_masking returned None — not yet implemented")

    def test_has_required_keys(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("mask", result)
        self.assertIn("selected", result)
        self.assertIn("count", result)

    def test_mask_shape(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["mask"].shape, self.x.shape)

    def test_mask_dtype(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["mask"].dtype, torch.bool)

    def test_selected_is_1d(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["selected"].dim(), 1)

    def test_count_matches(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["count"], result["mask"].sum().item())
        self.assertIsInstance(result["count"], int)

    def test_all_selected_above_threshold(self):
        result = indexing_and_masking(self.x, self.threshold)
        if result is None:
            self.skipTest("Not implemented")
        self.assertTrue((result["selected"] > self.threshold).all())


class TestEinsumOperations(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        self.a = torch.randn(2, 5, 8)  # (batch, seq, d)
        self.b = torch.randn(8, 8)     # (d, d)

    def test_returns_not_none(self):
        result = einsum_operations(self.a, self.b)
        self.assertIsNotNone(result, "einsum_operations returned None — not yet implemented")

    def test_has_required_keys(self):
        result = einsum_operations(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        self.assertIn("linear", result)
        self.assertIn("similarity", result)

    def test_linear_shape(self):
        result = einsum_operations(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["linear"].shape, (2, 5, 8))

    def test_linear_values(self):
        result = einsum_operations(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        expected = self.a @ self.b
        self.assertTrue(torch.allclose(result["linear"], expected, atol=1e-5))

    def test_similarity_shape(self):
        result = einsum_operations(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        self.assertEqual(result["similarity"].shape, (2, 5, 5))

    def test_similarity_values(self):
        result = einsum_operations(self.a, self.b)
        if result is None:
            self.skipTest("Not implemented")
        expected = self.a @ self.a.transpose(-1, -2)
        self.assertTrue(torch.allclose(result["similarity"], expected, atol=1e-5))


if __name__ == "__main__":
    unittest.main()
