import os
import gc
import pickle
import random
from dataclasses import dataclass
import cv2
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import copy
import mediapipe as mp


from core.modules.video_utils import standardize_fsize
from core.modules.mask_utils import Masker


@dataclass
class CameraData:
    matrix_dict: dict

    def __post_init__(self):
        self.fx = self.matrix_dict['fx']
        self.fy = self.matrix_dict['fy']
        self.cx = self.matrix_dict['cx']
        self.cy = self.matrix_dict['cy']

        self.intrinsic_matrix = np.array(
            [[self.fx, 0, self.cx],
             [0, self.fy, self.cy],
             [0, 0, 1]]
        )
        self.distortion_coeff = self.matrix_dict['dist_coeffs']


@dataclass
class VideoData:
    path: str

    def __post_init__(self):
        self.head_path, self.name = os.path.split(self.path)
        self.path_depths = self.path.replace('src.mp4', 'depths.npz')
        # self.path_pointcloud = self.path.replace('src.mp4', 'ptc.ply')
        self.path_pointcloud = self.path.replace('src.mp4', 'ptc.ply')
        self.vcap = cv2.VideoCapture(self.path)
        if not self.vcap.isOpened():
            raise IOError(f"Cannot open video at {self.path}")
        self.total_frames = int(self.vcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.vcap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def __len__(self):
        return self.total_frames

    def clone(self):
        # Useful when accessing different frames of the same video at the same time.
        return cv2.VideoCapture(self.path)

    def load_frame(self, frame_num):
        """
        Seek and return specific frame.
        """
        if frame_num < 0 or frame_num >= self.total_frames:
            raise IndexError("Frame number out of range")

        self.vcap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.vcap.read()
        if not ret:
            raise RuntimeError(f"Failed to read frame {frame_num}")
        return frame

    def iter_frames(self, start=0, end=None, step=1):
        """
        Generator to yield frames between [start, end)
        """
        if end is None:
            end = self.total_frames

        for i in range(start, end, step):
            yield self.load_frame(i)

    def iter_frames_streaming(self, max_frames=None):
        """
        Efficient frame reader without seek (streaming).
        Only works from beginning to end.
        """
        count = 0
        self.vcap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while self.vcap.isOpened():
            ret, frame = self.vcap.read()
            if not ret:
                break
            yield frame
            count += 1
            if max_frames and count >= max_frames:
                break

    def iter_random_frames(self, selectn=5, resize=False):
        """
        Sample frames to be annotated. Selection of frames is random
        """
        try:
            nf = random.sample(range(0, self.total_frames), selectn)
        except ValueError:
            print(f'Number of samples ({selectn}) > Number of total frames ({self.total_frames})')

        for i in nf:
            frame = self.load_frame(i)
            if resize:
                yield standardize_fsize(frame)
            else:
                yield frame

    def get_human_pose(self):
        human_pose = HumanPose(video=self)
        coords3d, coords2d, coords3d_confidence, coords2d_confidence = human_pose.get_3dpose(save=True, get_2dpose=True)

    def get_point_cloud(self):

        cam = {
            "fx": 1353.6915950245486,
            "fy": 1357.5577115711324,
            "cx": 538.9620188123179,
            "cy": 961.5329984766928,
            "dist_coeffs": [
                0.045870044322073686,
                -0.39564683084494173,
                -0.0020515588805692024,
                0.0015103837799576112,
                1.0718061310340865
            ]
        }
        camera = CameraData(cam)
        yolomodel = 'core/models/best.pt'
        masker = Masker(yolomodel)
        merged_pcd = o3d.geometry.PointCloud()
        pointcloud = PointCloudData(camera=camera, video=self, masker=masker)
        pcds = []
        # for i in range(self.total_frames):
        for i in [0, 20, 40]:
            pcd = pointcloud.rgbd_to_pointcloud(i)
            # Remove statistical outlier
            pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=1.0)
            pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=100, std_ratio=1.5)
            pcds.append(pcd)

        pose_graph = pointcloud.multiway_registration(pcds)
        merged_pcd = pointcloud.merge_aligned_pcds(pcds, pose_graph)
        o3d.io.write_point_cloud(self.path_pointcloud, merged_pcd)

        max_plane_id = 1
        pt_to_plane_dist = 0.01
        segment_models = {}
        segments = {}
        rest_pcd = merged_pcd

        # https://youtu.be/-OSVKbSsqT0?si=xsOuF2fhJRy-N5KX

        for i in range(max_plane_id):
            # colors = plt.get_cmap('tab20')(i)
            try:
                segment_models[i], inliers = rest_pcd.segment_plane(distance_threshold=pt_to_plane_dist, ransac_n=3, num_iterations=1000)
                segments[i] = rest_pcd.select_by_index(inliers)
                # segments[i].paint_uniform_color(list(colors[:3]))
                rest_pcd = rest_pcd.select_by_index(inliers, invert=True)
            except RuntimeError:
                pass
        if len(segments) > 0:
            planes_pcd = o3d.geometry.PointCloud()
            for i in range(max_plane_id):
                if segments[i] is not None:
                    planes_pcd += segments[i]
            # planes_pcd += rest_pcd
            o3d.io.write_point_cloud('plane.ply', planes_pcd)

            # Pattern Match with model
            model_mesh = o3d.io.read_triangle_mesh("../database/MB2024.obj")
            model_pcd = model_mesh.sample_points_poisson_disk(number_of_points=100000)  # or uniform
            model_pcd.estimate_normals()

            scan_bbox = planes_pcd.get_max_bound() - planes_pcd.get_min_bound()
            model_bbox = model_pcd.get_max_bound() - model_pcd.get_min_bound()
            scale_ratio = scan_bbox.max() / model_bbox.max()
            model_pcd.scale(scale_ratio, center=model_pcd.get_center())
            o3d.io.write_point_cloud('model.ply', model_pcd)

            # threshold = 0.05  # 5cm以内の最近傍点だけ使う
            # trans_init = np.identity(4)

            # reg_p2p = o3d.pipelines.registration.registration_icp(
            #     planes_pcd, model_pcd,
            #     threshold,
            #     trans_init,
            #     o3d.pipelines.registration.TransformationEstimationPointToPlane()
            # )

            # print("Transformation Matrix:")
            # print(reg_p2p.transformation)

            # # 点群を整合後に変換
            # aligned_scan = planes_pcd.transform(reg_p2p.transformation)
            # o3d.io.write_point_cloud('test.ply', aligned_scan + model_pcd)

            # del merged_pcd, depths
        return self.path_pointcloud

    def release(self):
        self.vcap.release()

    def __del__(self):
        try:
            self.release()
        except:
            pass


