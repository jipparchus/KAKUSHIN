import numpy as np
import cv2
from scipy.interpolate import UnivariateSpline

from backend.core.modules.data_objects import CameraData


def spline_smoothing(x, y, lam=None, k=3):
    mask = ~np.isnan(y)
    x_valid = x[mask]
    y_valid = y[mask]

    # lam: smoothing factor
    s = lam if lam is not None else len(x_valid)
    spline = UnivariateSpline(x_valid, y_valid, s=s, k=k)
    return spline


def polar2cartesian_xz(r, theta):
    """
    Get camera cartesian coordinates (only on X-Z plane) fropm ploar representation
    r: distance from the global origin [m]
    theta: angle [deg]. +z to +x axis is +theta.
    """
    theta = np.deg2rad(theta)
    x = r * np.sin(theta)
    z = r * np.cos(theta)
    return x, z


def cylindrical2cartesian(r, theta, height, vector_fmt=False):
    """
    Obtain cartesian position vector from the cylindrical coordinates
    """
    x, z = polar2cartesian_xz(r, theta)
    y = height
    if vector_fmt:
        return np.array([[x], [y], [z]])
    else:
        return x, y, z


def compute_transformation_matrix(A, B):
    """
    Transformation from A -> B
    """
    # Center the points
    A_centered = A - np.mean(A, axis=0)
    B_centered = B - np.mean(B, axis=0)

    # Compute the covariance matrix
    H = np.dot(A_centered.T, B_centered)

    # Perform SVD
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # Ensure a right-handed coordinate system
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    # Compute the translation
    t = np.mean(B, axis=0) - np.dot(R, np.mean(A, axis=0))

    # Create the transformation matrix
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T


def compute_translation(A, B):
    """
    Translation from A -> B
    """
    # Center the points
    A_centered = np.mean(A, axis=0)
    B_centered = np.mean(B, axis=0)
    M = B_centered - A_centered
    return np.array([[m, ] for m in M])


def coords_transformation_3D(coords3d, Ts: list):
    """
    coords3d: 3D coordinates to transform
    Ts: List of transformation matrix. Aplied from the head of the list
    """
    pose_global = []
    for kp in coords3d:
        xx, yy, zz = kp
        for M in Ts:
            xx, yy, zz, _ = M @ [xx, yy, zz, 1]
        pose_global.append([xx, yy, zz])
    return np.array(pose_global)


def solvePnP(world_coords, img_coords, cameradata: CameraData, **kwargs):
    """
    PnP solver for the wall and human pose
    world_coords: 3d coordinates of points
    img_coords: 2d coordinates of the same set of the points
    cameradata: CameraData instance containing information of the camera intrinsic matrix and distortion coefficients
    """
    vervose = kwargs.pop('vervose', False)
    success, rvec, tvec, inliers = cv2.solvePnPRansac(
        world_coords,
        img_coords,
        cameradata.intrinsic_matrix,
        cameradata.distortion_coeff,
        flags=cv2.SOLVEPNP_ITERATIVE,
        reprojectionError=8.0,
        confidence=0.99
    )

    if success:
        if vervose:
            print("Rotation Vector:\n", rvec)
            print("Translation Vector:\n", tvec)
        return rvec, tvec
    else:
        print("PnP RANSAC failed.")
        return None, None
