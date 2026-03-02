"""
Object Detection: YOLO Inference & Fine-Tuning
================================================
Difficulty : *** (3/5)

You know how to classify images (Exercise 6). Now learn to DETECT objects —
find WHAT is in an image AND WHERE it is.

This exercise teaches the practical workflow of object detection:
  1. Load a pre-trained YOLO model and run inference
  2. Parse detection results (boxes, scores, class labels)
  3. Prepare a custom dataset in YOLO format
  4. Fine-tune YOLO to detect your own custom objects
  5. Run your fine-tuned model and evaluate results

This is a real-world workflow — the same steps you'd follow to ship
a custom object detector for a product, a robot, or a research project.

Requires:
    pip install ultralytics

Dataset: Synthetic images of colored shapes (generated at runtime)
  - 2 classes: circle, rectangle
  - No downloads needed — images are generated with numpy

Run:
    python 07_object_detection/exercise.py

Test:
    python -m unittest 07_object_detection.test_exercise -v
"""

import os
import tempfile
import numpy as np

try:
    from ultralytics import YOLO
    HAS_ULTRALYTICS = True
except ImportError:
    HAS_ULTRALYTICS = False


# ============================================================
# SYNTHETIC DATA HELPERS (GIVEN — read but don't modify)
# ============================================================
# These helpers generate a tiny dataset of colored shapes on
# plain backgrounds. Two classes:
#   0 = "circle"     (blue-ish blob)
#   1 = "rectangle"  (red-ish blob)
#
# The dataset uses YOLO format:
#   dataset/
#   ├── images/
#   │   ├── train/   ← training images (PNG)
#   │   └── val/     ← validation images
#   ├── labels/
#   │   ├── train/   ← one .txt per image
#   │   └── val/
#   └── dataset.yaml ← config file
#
# Each label .txt has one line per object:
#   class_id  cx  cy  w  h
# All coordinates normalized to [0, 1] relative to image size.

def _write_png(image, path):
    """Write a numpy array as PNG. Uses PIL if available, else pure stdlib. (GIVEN)"""
    try:
        from PIL import Image
        Image.fromarray(image).save(path)
    except ImportError:
        import struct
        import zlib
        h, w = image.shape[:2]

        def chunk(name, data):
            crc = zlib.crc32(name + data) & 0xFFFFFFFF
            return struct.pack('>I', len(data)) + name + data + struct.pack('>I', crc)

        raw = b''.join(b'\x00' + image[y].tobytes() for y in range(h))
        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', zlib.compress(raw)))
            f.write(chunk(b'IEND', b''))


def generate_shapes_dataset(dataset_dir, n_train=20, n_val=5, img_size=160, seed=42):
    """Generate a tiny YOLO-format dataset of colored shapes. (GIVEN)

    Creates images with colored circles and rectangles on gray backgrounds,
    plus matching YOLO-format label files.

    Args:
        dataset_dir: directory to create the dataset in.
        n_train: number of training images.
        n_val: number of validation images.
        img_size: width and height of each image in pixels.
        seed: random seed for reproducibility.

    Returns:
        dataset_dir (the same path passed in).
    """
    rng = np.random.RandomState(seed)

    COLORS = {
        0: np.array([50, 100, 220], dtype=np.uint8),   # blue = circle
        1: np.array([220, 60, 50], dtype=np.uint8),     # red = rectangle
    }

    for split, n_images in [('train', n_train), ('val', n_val)]:
        img_dir = os.path.join(dataset_dir, 'images', split)
        lbl_dir = os.path.join(dataset_dir, 'labels', split)
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)

        for idx in range(n_images):
            # Gray background
            img = np.full((img_size, img_size, 3), 180, dtype=np.uint8)

            # Pick class and draw shape
            cls_id = rng.randint(0, 2)
            color = COLORS[cls_id]

            # Random size (15-35% of image)
            h_px = max(8, int(rng.uniform(0.15, 0.35) * img_size))
            w_px = max(8, int(h_px * rng.uniform(0.8 if cls_id == 0 else 1.4,
                                                  1.2 if cls_id == 0 else 2.2)))
            w_px = min(w_px, img_size - 4)
            h_px = min(h_px, img_size - 4)

            # Random position
            x1 = rng.randint(2, img_size - w_px - 2)
            y1 = rng.randint(2, img_size - h_px - 2)
            x2 = x1 + w_px
            y2 = y1 + h_px

            # Draw filled rectangle
            img[y1:y2, x1:x2] = color

            # YOLO label (normalized center format)
            cx = (x1 + x2) / 2 / img_size
            cy = (y1 + y2) / 2 / img_size
            w_norm = (x2 - x1) / img_size
            h_norm = (y2 - y1) / img_size
            label_line = f"{cls_id} {cx:.6f} {cy:.6f} {w_norm:.6f} {h_norm:.6f}"

            stem = f"{split}_{idx:04d}"
            _write_png(img, os.path.join(img_dir, f"{stem}.png"))
            with open(os.path.join(lbl_dir, f"{stem}.txt"), 'w') as f:
                f.write(label_line + '\n')

    return dataset_dir


