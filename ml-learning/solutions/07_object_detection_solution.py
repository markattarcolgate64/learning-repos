"""
Solution for Exercise 7: Object Detection — YOLO Inference & Fine-Tuning
"""

import os
import tempfile
import numpy as np

try:
    from ultralytics import YOLO
    HAS_ULTRALYTICS = True
except ImportError:
    HAS_ULTRALYTICS = False


def load_yolo_model(model_name='yolov8n.pt'):
    if not HAS_ULTRALYTICS:
        return None
    model = YOLO(model_name)
    return model


def run_inference(model, image_path):
    if model is None:
        return None
    results = model(image_path, verbose=False)
    result = results[0]
    boxes = result.boxes.xyxy.cpu().numpy()
    scores = result.boxes.conf.cpu().numpy()
    class_ids = result.boxes.cls.cpu().numpy().astype(int)
    class_names = [result.names[c] for c in class_ids]
    return {
        'boxes': boxes,
        'scores': scores,
        'class_ids': class_ids,
        'class_names': class_names,
        'n_detections': len(boxes),
    }


def create_dataset_yaml(dataset_dir):
    yaml_path = os.path.join(dataset_dir, 'dataset.yaml')
    abs_dir = os.path.abspath(dataset_dir)
    with open(yaml_path, 'w') as f:
        f.write(f'path: {abs_dir}\n')
        f.write('train: images/train\n')
        f.write('val: images/val\n')
        f.write('nc: 2\n')
        f.write("names: ['circle', 'rectangle']\n")
    return yaml_path


def fine_tune_yolo(dataset_yaml, epochs=2, imgsz=160):
    if not HAS_ULTRALYTICS:
        return None
    model = YOLO('yolov8n.pt')
    results = model.train(
        data=dataset_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=4,
        device='cpu',
        workers=0,
        verbose=False,
    )
    results_dir = str(results.save_dir)
    metrics = {
        'mAP50': float(results.results_dict.get('metrics/mAP50(B)', 0.0))
    }
    best_path = os.path.join(results_dir, 'weights', 'best.pt')
    if os.path.exists(best_path):
        fine_tuned = YOLO(best_path)
    else:
        fine_tuned = model
    return {
        'model': fine_tuned,
        'results_dir': results_dir,
        'metrics': metrics,
    }


def test_fine_tuned_model(model, dataset_dir):
    if model is None:
        return None
    val_dir = os.path.join(dataset_dir, 'images', 'val')
    if not os.path.exists(val_dir):
        return None
    image_files = sorted([f for f in os.listdir(val_dir) if f.endswith('.png')])
    detections_per_image = []
    total_detections = 0
    for img_file in image_files:
        img_path = os.path.join(val_dir, img_file)
        results = model(img_path, verbose=False)
        n_det = len(results[0].boxes)
        detections_per_image.append(n_det)
        total_detections += n_det
    return {
        'total_images': len(image_files),
        'total_detections': total_detections,
        'detections_per_image': detections_per_image,
    }
