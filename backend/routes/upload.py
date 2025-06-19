import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Header
from auth.jwt_utils import decode_token
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from config import load_config
from db.dependency import get_db
from auth.dependencies import get_current_user
from db.models import CameraMatrix
from core.modules.cam_utils import get_camera_matrix
from core.modules.data_objects import VideoData
from core.modules.visual_odometry import rgbd_vo
from utils.img_tools import encode_images

router = APIRouter()


def get_user_id(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization[7:]
    decoded = decode_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Token invalid or expired")
    return decoded["user_id"]

# When accessed to the root URL


@router.post("/images")
async def upload_images(
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    mode: Optional[str] = Header(None),  # Get custom header 'mode'
):
    print('##########################')
    print(f"📦 Upload mode: {mode}")
    print('##########################')
    imgs_bytes = [await img.read() for img in images]
    status = '✅ upload: success'
    if mode == 'cam_calibration':
        result = get_camera_matrix(imgs_bytes)
        if result is not None:
            status += ' ✅ Calibration: success'
            comment = result[0]
            b64_images = encode_images(result[1])
            new_cam = CameraMatrix(
                user_id=current_user.id,
                camera_matrix=result[0],
            )
            db.add(new_cam)
            db.commit()  # generate an UPDATE SQL statement only for the fields that changed.
            db.refresh(current_user)
            response_content = {'status': status, 'comment': comment, 'images': b64_images}
        else:
            status += ' ❌ Calibration: fail'
            comment = None
            response_content = {'status': status, 'comment': comment}

    return JSONResponse(
        content=response_content,
    )


@router.post("/video")
async def upload_video(
    video: UploadFile = File(...),
    user_id: int = Depends(get_user_id)
):
    config = load_config()
    UPLOAD_DIR = config['paths']['assets']
    folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, video.filename)
    # Read bytes
    contents = await video.read()

    with open(filepath, "wb") as f:
        f.write(contents)

    del video
    video = VideoData(filepath)
    video.get_human_pose()
    # Do the core analyis
    # path_pointcloud = rgbd_vo(video)

    # return JSONResponse({"status": "success"})
    # return FileResponse(path_pointcloud, media_type='application/octet-stream', filename=os.path.basename(path_pointcloud))
    return StreamingResponse(open(filepath, "rb"),
                             media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=result.ply"}
                             )


# @app.post("/create-climb")
# def create_climb(climb: CreateClimb, db: Session = Depends(get_db)):
#     user = db.query(User).filter_by(id=climb.user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     new_climb = MyClimb(name=climb.name, user_id=user.id)
#     db.add(new_climb)
#     db.commit()
#     return {"status": "climb created", "climb_id": new_climb.id}
