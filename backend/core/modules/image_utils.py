import numpy as np
import cv2

# Image pre-processing functions


def gammaCorrection(src):
    #  ratio of the log(mid)/log(mean)
    mid = 0.3
    mean = np.mean(src)
    gamma = np.log(mid * 255) / np.log(mean)

    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


def invert(src):
    """
    Inverted grey image
    """
    return cv2.bitwise_not(src)


def draw_yolo_detections(frame, results):
    """
    frame: np.ndarray
    results: detection result from YOLO (must include boxes, class names, etc.)

    Returns: Annotated frame
    """
    for det in results:
        x1, y1, x2, y2 = map(int, det['box'])
        label = det['label']
        conf = det['confidence']

        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Draw label and confidence
        text = f"{label} {conf:.2f}"
        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return frame