@dataclass
class HumanPose:
    video: VideoData

    def __post_init__(self):
        self.pose_video = self.video.path.replace('.mp4', '_humanpose.mp4')
        self.direc_saveas_3d = self.video.path.replace('.mp4', '_3dpose.pkl')
        self.direc_saveas_3d_cnf = self.video.path.replace('.mp4', '_3dpose_confidence.pkl')
        self.direc_saveas_2d = self.video.path.replace('.mp4', '_2dpose.pkl')
        self.direc_saveas_2d_cnf = self.video.path.replace('.mp4', '_2dpose_confidence.pkl')

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.drawing_styles = mp.solutions.drawing_styles
        print('HumanPose initialised')

    def get_3dpose(self, save=True, get_2dpose=True):

        def adaptive_thld(img):
            (r, g, b) = cv2.split(img)
            r = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
            g = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
            b = cv2.adaptiveThreshold(b, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
            return cv2.merge((r, g, b))

        if save:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.pose_video, fourcc, 30.0, (int(self.video.vcap.get(3)), int(self.video.vcap.get(4))))

        coords3d = []
        coords2d = []
        coords3d_confidence = []
        coords2d_confidence = []

        with self.mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4) as holistic:
            for frame in self.video.iter_frames_streaming():
                # while self.video.vcap.isOpened():
                #     ret, frame = self.video.vcap.read()
                try:
                    nx, ny, nz = frame.shape

                    def coords_conversion(array):
                        return tuple(np.multiply(array, [ny, nx]).astype(int))
                    # BGR to RGB
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img2show = cv2.addWeighted(src1=img, alpha=0.9, src2=adaptive_thld(img), beta=0.1, gamma=0)
                    # Detection
                    results = holistic.process(img2show)

                    landmarks_3d = [results.pose_world_landmarks.landmark[lm] for lm in mp.solutions.pose.PoseLandmark]
                    coords3d.append(np.array([(lm.x, lm.y, lm.z) for lm in landmarks_3d]))
                    coords3d_confidence.append(np.array([lm.visibility for lm in landmarks_3d]))

                    if get_2dpose:
                        landmarks_2d = [results.pose_landmarks.landmark[lm] for lm in mp.solutions.pose.PoseLandmark]
                        coords2d.append(np.array([(lm.x, lm.y) for lm in landmarks_2d]))
                        coords2d_confidence.append(np.array([lm.visibility for lm in landmarks_2d]))

                    if save:
                        self.mp_drawing.draw_landmarks(img2show, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                                       self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1),
                                                       self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3))
                        self.mp_drawing.draw_landmarks(img2show, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=0),
                                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
                        self.mp_drawing.draw_landmarks(img2show, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=0),
                                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
                        img2show = cv2.cvtColor(img2show, cv2.COLOR_RGB2BGR)
                        out.write(img2show)

                except AttributeError:
                    break

            coords3d, coords2d = np.array(coords3d), np.array(coords2d)

            self.video.vcap.release()
            if save:
                out.release()
            cv2.destroyAllWindows()

        if save:
            with open(self.direc_saveas_3d, 'wb') as f:
                pickle.dump(coords3d, f)

            with open(self.direc_saveas_3d_cnf, 'wb') as f:
                pickle.dump(coords3d_confidence, f)

            if get_2dpose:
                with open(self.direc_saveas_2d, 'wb') as f:
                    pickle.dump(coords2d, f)

                with open(self.direc_saveas_2d_cnf, 'wb') as f:
                    pickle.dump(coords2d_confidence, f)

        return coords3d, coords2d, coords3d_confidence, coords2d_confidence


