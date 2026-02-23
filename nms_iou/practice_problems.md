# IoU and NMS Practice Problems

Use these as hand-worked exercises. Only check the answers once you have your result.

## Part A: IoU by Hand

1) Boxes:
   - A: (0, 0, 4, 4)
   - B: (2, 2, 6, 6)
   Compute IoU.

2) Boxes:
   - A: (1, 1, 5, 4)
   - B: (6, 2, 9, 6)
   Compute IoU.

3) Boxes:
   - A: (0, 0, 10, 10)
   - B: (2, 2, 8, 8)
   Compute IoU.

4) Boxes:
   - A: (3, 3, 7, 7)
   - B: (5, 5, 9, 9)
   Compute IoU.

5) Boxes:
   - A: (0, 0, 5, 5)
   - B: (1, 1, 4, 4)
   - C: (6, 6, 9, 9)
   Compute IoU for (A,B) and (A,C).

## Part B: NMS by Hand

Assume class-wise NMS with IoU threshold = 0.5.

Given boxes and scores:
1) Box 0: (0, 0, 4, 4), score 0.95
2) Box 1: (1, 1, 5, 5), score 0.90
3) Box 2: (10, 10, 14, 14), score 0.60
4) Box 3: (2, 2, 6, 6), score 0.55

Questions:
- Which boxes are kept in order?
- Which boxes are suppressed, and by which kept box?

## Part C: Coding Tasks (No Libraries)

1) Write a function `iou(box_a, box_b)` using (x_min, y_min, x_max, y_max).
2) Write `pairwise_iou(boxes_a, boxes_b)` that returns a matrix of IoUs.
3) Implement `nms(boxes, scores, threshold)` using hard NMS.

## Part D: IoU Coding Problems (No Libraries)

1) Implement `iou_center(box_a, box_b)` where boxes are (x_center, y_center, w, h).
2) Write `iou_safe(box_a, box_b)` that returns 0 if either box has non-positive area.
3) Implement `max_iou(query_box, boxes)` that returns (best_index, best_iou).
4) Given a list of boxes, compute a symmetric IoU matrix (NxN) with zeros on the diagonal.
5) Write `iou_threshold_filter(boxes, scores, query_box, t)` that returns boxes with IoU >= t.

## Part E: NMS Coding Problems (No Libraries)

1) Implement class-wise NMS given `boxes`, `scores`, and `classes`.
2) Add `top_k` to NMS: keep only the top K scores before suppression.
3) Implement Soft-NMS (linear decay) and compare kept indices to hard NMS.
4) Write `batched_nms` that runs NMS for each class separately and concatenates results.
5) Add a `max_output` limit to NMS that stops once you have enough kept boxes.

## Part F: Edge Cases

1) What should IoU be when boxes do not overlap?
2) What if one box has zero area?
3) How do you handle negative coordinates?

## Answer Check (Peek Only After Solving)

Part A:
1) IoU = 4 / 28 = 0.142857...
2) IoU = 0
3) IoU = 36 / 100 = 0.36
4) IoU = 4 / 28 = 0.142857...
5) IoU(A,B) = 9 / 25 = 0.36, IoU(A,C) = 0

Part B:
- Keep order: Box 0, Box 2
- Suppressed: Box 1 (by Box 0), Box 3 (by Box 0)
