import numpy as np
import cv2


def get_camera_matrix(images: list):
    # Define checkerboard properties
    CHECKERBOARD = (9, 6)  # (internal corners per row, per column)
    square_size = 0.015  # Set the square size in meters (e.g., 2.5cm = 0.025m)

    # Arrays to store object points and image points
    objpoints = []  # 3D world points
    imgpoints = []  # 2D image points
    imgs_annotated = []  # Annotated images

    # Define real-world 3D points for the checkerboard
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * square_size

    for img_bytes in images:
        img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect checkerboard corners
        ret, corners = cv2.findChessboardCorners(
            gray,
            CHECKERBOARD,
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH +
            cv2.CALIB_CB_FAST_CHECK +
            cv2.CALIB_CB_NORMALIZE_IMAGE
        )

        if ret:
            print(f"✅ Pattern detected in {img}")
            imgs_annotated.append(draw_calibration_overlay(img, corners, CHECKERBOARD))
            objpoints.append(objp)
            imgpoints.append(corners)
        else:
            print(f"❌ Pattern NOT detected in {img}")

    # Camera calibration
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        # print("\nCamera Matrix (K):\n", K)
        fx, fy = K[0, 0], K[1, 1]
        cx, cy = K[:2, 2]
        # distortion coefficient
        dist = list(dist[0])
        return {
            'fx': fx,
            'fy': fy,
            'cx': cx,
            'cy': cy,
            'dist_coeffs': dist,
        }, imgs_annotated
    else:
        return None


def draw_calibration_overlay(img, corners, pattern_size):
    # Draw chessboard corners
    cv2.drawChessboardCorners(img, pattern_size, corners, True)

    # Encode back to JPEG
    success, encoded_img = cv2.imencode('.jpg', img)
    return encoded_img.tobytes() if success else None


def get_extrinsic_matrix(rvec, tvec):
    """
    Extrinsic matrix
    """
    T = np.eye(4)
    R, _ = cv2.Rodrigues(rvec)
    T[:3, :3] = R
    T[:3, 3] = tvec.flatten()
    return T