@dataclass
class PointCloudData:
    camera: CameraData
    video: VideoData
    masker: Masker

    def __post_init__(self):
        depth_array = np.load(self.video.path_depths, mmap_mode='r')
        self.depths = depth_array['depths']  # shape = (nt, ny, nx)
        nt, depth_ny, depth_nx = self.depths.shape
        scale_x = depth_nx / self.video.width
        scale_y = depth_ny / self.video.height
        self.intrinsic = o3d.camera.PinholeCameraIntrinsic()
        self.intrinsic.set_intrinsics(
            width=self.video.width,
            height=self.video.height,
            fx=self.camera.fx * scale_x, fy=self.camera.fy * scale_y,
            cx=self.camera.cx * scale_x, cy=self.camera.cy * scale_y)

    def get_rgbd(self, frame_num: int):
        """
        Create RGB-D frames from rgb frames and depth array
        Parameters:
            frame_num: Frame number
        """
        print('RGBD frames')
        # Obtain point cloud from a single image and corresponding depth array
        rgb_frame = cv2.cvtColor(self.video.load_frame(frame_num), cv2.COLOR_BGR2RGB)
        depth_np = self.depths[frame_num].astype(np.float32)

        # Resize RGB frame to the size of the depth array
        rgb_resized = cv2.resize(rgb_frame, (depth_np.shape[1], depth_np.shape[0]))

        # Apply mask
        depth_np[self.masker.apply_mask(rgb_resized, 0.3, cls2include=[0], cls2exclude=[1, 2]) == 0] = 0

        # Convert the inverse depth to depth
        depth_metric = 1.0 / (depth_np + 1e-6)
        print(f'depth_metric max: {np.max(depth_metric)}')
        print(f'depth_metric min: {np.min(depth_metric)}')
        color_o3d = o3d.geometry.Image(rgb_resized)
        depth_o3d = o3d.geometry.Image(depth_metric)
        # RGBD image
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color_o3d, depth_o3d,
            depth_scale=1.0, convert_rgb_to_intensity=False
        )
        return rgbd

    def rgbd_to_pointcloud(self, frame_num: int, **kwargs):
        """
        Parameters:
            frame_num: Frame number
            kwargs: downsample_voxel_size: float
        """
        rgbd = self.get_rgbd(frame_num)
        downsample_voxel_size = kwargs.pop('downsample_voxel_size', None)
        print('RGBD to point cloud')
        # Point cloud creation
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, self.intrinsic)
        if downsample_voxel_size is not None:
            pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size)  # Downsampling
        print(f'#points: {len(pcd.points)}')

        return pcd

    def pairwise_registration(
            self,
            source: o3d.geometry.PointCloud,
            target: o3d.geometry.PointCloud,
            estimation_method: str = 'color'
    ):
        """
        Align source point cloud -> target point cloud
        https://www.open3d.org/docs/release/tutorial/t_pipelines/t_icp_registration.html#Colored-ICP-Registration
        If estimation_method is 'color': Iterate the fitting from large scle to small scale
        Else: find the transformation without iterative processes
        Returns: icp result, information matrix
        """
        print('Pairwise ICP: ', estimation_method)
        current_transformation = np.identity(4)
        if estimation_method == 'color':
            method = o3d.pipelines.registration.TransformationEstimationForColoredICP()
            # Try iterations with different scales from large to small
            voxel_radius = [0.02, 0.01, 0.001]
            max_iter = [50, 30, 15]
            for scale in range(len(voxel_radius)):
                iter = max_iter[scale]
                radius = voxel_radius[scale]
                print(f'Config: iterations {iter}, radius {radius}')

                # Downsample
                # source_down = source.voxel_down_sample(radius)
                # target_down = target.voxel_down_sample(radius)
                source_down = source
                target_down = target
                # Normal estimation
                source_down.estimate_normals(
                    o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30)
                )
                target_down.estimate_normals(
                    o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30)
                )
                print(f'Source #points: {len(source_down.points)}')
                print(f'Target #points: {len(target_down.points)}')
                result_icp = o3d.pipelines.registration.registration_icp(
                    source_down,
                    target_down,
                    radius,  # max_correspondance_distance
                    current_transformation,
                    method,
                    o3d.pipelines.registration.ICPConvergenceCriteria(
                        relative_fitness=1e-6,
                        relative_rmse=1e-6,
                        max_iteration=iter
                    )
                )
                # Update the current transformation
                current_transformation = result_icp.transformation
            max_correspondance_distance = radius

        else:
            max_correspondance_distance = 0.05
            # Point to plane ICP
            if estimation_method == 'point2plane':
                method = o3d.pipelines.registration.TransformationEstimationPointToPlane()
            # Point to point ICP
            elif estimation_method == 'point2point':
                method = o3d.pipelines.registration.TransformationEstimationPointToPoint()

            # Normal estimation
            source_down.estimate_normals(
                o3d.geometry.KDTreeSearchParamHybrid(radius=max_correspondance_distance * 2, max_nn=30)
            )
            target_down.estimate_normals(
                o3d.geometry.KDTreeSearchParamHybrid(radius=max_correspondance_distance * 2, max_nn=30)
            )

            result_icp = o3d.pipelines.registration.registration_icp(
                source,
                target,
                max_correspondance_distance,  # max_correspondance_distance
                current_transformation,
                method,
                o3d.pipelines.registration.ICPConvergenceCriteria(
                    relative_fitness=1e-6,
                    relative_rmse=1e-6,
                    max_iteration=50
                )
            )

        information_matrix = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
            source,
            target,
            max_correspondance_distance,
            result_icp.transformation
        )
        return result_icp, information_matrix

    def multiway_registration(
            self,
            pcds: list,
    ):
        """
        pcds: list of point cloud
        Registrer multiple scanes -> build a consistent global model
        https://www.open3d.org/docs/release/tutorial/pipelines/multiway_registration.html

        Frame-to-frame:
        → Pairwise local ICP
        → Store relative transforms {T_ij}

        Pose graph:
        → Build from pairs
        → Add loop closures

        Global optimization:
        → Minimise sum(norm(T_j*inv(T_i) - T_ij)^2)

        Apply final transforms + merge
        → Build consistent global model
        """
        # PoseGraph initialisation
        pose_graph = self.init_posegraph(pcds)
        max_correspondance_distance = 0.02
        option = o3d.pipelines.registration.GlobalOptimizationOption(
            max_correspondence_distance=max_correspondance_distance,
            edge_prune_threshold=0.25,
            reference_node=0
        )
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug):
            print('Optimising PoseGraph ...')
            o3d.pipelines.registration.global_optimization(
                pose_graph,
                o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
                o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
                option
            )
        return pose_graph

    def init_posegraph(self, pcds: list):
        """
        Registering the list of point cloud into the PoseGraph. Wrapper of 'multiway_registration_posegraph'
        Return: PoseGraph
        """
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug):
            print('Creating PoseGraph ...')
            pose_graph = self.multiway_registration_posegraph(pcds)
        return pose_graph

    def multiway_registration_posegraph(
            self,
            pcds: list,
    ):
        """
        PoseGraph creation
        """
        pose_graph = o3d.pipelines.registration.PoseGraph()
        odometry = np.identity(4)
        pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))
        n_pcds = len(pcds)

        # Get pairwise registrations
        for source_id in range(n_pcds):
            for target_id in range(source_id + 1, n_pcds):
                result_icp, information_matrix = self.pairwise_registration(
                    pcds[source_id],
                    pcds[target_id],
                    estimation_method='color'
                )
                if target_id == source_id + 1:  # odometry case
                    odometry = np.dot(result_icp.transformation, odometry)

                    # Node i
                    pose_graph.nodes.append(
                        o3d.pipelines.registration.PoseGraphNode(
                            np.linalg.inv(odometry)))
                    # Edge i-j
                    pose_graph.edges.append(
                        o3d.pipelines.registration.PoseGraphEdge(
                            source_id,
                            target_id,
                            result_icp.transformation,
                            information_matrix,
                            uncertain=False)
                    )
                else:  # loop closure case
                    pose_graph.edges.append(
                        o3d.pipelines.registration.PoseGraphEdge(
                            source_id,
                            target_id,
                            result_icp.transformation,
                            information_matrix,
                            uncertain=True)
                    )
        return pose_graph

    def merge_aligned_pcds(self, pcds: list, pose_graph):
        """
        Merge the point clouds aligned by multiway registration
        pcds: list of point cloud objects
        """
        print('Downsampling ...')
        voxel_size = 0.01
        pcd_combined = o3d.geometry.PointCloud()
        for point_id in range(len(pcds)):
            pcds[point_id].transform(pose_graph.nodes[point_id].pose)
            pcd_combined += pcds[point_id]
        # pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)
        # return pcd_combined_down
        return pcd_combined


