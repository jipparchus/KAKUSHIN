

def coords_converter(src, conversion):
    """
    src: coords to be converted
    Coordinate system conversions for the pairs:
        'blender-opencv',
        'mediapipe-opencv',
        'opencv-matplotlib',
        'matplotlib-opencv'
        'blender-matplotlib',
        'mediapipe-matplotlib',
    """
    conversion_memu = [
            'blender-opencv',
            'mediapipe-opencv',
            'opencv-matplotlib',
            'matplotlib-opencv',
            'blender-matplotlib',
            'mediapipe-matplotlib',
            ]
    if conversion not in conversion_memu:
        raise ValueError(
            f"coords_from must be one of {conversion_memu}"
            )

    if len(src) != 3:
        raise ValueError('The input coordinates must be 3D cartesian')

    c0, c1, c2 = src
    if conversion in ['blender-opencv', 'mediapipe-opencv']:
        return c0, -c2, c1
    elif conversion in ['opencv-matplotlib', 'matplotlib-opencv']:
        return c0, -c1, c2
    elif conversion in ['blender-matplotlib', 'mediapipe-matplotlib']:
        return c0, c2, c1
