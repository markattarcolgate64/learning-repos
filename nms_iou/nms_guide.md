# Non-Maximum Suppression (NMS) Guide

## What NMS Does
NMS removes duplicate detections by keeping the highest-scoring box and suppressing nearby boxes that overlap it too much.

## Inputs
- Boxes: (x_min, y_min, x_max, y_max)
- Scores: confidence for each box
- IoU threshold: overlap cutoff (e.g., 0.5)

## Core Algorithm (Hard NMS)
1) Sort boxes by descending score.
2) Pick the top-scoring box and keep it.
3) Compute IoU between that box and the remaining boxes.
4) Remove any box with IoU >= threshold.
5) Repeat until no boxes remain.

## Pseudocode
```
keep = []
order = argsort(scores, descending=True)
while order not empty:
    i = order[0]
    keep.append(i)
    rest = order[1:]
    ious = IoU(boxes[i], boxes[rest])
    order = rest[ious < threshold]
return keep
```

## When to Apply
- After model inference to prune overlapping predictions.
- Typically done per class, not across different classes.

## Tuning Tips
- Lower threshold keeps more boxes (less aggressive suppression).
- Higher threshold removes more boxes (more aggressive suppression).
- Common values: 0.3 to 0.6 depending on object density.

## Variants You Should Know
- Soft-NMS: reduces scores instead of removing boxes.
- DIoU-NMS / CIoU-NMS: use distance-aware overlap.

## Common Pitfalls
- Forgetting to sort by score.
- Mixing classes in NMS (unless you intend class-agnostic NMS).
- Using a different box format than your IoU function expects.