# class Body:
#     def __init__(self, frame_number):
#         self.t = frame_number
#         self.mass = get_mass_all()
#         self.coords3d, self.coords2d = clean_coord(coords3d, coords2d)
#         self.coords3d_conf, self.coords2d_conf = coords3d_confidence, coords2d_confidence
#         # self.coords3d, self.coords2d = coords3d, coords2d
#         self.dict_com3d = get_com_part_simple(self.coords3d[self.t])
#         self.dict_com2d = get_com_part_simple(self.coords2d[self.t])
#         self.contact_points3d = ContactPoints(self.coords3d, self.t)
#         self.contact_points2d = ContactPoints(self.coords2d, self.t)
#         self.edges3d = get_edge_coords_all(self.coords3d[self.t])
#         self.edges2d = get_edge_coords_all(self.coords2d[self.t])
#         self.edges_col = get_edge_col_all()

#     def plot(self, ax):
#         for coords, col in zip(self.edges3d.values(), self.edges_col.values()):
#             p0, p1 = coords
#             xs, ys, zs = [p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]]
#             ax.plot(xs, ys, zs, c=col)

#         for point in self.contact_points3d.dict_points.values():
#             col = 'white'
#             if point['state'] == 1:
#                 col = 'orange'
#             x, y, z = point['coords']
#             ax.scatter(x, y, z, marker='o', c=col, edgecolors='k', s=30)

#         for key, val in self.dict_com3d.items():
#             x, y, z = val
#             ax.scatter(x, y, z, marker='o', c='green', edgecolors='k', s=50)
#         ax.set_xlabel("x")
#         ax.set_ylabel("y")
#         ax.set_zlabel("z")
#         return ax
