from ultralytics import YOLO
import numpy as np
import cv2
# import torch


class Masker:
    def __init__(self, model_name='models/yolov8x-seg.pt'):
        self.model = YOLO(model_name)

    def apply_mask(self, frame, threshold=0.5, cls2include=[0], cls2exclude=[1, 2]):
        # class 0: human
        results = self.model(frame)[0]
        # Mask initialisation
        mask_combined = np.zeros(frame.shape[:2], dtype=np.uint8)

        for i, cls in enumerate(results.boxes.cls):
            if int(cls) in cls2include:
                mask = results.masks.data[i].cpu().numpy()
                mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
                mask_combined[mask_resized > threshold] = 255
            elif int(cls) in cls2exclude:
                mask = results.masks.data[i].cpu().numpy()
                # Dilate the mask to ensure the ccoverage
                mask_dilated = cv2.dilate(mask, kernel=np.ones((25, 25), np.uint8), iterations=1)
                mask_resized = cv2.resize(mask_dilated, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
                mask_combined[mask_resized > threshold] = 0

        # return self.exclude_border(mask_combined, 10)  # 255 = person, 0 = background
        return mask_combined  # 255 = wall, 0 = background

    def exclude_border(self, mask: np.ndarray, margin: int = 10) -> np.ndarray:
        """
        Add mergine to the 4 sides of the frame
        """
        h, w = mask.shape
        new_mask = mask.copy()
        new_mask[:margin, :] = 0
        new_mask[-margin:, :] = 0
        new_mask[:, :margin] = 0
        new_mask[:, -margin:] = 0
        return new_mask

    def annotated_frame(self, frame):
        result = self.model.track(frame)[0]
        return result
