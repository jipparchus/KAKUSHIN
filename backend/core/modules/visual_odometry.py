import os

from backend.core.modules.video_utils import get_depth_video
from backend.core.modules.data_objects import VideoData


def rgbd_vo(rgb_video: VideoData):
    """
    Vision Odometry by RGBD images.
    """
    get_depth_video(rgb_video.path)
    # Delete the original high fps video, and return
    rgb_video_path = rgb_video.path
    del rgb_video
    os.remove(rgb_video_path)

    # Load the low FPS version of the rgb_video
    (head, basename) = os.path.split(rgb_video_path)
    video = VideoData(os.path.join(head, basename.replace('.mp4', '_src.mp4')))
    video.get_point_cloud()
    return video.path_pointcloud
