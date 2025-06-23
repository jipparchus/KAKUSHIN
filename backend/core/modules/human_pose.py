import os
import pickle

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

save_annotated_video = True
video_name = '1StarChoss_trimmed.mp4'

direc_assets = 'E:/KAKUSHIN/assets/52620528-304a-42ce-a72a-5bbce84c1e71'
direc_video = os.path.join(direc_assets, video_name)


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
drawing_styles = mp.solutions.drawing_styles


def get_3dpose(direc_video=direc_video, save=True, get_2dpose=True):
    direc_saveas_3d = str(direc_video.split('.')[0]) + '_3dpose.pkl'
    direc_saveas_3d_cnf = str(direc_video.split('.')[0]) + '_3dpose_confidence.pkl'
    direc_saveas_2d = str(direc_video.split('.')[0]) + '_2dpose.pkl'
    direc_saveas_2d_cnf = str(direc_video.split('.')[0]) + '_2dpose_confidence.pkl'

    def adaptive_thld(img):
        (r, g, b) = cv2.split(img)
        r = cv2.adaptiveThreshold(r, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
        g = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
        b = cv2.adaptiveThreshold(b, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 20)
        return cv2.merge((r, g, b))

    def get_img_coords_pose(coords2d, t):
        df_pose2d = pd.DataFrame(columns=['X', 'Y'])
        df_pose2d['X'] = np.array(coords2d[t][:, 0])*nx
        df_pose2d['Y'] = np.array(coords2d[t][:, 1])*ny
        img_coords_pose = []
        for i in df_pose2d.index:
            img_coords_pose.append(list(df_pose2d.loc[i, ['X', 'Y']]))
        del df_pose2d
        return np.array(img_coords_pose).astype('float32')

    cap = cv2.VideoCapture(direc_video)

    if save_annotated_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
                os.path.join(
                    direc_assets,
                    video_name.split('.')[0] + '_humanpose.mp4'
                    ), fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))
                )
            )

    coords3d = []
    coords2d = []
    coords3d_confidence = []
    coords2d_confidence = []

    with mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
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

                if save_annotated_video:
                    mp_drawing.draw_landmarks(img2show, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1),
                                              mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3))
                    mp_drawing.draw_landmarks(img2show, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=0),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
                    mp_drawing.draw_landmarks(img2show, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=0),
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
                    img2show = cv2.cvtColor(img2show, cv2.COLOR_RGB2BGR)
                    out.write(img2show)

            except AttributeError:
                break

        coords3d, coords2d = np.array(coords3d), np.array(coords2d)

        cap.release()
        if save_annotated_video:
            out.release()
        cv2.destroyAllWindows()

    if save:
        with open(direc_saveas_3d, 'wb') as f:
            pickle.dump(coords3d, f)

        with open(direc_saveas_3d_cnf, 'wb') as f:
            pickle.dump(coords3d_confidence, f)

        if get_2dpose:
            with open(direc_saveas_2d, 'wb') as f:
                pickle.dump(coords2d, f)

            with open(direc_saveas_2d_cnf, 'wb') as f:
                pickle.dump(coords2d_confidence, f)

    return coords3d, coords2d, coords3d_confidence, coords2d_confidence


if __name__ == '__main__':
    get_3dpose()