# ============================================================
# PART 1: Load a Pre-Trained YOLO Model
# ============================================================
# YOLOv8 by Ultralytics is the most popular object detector.
# YOLOv8n ("nano") is the smallest variant:
#   - 3.2 million parameters
#   - ~6 MB model file
#   - Trained on COCO dataset (80 object classes)
#   - Can detect: person, car, dog, cat, chair, bottle, etc.
#
# Loading it is one line:
#   model = YOLO('yolov8n.pt')
#
# On first run, it auto-downloads the weights (~6 MB).

def load_yolo_model(model_name='yolov8n.pt'):
    """Load a pre-trained YOLO model.

    Args:
        model_name: model weight file name (default: 'yolov8n.pt').

    Returns:
        A YOLO model object, or None if ultralytics is not installed.
    """
    if not HAS_ULTRALYTICS:
        return None

    # TODO: Load and return the YOLO model
    # Hint: model = YOLO(model_name)
    #       return model
    return None  # Your code here


# ============================================================
# PART 2: Run Inference and Parse Results
# ============================================================
# Running inference is also one line:
#   results = model(image_path, verbose=False)
#
# But the results object has structure you need to understand:
#   results[0]           — results for the first (only) image
#   results[0].boxes     — all detected bounding boxes
#     .xyxy              — box coordinates [x1, y1, x2, y2] (tensor)
#     .conf              — confidence scores (tensor)
#     .cls               — class IDs (tensor)
#   results[0].names     — dict mapping class ID → class name
#
# To get numpy arrays, use: tensor.cpu().numpy()
# To get class names: results[0].names[class_id]

def run_inference(model, image_path):
    """Run YOLO inference on a single image.

    Args:
        model: a YOLO model object.
        image_path: path to an image file.

    Returns:
        A dict with:
        - 'boxes': (N, 4) numpy array in [x1, y1, x2, y2] format
        - 'scores': (N,) numpy array of confidence scores
        - 'class_ids': (N,) numpy array of integer class IDs
        - 'class_names': list of N class name strings
        - 'n_detections': int, total number of detections
        Returns None if model is None.
    """
    if model is None:
        return None

    # TODO: Run inference and extract results
    # Hint:
    #   results = model(image_path, verbose=False)
    #   result = results[0]
    #
    #   boxes = result.boxes.xyxy.cpu().numpy()
    #   scores = result.boxes.conf.cpu().numpy()
    #   class_ids = result.boxes.cls.cpu().numpy().astype(int)
    #   class_names = [result.names[c] for c in class_ids]
    #
    #   return {
    #       'boxes': boxes,
    #       'scores': scores,
    #       'class_ids': class_ids,
    #       'class_names': class_names,
    #       'n_detections': len(boxes),
    #   }
    return None  # Your code here


# ============================================================
# PART 3: Create a YOLO Dataset Config
# ============================================================
# To train YOLO on custom data, you need a YAML config file
# that tells it where the images and labels are:
#
#   path: /absolute/path/to/dataset
#   train: images/train
#   val: images/val
#   nc: 2
#   names: ['circle', 'rectangle']
#
# 'path' must be an absolute path (avoids confusing relative path issues).
# 'nc' is the number of classes.
# 'names' maps class IDs (0, 1, ...) to human-readable names.

