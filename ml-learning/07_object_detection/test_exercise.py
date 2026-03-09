"""
Tests for Exercise 7: Object Detection — YOLO Inference & Fine-Tuning.

All tests require ultralytics. They are skipped if it's not installed.

Run with:
    python -m unittest 07_object_detection.test_exercise -v
"""

import unittest
import tempfile
import shutil
import os
import numpy as np

from .exercise import (
    HAS_ULTRALYTICS,
    generate_shapes_dataset,
    _write_png,
    load_yolo_model,
    run_inference,
    create_dataset_yaml,
    fine_tune_yolo,
    test_fine_tuned_model,
)


@unittest.skipUnless(HAS_ULTRALYTICS, "ultralytics not installed — run: pip install ultralytics")
class TestObjectDetection(unittest.TestCase):
    """Tests for YOLO inference and fine-tuning exercise."""

    @classmethod
    def setUpClass(cls):
        """Create shared fixtures: dataset, model, and test image."""
        cls.dataset_dir = tempfile.mkdtemp(prefix='shapes_yolo_test_')
        generate_shapes_dataset(cls.dataset_dir, n_train=20, n_val=5)

        # Create a test image for inference
        cls.test_img_path = os.path.join(cls.dataset_dir, '_test_img.png')
        img = np.full((320, 320, 3), 180, dtype=np.uint8)
        img[80:200, 60:180] = [50, 100, 220]  # blue rectangle
        _write_png(img, cls.test_img_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dataset_dir, ignore_errors=True)

    # ------------------------------------------------------------------
    # 1. Load model
    # ------------------------------------------------------------------

    def test_load_yolo_model_returns_model(self):
        """load_yolo_model() should return a YOLO model object."""
        model = load_yolo_model()
        self.assertIsNotNone(model, "load_yolo_model() returned None")
        self.assertTrue(hasattr(model, 'predict'),
                        "Model should have a .predict() method")

    def test_load_yolo_model_custom_name(self):
        """load_yolo_model() should accept a model name parameter."""
        model = load_yolo_model('yolov8n.pt')
        self.assertIsNotNone(model)

    # ------------------------------------------------------------------
    # 2. Inference
    # ------------------------------------------------------------------

    def test_run_inference_returns_dict(self):
        """run_inference() should return a dict with expected keys."""
        model = load_yolo_model()
        result = run_inference(model, self.test_img_path)
        self.assertIsNotNone(result, "run_inference() returned None")
        for key in ['boxes', 'scores', 'class_ids', 'class_names', 'n_detections']:
            self.assertIn(key, result, f"Missing key: '{key}'")

    def test_run_inference_consistent_shapes(self):
        """All arrays in inference result should have consistent lengths."""
        model = load_yolo_model()
        result = run_inference(model, self.test_img_path)
        self.assertIsNotNone(result)
        n = result['n_detections']
        self.assertEqual(len(result['scores']), n)
        self.assertEqual(len(result['class_ids']), n)
        self.assertEqual(len(result['class_names']), n)
        if n > 0:
            self.assertEqual(result['boxes'].shape, (n, 4))

    def test_run_inference_scores_in_range(self):
        """Confidence scores should be in [0, 1]."""
        model = load_yolo_model()
        result = run_inference(model, self.test_img_path)
        self.assertIsNotNone(result)
        if result['n_detections'] > 0:
            self.assertTrue(np.all(result['scores'] >= 0))
            self.assertTrue(np.all(result['scores'] <= 1))

    def test_run_inference_class_ids_are_ints(self):
        """Class IDs should be integers."""
        model = load_yolo_model()
        result = run_inference(model, self.test_img_path)
        self.assertIsNotNone(result)
        if result['n_detections'] > 0:
            self.assertTrue(np.issubdtype(result['class_ids'].dtype, np.integer))

    def test_run_inference_returns_none_for_none_model(self):
        """run_inference(None, ...) should return None gracefully."""
        result = run_inference(None, self.test_img_path)
        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # 3. Dataset YAML
    # ------------------------------------------------------------------

    def test_create_dataset_yaml_creates_file(self):
        """create_dataset_yaml() should create a .yaml file on disk."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path, "create_dataset_yaml() returned None")
        self.assertTrue(os.path.exists(yaml_path),
                        f"YAML file not found at {yaml_path}")

    def test_create_dataset_yaml_has_required_fields(self):
        """YAML config should contain path, train, val, nc, names."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path)
        with open(yaml_path) as f:
            content = f.read()
        for field in ['path:', 'train:', 'val:', 'nc:', 'names:']:
            self.assertIn(field, content,
                          f"YAML missing required field: {field}")

    def test_create_dataset_yaml_correct_nc(self):
        """YAML should specify nc: 2 (circle and rectangle)."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path)
        with open(yaml_path) as f:
            content = f.read()
        self.assertIn('nc: 2', content,
                      "YAML should have nc: 2 for our 2 classes")

    def test_create_dataset_yaml_has_class_names(self):
        """YAML should list 'circle' and 'rectangle' class names."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path)
        with open(yaml_path) as f:
            content = f.read()
        self.assertIn('circle', content)
        self.assertIn('rectangle', content)

    def test_create_dataset_yaml_uses_absolute_path(self):
        """YAML path field should be an absolute path."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path)
        with open(yaml_path) as f:
            content = f.read()
        # Extract the path value
        for line in content.split('\n'):
            if line.startswith('path:'):
                path_val = line.split(':', 1)[1].strip()
                self.assertTrue(os.path.isabs(path_val),
                                f"path should be absolute, got: {path_val}")
                break

    # ------------------------------------------------------------------
    # 4. Fine-tuning
    # ------------------------------------------------------------------

    def test_fine_tune_yolo_returns_result(self):
        """fine_tune_yolo() should return a dict with model, results_dir, metrics."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        self.assertIsNotNone(yaml_path)
        result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(result, "fine_tune_yolo() returned None")
        for key in ['model', 'results_dir', 'metrics']:
            self.assertIn(key, result, f"Missing key: '{key}'")

    def test_fine_tune_yolo_results_dir_exists(self):
        """Training results directory should exist on disk."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(result)
        self.assertTrue(os.path.isdir(result['results_dir']),
                        f"Results dir not found: {result['results_dir']}")

    def test_fine_tune_yolo_has_map50(self):
        """Metrics should include mAP50."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(result)
        self.assertIn('mAP50', result['metrics'])
        self.assertIsInstance(result['metrics']['mAP50'], float)

    def test_fine_tuned_model_can_predict(self):
        """Fine-tuned model should be able to run inference."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(result)
        model = result['model']
        self.assertTrue(hasattr(model, 'predict'),
                        "Fine-tuned model should have .predict()")
        # Run a prediction to verify it works
        preds = model(self.test_img_path, verbose=False)
        self.assertIsNotNone(preds)
        self.assertGreater(len(preds), 0)

    # ------------------------------------------------------------------
    # 5. Test fine-tuned model
    # ------------------------------------------------------------------

    def test_test_fine_tuned_model_returns_result(self):
        """test_fine_tuned_model() should return detection stats."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        ft_result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(ft_result)

        result = test_fine_tuned_model(ft_result['model'], self.dataset_dir)
        self.assertIsNotNone(result, "test_fine_tuned_model() returned None")
        for key in ['total_images', 'total_detections', 'detections_per_image']:
            self.assertIn(key, result, f"Missing key: '{key}'")

    def test_test_fine_tuned_model_correct_image_count(self):
        """Should test on all validation images."""
        yaml_path = create_dataset_yaml(self.dataset_dir)
        ft_result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
        self.assertIsNotNone(ft_result)

        result = test_fine_tuned_model(ft_result['model'], self.dataset_dir)
        self.assertIsNotNone(result)
        self.assertEqual(result['total_images'], 5,
                         "Should test on 5 validation images")
        self.assertEqual(len(result['detections_per_image']), 5)

    def test_test_fine_tuned_model_returns_none_for_none_model(self):
        """test_fine_tuned_model(None, ...) should return None."""
        result = test_fine_tuned_model(None, self.dataset_dir)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
