import numpy as np
import mathutils
import bpy

from backend.core.modules.maths_utils import cylindrical2cartesian
from backend.core.modules.plot_utils import coords_converter


def make_camera_data(f_in_mm, scene):
    """
    scene: blender scene
    Returns: bpy.data.cameras
    """
    cam_data = bpy.data.cameras.new('Camera')
    cam_data.lens = f_in_mm
    sensor_w_in_mm = cam_data.sensor_width
    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100.0
    aspect_ratio = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x
    # Get pixel size
    resolution_x_in_px = res_x * scale
    resolution_y_in_px = res_y * scale
    # Focal length in pixels
    fx = f_in_mm / sensor_w_in_mm * resolution_x_in_px
    fy = fx / aspect_ratio
    # Principal point
    cx = resolution_x_in_px / 2 - cam_data.shift_x * resolution_x_in_px
    cy = resolution_y_in_px / 2 + cam_data.shift_y * resolution_y_in_px
    # Construct K
    K = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0,  0,  1]
    ])
    return cam_data, K


def place_camera_object(cam_data, r: float, theta: float, height: float, name: str):
    """
    cam_data: bpy.data.cameras
    r: Distance from the wall
    theta: Angle of the camera measured from the centre line
    height: Height of the camera
    """
    cam_obj = bpy.data.objects.new(name, cam_data)
    x, y, z = cylindrical2cartesian(r, theta, height)
    cam_obj.location = (x, y, z)
    cam_obj.rotation_mode = 'XYZ'
    cam_obj.rotation_euler = (np.deg2rad(0), np.deg2rad(theta), np.deg2rad(0))
    return cam_obj


def render_model(scene, camera, save_to=None):
    """
    camera: camera object
    """
    # Render from cam0
    scene.camera = camera

    if save_to is None:
        tmp_path = '/tmp/temp.png'
        import cv2
        from io import BytesIO
        import os
        # Save the rendered image to memory instead of writing to the disk
        # Create a BytesIO buffer
        buffer = BytesIO()
        # offscreen rendering
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGB'

        # don’t save to file automatically
        bpy.ops.render.render(write_still=False)
        # Get rendered image from Blender's internal buffer
        render_result = bpy.data.images['Render Result']
        # Convert to byte string, temporarily save
        render_result.save_render(filepath=tmp_path)

        # Ensure file exists and has content
        if not os.path.exists(tmp_path):
            raise FileNotFoundError(f"Render file not found at {tmp_path}")

        if os.path.getsize(tmp_path) == 0:
            raise ValueError(f"Render file is empty at {tmp_path}")

        # Read image into memory buffer
        with open(tmp_path, "rb") as f:
            file_data = f.read()

        if not file_data:
            raise ValueError("Failed to read image data from temporary render file.")

        buffer = BytesIO(file_data)
        buffer.seek(0)

        # Decode with OpenCV
        file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("OpenCV failed to decode image. File may be corrupted.")

        return img

    else:
        bpy.ops.render.render(write_still=True)
        bpy.data.images["Render Result"].save_render(filepath=save_to)


def pixel_to_world_ray(x, y, cam_obj, cam_intrinsics):
    """
    Calculate the ray vector in the camera direction originated from a point on the rendered image
    """
    fx = cam_intrinsics[0, 0]
    fy = cam_intrinsics[1, 1]
    cx = cam_intrinsics[0, 2]
    cy = cam_intrinsics[1, 2]

    # Convert to normalized device coords
    x_ndc = (x - cx) / fx
    y_ndc = (y - cy) / fy
    ray_camera = mathutils.Vector((x_ndc, -y_ndc, -1)).normalized()  # Blender uses -Z forward
    # ray_camera = mathutils.Vector((x_ndc, y_ndc, 1)).normalized()

    # Transform ray to world coordinates
    ray_world = cam_obj.matrix_world.to_3x3() @ ray_camera
    origin_world = cam_obj.matrix_world.to_translation()

    return origin_world, ray_world.normalized()


def intersect_ray_with_mesh(scene, origin, direction):
    """
    Coordinates of intersection with the rays from the feature points and the 3d mesh
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    result, location, normal, index, obj, matrix = scene.ray_cast(
        depsgraph, origin, direction
    )
    return location if result else None


def get_depth_ray_casting(coords2d, scene, cam_obj, K_blender):
    """
    coords2d: [[x, y], ...]
    scene: blender scene
    cam_obj: blender camera object
    K_blender: blender camera intrinsic matrix
    """
    coords3d = []
    for pt in coords2d:
        origin, direction = pixel_to_world_ray(pt[0], pt[1], cam_obj, K_blender)
        intersection = intersect_ray_with_mesh(scene, origin, direction)
        if intersection is not None:
            coords3d.append(intersection)
        else:
            coords3d.append(None)  # No hit
    return coords3d


def get_pair_2d_3d(pt_render, pt_videoframe, scene, cam_obj, K_blender):
    """
    Get 2d and 3d coordinates identified from the feature matching
    pt_render: 2d coordinates array from the mesh model. result of the feature mathcing
    pt_videoframe: 2d coordinates array from the video frame snapshot.
    """
    pt_ray_casting = get_depth_ray_casting(pt_render, scene, cam_obj, K_blender)
    pts_wld = []
    pts_img = []
    for coords_w, coords_i in zip(pt_ray_casting, pt_videoframe):
        if coords_w is not None:
            pts_wld.append([coords_w[0], coords_w[1], coords_w[2]])
            pts_img.append([coords_i[0], coords_i[1]])

    # blender coords -> opencv coords
    # pts_wld = np.array([coords_converter(coords, 'blender-opencv') for coords in pts_wld])
    pts_wld = np.array([coords_converter(coords, 'blender-matplotlib') for coords in pts_wld])
    pts_img = np.array(pts_img)
    return pts_img, pts_wld
