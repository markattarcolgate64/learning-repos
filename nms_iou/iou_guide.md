# Intersection over Union (IoU) Guide

## What IoU Measures
IoU quantifies overlap between two axis-aligned bounding boxes:

IoU = Area(Intersection) / Area(Union)

It ranges from 0 (no overlap) to 1 (perfect overlap).

## Box Format (Assumed)
This guide uses box coordinates as:

- (x_min, y_min, x_max, y_max)
- x_max > x_min, y_max > y_min
- Coordinates are in pixels or normalized units

## Step-by-Step Calculation
1) Compute intersection corners:
   - inter_x_min = max(x_min_A, x_min_B)
   - inter_y_min = max(y_min_A, y_min_B)
   - inter_x_max = min(x_max_A, x_max_B)
   - inter_y_max = min(y_max_A, y_max_B)

2) Intersection width/height:
   - inter_w = max(0, inter_x_max - inter_x_min)
   - inter_h = max(0, inter_y_max - inter_y_min)
   - inter_area = inter_w * inter_h

3) Areas:
   - area_A = (x_max_A - x_min_A) * (y_max_A - y_min_A)
   - area_B = (x_max_B - x_min_B) * (y_max_B - y_min_B)

4) Union:
   - union_area = area_A + area_B - inter_area

5) IoU:
   - iou = inter_area / union_area

## Worked Example
Box A: (10, 10, 30, 30)
Box B: (20, 20, 40, 40)

Intersection:
- inter_x_min = 20, inter_y_min = 20
- inter_x_max = 30, inter_y_max = 30
- inter_w = 10, inter_h = 10, inter_area = 100

Areas:
- area_A = 20 * 20 = 400
- area_B = 20 * 20 = 400

Union:
- union_area = 400 + 400 - 100 = 700

IoU:
- 100 / 700 = 0.142857...

## Common Pitfalls
- Mixing formats (center/width/height vs corners)
- Forgetting max(0, ...) on intersection width/height
- Off-by-one from pixel-inclusive coordinates (decide your convention and stick to it)

## Quick Reference
If you switch to (x_center, y_center, width, height), convert to corners before IoU.