def create_dataset_yaml(dataset_dir):
    """Create the YOLO dataset YAML configuration file.

    Args:
        dataset_dir: absolute path to the dataset directory
                     (as created by generate_shapes_dataset).

    Returns:
        Path to the written YAML file (dataset_dir/dataset.yaml).
    """
    # TODO: Write a YAML config file for YOLO training
    # Hint:
    #   yaml_path = os.path.join(dataset_dir, 'dataset.yaml')
    #   abs_dir = os.path.abspath(dataset_dir)
    #   with open(yaml_path, 'w') as f:
    #       f.write(f'path: {abs_dir}\n')
    #       f.write('train: images/train\n')
    #       f.write('val: images/val\n')
    #       f.write('nc: 2\n')
    #       f.write("names: ['circle', 'rectangle']\n")
    #   return yaml_path
    return None  # Your code here


# ============================================================
# PART 4: Fine-Tune YOLO on Your Custom Dataset
# ============================================================
# Fine-tuning = take a pre-trained model and continue training
# it on YOUR data. The model already knows general features
# (edges, textures, shapes) from COCO. You just teach it
# your specific classes.
#
# The training API is simple:
#   model = YOLO('yolov8n.pt')       # start from pre-trained
#   model.train(data='dataset.yaml', epochs=2, ...)
#
# Key training parameters for CPU:
#   device='cpu'   — no GPU
#   imgsz=160      — small images = faster training
#   epochs=2       — just enough to verify the workflow
#   batch=4        — small batch size for CPU memory
#   workers=0      — avoid multiprocessing issues
#   verbose=False  — don't flood the console
#
# Real training uses a GPU, larger images (640), and 50-300 epochs.
# Here we just learn the WORKFLOW.

def fine_tune_yolo(dataset_yaml, epochs=2, imgsz=160):
    """Fine-tune YOLOv8n on a custom dataset.

    Args:
        dataset_yaml: path to the dataset YAML config.
        epochs: number of training epochs (keep small for CPU!).
        imgsz: image size for training (keep small for CPU!).

    Returns:
        A dict with:
        - 'model': the fine-tuned YOLO model
        - 'results_dir': path to training results directory
        - 'metrics': dict with 'mAP50' from validation results
        Returns None if ultralytics is not installed.
    """
    if not HAS_ULTRALYTICS:
        return None

    # TODO: Fine-tune YOLOv8n
    # Hint:
    #   model = YOLO('yolov8n.pt')
    #   results = model.train(
    #       data=dataset_yaml,
    #       epochs=epochs,
    #       imgsz=imgsz,
    #       batch=4,
    #       device='cpu',
    #       workers=0,
    #       verbose=False,
    #   )
    #
    #   results_dir = str(results.save_dir)
    #   metrics = {
    #       'mAP50': float(results.results_dict.get('metrics/mAP50(B)', 0.0))
    #   }
    #
    #   # Load best checkpoint
    #   best_path = os.path.join(results_dir, 'weights', 'best.pt')
    #   if os.path.exists(best_path):
    #       fine_tuned = YOLO(best_path)
    #   else:
    #       fine_tuned = model
    #
    #   return {
    #       'model': fine_tuned,
    #       'results_dir': results_dir,
    #       'metrics': metrics,
    #   }
    return None  # Your code here


# ============================================================
# PART 5: Test Your Fine-Tuned Model
# ============================================================
# The final step: use your fine-tuned model to detect objects
# in new images. This closes the loop:
#   pre-trained model → custom data → fine-tuned model → deploy
#
# You'll run inference with your fine-tuned model on validation
# images and check if it detects the shapes correctly.

def test_fine_tuned_model(model, dataset_dir):
    """Run the fine-tuned model on validation images and report results.

    Args:
        model: a fine-tuned YOLO model.
        dataset_dir: path to the dataset directory.

    Returns:
        A dict with:
        - 'total_images': number of validation images tested
        - 'total_detections': total detections across all images
        - 'detections_per_image': list of detection counts per image
        Returns None if model is None.
    """
    if model is None:
        return None

    val_dir = os.path.join(dataset_dir, 'images', 'val')
    if not os.path.exists(val_dir):
        return None

    # TODO: Run inference on each validation image and collect results
    # Hint:
    #   image_files = sorted([f for f in os.listdir(val_dir) if f.endswith('.png')])
    #   detections_per_image = []
    #   total_detections = 0
    #
    #   for img_file in image_files:
    #       img_path = os.path.join(val_dir, img_file)
    #       results = model(img_path, verbose=False)
    #       n_det = len(results[0].boxes)
    #       detections_per_image.append(n_det)
    #       total_detections += n_det
    #
    #   return {
    #       'total_images': len(image_files),
    #       'total_detections': total_detections,
    #       'detections_per_image': detections_per_image,
    #   }
    return None  # Your code here


