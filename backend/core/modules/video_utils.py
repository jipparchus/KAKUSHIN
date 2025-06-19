import os
import cv2
import numpy as np
import subprocess
from backend.config import load_config


def standardize_fsize(frame, target_size=640):
    """
    Standardize the frame size to 640x640 pixels for YOLOv11.
    Resize while keeping the aspect ratio. Padding the frame with black pixels.
    """
    h, w = frame.shape[:2]
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    # resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    resized = cv2.resize(frame, (new_w, new_h))
    # Create a blank canvas with padding
    # If grayscale image
    if len(frame.shape) == 2:
        padded_frame = np.ones((target_size, target_size), dtype=np.uint8) * 128  # Gray padding
    else:
        padded_frame = np.ones((target_size, target_size, 3), dtype=np.uint8) * 128  # Gray padding
    pad_top = (target_size - new_h) // 2
    pad_left = (target_size - new_w) // 2
    padded_frame[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = resized

    return padded_frame


def standardize_fsize_coord_conversion(videosize, target_size=640, coords=(0, 0)):
    """
    coordinates conversion from coords after standardising to that of the before.
    """
    w, h = videosize
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    pad_top = (target_size - new_h) // 2
    pad_left = (target_size - new_w) // 2
    # Coordinates in the standardized frame
    x, y = coords
    x -= pad_left
    y -= pad_top
    x /= scale
    y /= scale
    return (round(x), round(y))


"""
Video Depth Estimation
"""


def get_depth_video(video_path):
    config = load_config()
    # Script directory
    model = 'vits'  # Large: 'vitl', Small: 'vits'
    max_res = 720
    # max_res = 1280
    fps = 10
    scrpt_path = os.path.abspath('scripts')
    input_path = os.path.abspath(video_path)
    output_path = os.path.split(input_path)[0]
    cmd_clone_vda = os.path.join(scrpt_path, 'clone_vda.sh')
    cmd_init_vda = os.path.join(scrpt_path, 'init_vda.sh')
    cmd_vda = os.path.join(scrpt_path, 'get_depth_video.sh')

    # Clone Video-Depth-Anything repository
    if 'Video-Depth-Anything' not in os.listdir(config['paths']['models']):
        try:
            process_clone = subprocess.Popen(
                ['bash', cmd_clone_vda],
                stdout=subprocess.PIPE
            )
            process_clone.wait()
            process_init = subprocess.Popen(
                ['bash', cmd_init_vda],
                stdout=subprocess.PIPE
            )
            process_init.wait()
        except RuntimeError:
            print('RuntimeError: Clone the Video-Depth-Anything model')

    # Use Video-Depth-Anything small or large model
    print('#' * 30)
    print('model: ', model)
    print('Start the process ...')
    try:
        process = subprocess.Popen(
            ['bash', cmd_vda, input_path, output_path, model, str(max_res), str(fps)],
            stdout=subprocess.PIPE
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        print('Video - Depth - Anything finished the proicess!')
        print('#' * 30)

    except RuntimeError:
        print('Error in video depth estimation.')
