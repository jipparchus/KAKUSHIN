import numpy as np

KEYPOINTS = [
    'nose',
    'eye_i_l',
    'eye_l',
    'eye_o_l',
    'eye_i_r',
    'eye_r',
    'eye_o_r',
    'ear_l',
    'ear_r',
    'mouth_l',
    'mouth_r',
    'shoulder_l',
    'shoulder_r',
    'elbow_l',
    'elbow_r',
    'wrist_l',
    'wrist_r',
    'pinky_l',
    'pinky_r',
    'index_l',
    'index_r',
    'thumb_l',
    'thumb_r',
    'hip_l',
    'hip_r',
    'knee_l',
    'knee_r',
    'ankle_l',
    'ankle_r',
    'heel_l',
    'heel_r',
    'foot_index_l',
    'foot_index_r',
]

# CUSTOM_KEYPOINTS = [
#     'sacrum'
#     'coccyx'
#     'mid_spine'
#     'throat_btm'
# ]

# EDGES = {
#     'sc': ['sacrum', 'coccyx'],
#     'sp_b': ['sacrum', 'mid_spine'],
#     'sp_t': ['mid_spine', 'throat_btm'],
#     'nck': ['throat_btm', 'nose'],
#     'sh_l': ['throat_btm', 'shoulder_l'],
#     'sh_r': ['throat_btm', 'shoulder_r'],
#     'a_l': ['shoulder_l', 'elbow_l'],
#     'a_r': ['shoulder_r', 'elbow_r'],
#     'af_l': ['elbow_l', 'wrist_l'],
#     'af_r': ['elbow_r', 'wrist_r'],
#     'hp_l': ['coccyx', 'hip_l'],
#     'hp_r': ['coccyx', 'hip_r'],
#     'thigh_l': ['hip_l', 'knee_l'],
#     'thigh_r': ['hip_r', 'knee_r'],
#     'shin_l': ['knee_l', 'ankle_l'],
#     'shin_r': ['knee_r', 'ankle_r'],
#     'foot_top_l': ['ankle_l', 'foot_index_l'],
#     'foot_top_r': ['ankle_r', 'foot_index_r'],
#     'foot_btm_l': ['heel_l', 'foot_index_l'],
#     'foot_btm_r': ['heel_r', 'foot_index_r'],
#     'foot_heel_l': ['ankle_l', 'heel_l'],
#     'foot_heel_r': ['ankle_r', 'heel_r'],
# }

EDGES = {
    'sh': ['shoulder_l', 'shoulder_r'],
    'a_l': ['shoulder_l', 'elbow_l'],
    'a_r': ['shoulder_r', 'elbow_r'],
    'af_l': ['elbow_l', 'wrist_l'],
    'af_r': ['elbow_r', 'wrist_r'],
    'side_l': ['shoulder_l', 'hip_l'],
    'side_r': ['shoulder_r', 'hip_r'],
    'hp': ['hip_l', 'hip_r'],
    'thigh_l': ['hip_l', 'knee_l'],
    'thigh_r': ['hip_r', 'knee_r'],
    'shin_l': ['knee_l', 'ankle_l'],
    'shin_r': ['knee_r', 'ankle_r'],
    'foot_top_l': ['ankle_l', 'foot_index_l'],
    'foot_top_r': ['ankle_r', 'foot_index_r'],
    'foot_btm_l': ['heel_l', 'foot_index_l'],
    'foot_btm_r': ['heel_r', 'foot_index_r'],
    'foot_heel_l': ['ankle_l', 'heel_l'],
    'foot_heel_r': ['ankle_r', 'heel_r'],
    'face_l': ['eye_o_l', 'nose'],
    'face_r': ['eye_o_r', 'nose'],
}

PARTS = {
    'forearm_l': ['af_l'],
    'forearm_r': ['af_r'],
    'arm_l': ['a_l'],
    'arm_r': ['a_r'],
    'thigh_l': ['thigh_l'],
    'thigh_r': ['thigh_r'],
    'lowerleg_l': ['shin_l', 'foot_top_l', 'foot_btm_l', 'foot_heel_l'],
    'lowerleg_r': ['shin_r', 'foot_top_r', 'foot_btm_r', 'foot_heel_r'],
    'body': ['side_l', 'side_r', 'sh', 'hp'],
    'head': ['face_l', 'face_r']
}

color_map = {
    'eye': '#000000',
    'ear': '#000000',
    'mouth': '#000000',
    'nose': '#1f77b4',
    'shoulder': '#ff7f0e',
    'elbow': '#2ca02c',
    'wrist': '#d62728',
    'pinky': '#9467bd',
    'index': '#17becf',
    'thumb': '#8c564b',
    'hip': '#e377c2',
    'knee': '#7f7f7f',
    'ankle': '#bcbd22',
    'heel': '#17becf',
    'foot_index': '#1f77b4',
}


def get_plot_style(kp):
    for key in color_map:
        if key in kp:
            color = color_map[key]
            if kp.endswith('_l'):
                linestyle = 'solid'
            elif kp.endswith('_r'):
                linestyle = 'dashed'
            else:
                linestyle = 'dotted'
            return color, linestyle
    return 'black', 'solid'


def get_KEYPOINTS():
    return KEYPOINTS


def get_edges():
    return EDGES


def get_kp_idx(kp: str):
    """
    For a given keypoint return MediaPipe keypoint index
    """
    if kp in KEYPOINTS:
        idx = KEYPOINTS.index(kp)
    else:
        idx = np.nan
    return idx


def get_kp_coords(kpcoords, kp: str):
    return kpcoords[get_kp_idx(kp)]


def get_edge_coords(kpcoords, edge: str):
    """
    Parameters:
        kp_coords: List of coordinates
        edge: Name of the edge
    Return: 3D/2D coords of the two keypoints consist of the edge.
    """
    kp1, kp2 = EDGES[edge]
    return get_kp_coords(kpcoords, kp1), get_kp_coords(kpcoords, kp2)


def get_edge_coords_all(kpcoords):
    """
    Return all the edge coords as a dict
    """
    dict_edges = {}
    for edge in EDGES.keys():
        dict_edges[edge] = get_edge_coords(kpcoords, edge)
    return dict_edges


def get_edge_col(edge: str):
    col = 'black'
    if '_l' in edge:
        col = 'blue'
    elif '_r' in edge:
        col = 'red'
    return col


def get_edge_col_all():
    return {edge: get_edge_col(edge) for edge in EDGES.keys()}


def get_com_part_simple(coords):
    """
    Returns the mean of coordinates for parts in PARTS as dictionary
    """
    dict_com_parts = {}
    for part, edges in PARTS.items():
        if len(edges) == 1:
            com = np.mean(get_edge_coords(coords, edges[0]), axis=0)
        else:
            com = np.mean([np.mean(get_edge_coords(coords, edge), axis=0) for edge in edges], axis=0)
        dict_com_parts[part] = com
    # Total com as whole body
    coms = np.array([v for _, v in dict_com_parts.items()])
    dict_com_parts['total'] = np.mean(coms, axis=0)
    return dict_com_parts


def get_contact_coords(coords):
    return [get_kp_coords(coords, part)for part in ['wrist_l', 'wrist_r', 'foot_index_l', 'foot_index_r']]