# ============================================================
# Run the full object detection pipeline
# ============================================================
if __name__ == "__main__":
    import shutil

    if not HAS_ULTRALYTICS:
        print("=" * 60)
        print("ultralytics is not installed!")
        print("Install with: pip install ultralytics")
        print("Then re-run this script.")
        print("=" * 60)
        exit(1)

    # Part 1: Load model
    print("=" * 60)
    print("PART 1: Loading Pre-Trained YOLOv8n")
    print("=" * 60)
    model = load_yolo_model()
    if model is not None:
        print("Model loaded successfully!")
        print(f"Model type: {type(model).__name__}")
    else:
        print("TODO: Implement load_yolo_model()")

    # Part 2: Inference
    print("\n" + "=" * 60)
    print("PART 2: Running Inference")
    print("=" * 60)
    if model is not None:
        # Create a test image
        rng = np.random.RandomState(99)
        test_img = np.full((320, 320, 3), 180, dtype=np.uint8)
        test_img[80:200, 60:180] = [50, 100, 220]  # blue rectangle
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            _write_png(test_img, f.name)
            tmp_path = f.name
        try:
            detections = run_inference(model, tmp_path)
            if detections is not None:
                print(f"Detections: {detections['n_detections']}")
                for i in range(min(detections['n_detections'], 5)):
                    print(f"  {detections['class_names'][i]:15s} "
                          f"conf={detections['scores'][i]:.2f}  "
                          f"box={detections['boxes'][i].astype(int)}")
                if detections['n_detections'] == 0:
                    print("  (No detections — expected for synthetic image on COCO model)")
            else:
                print("TODO: Implement run_inference()")
        finally:
            os.unlink(tmp_path)

    # Part 3: Create dataset
    print("\n" + "=" * 60)
    print("PART 3: Creating YOLO Dataset")
    print("=" * 60)
    dataset_dir = tempfile.mkdtemp(prefix='shapes_yolo_')
    try:
        generate_shapes_dataset(dataset_dir, n_train=20, n_val=5)
        n_train = len(os.listdir(os.path.join(dataset_dir, 'images', 'train')))
        n_val = len(os.listdir(os.path.join(dataset_dir, 'images', 'val')))
        print(f"Dataset created at: {dataset_dir}")
        print(f"  Training images: {n_train}")
        print(f"  Validation images: {n_val}")
        print(f"  Classes: circle (blue), rectangle (red)")

        yaml_path = create_dataset_yaml(dataset_dir)
        if yaml_path is not None:
            print(f"  YAML config: {yaml_path}")
            with open(yaml_path) as f:
                print(f"  Contents:\n{f.read()}")
        else:
            print("TODO: Implement create_dataset_yaml()")

        # Part 4: Fine-tune
        print("\n" + "=" * 60)
        print("PART 4: Fine-Tuning YOLO (2 epochs, ~1-3 min on CPU)")
        print("=" * 60)
        if yaml_path is not None:
            ft_result = fine_tune_yolo(yaml_path, epochs=2, imgsz=160)
            if ft_result is not None:
                print(f"Fine-tuning complete!")
                print(f"  Results dir: {ft_result['results_dir']}")
                print(f"  mAP@50: {ft_result['metrics']['mAP50']:.4f}")

                # Part 5: Test fine-tuned model
                print("\n" + "=" * 60)
                print("PART 5: Testing Fine-Tuned Model")
                print("=" * 60)
                test_results = test_fine_tuned_model(ft_result['model'], dataset_dir)
                if test_results is not None:
                    print(f"Tested on {test_results['total_images']} validation images")
                    print(f"Total detections: {test_results['total_detections']}")
                    print(f"Detections per image: {test_results['detections_per_image']}")
                else:
                    print("TODO: Implement test_fine_tuned_model()")
            else:
                print("TODO: Implement fine_tune_yolo()")
        else:
            print("Skipping — need create_dataset_yaml() first")

    finally:
        shutil.rmtree(dataset_dir, ignore_errors=True)
        print("\nCleaned up temp dataset directory.")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 07_object_detection.test_exercise -v")
    print("=" * 60)
