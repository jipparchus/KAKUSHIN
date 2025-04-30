#!/bin/bash
VENV_DIR="../env/venv_vda"

# bash clone_vda.sh

echo "Input video: $1"
echo "Output: $2"
echo "Model: $3"
echo "Max res: $4"
echo "FPS: $5"
echo "Starting depth estimation ..."
source "$VENV_DIR/bin/activate"

cd ./core/models/Video-Depth-Anything
python run.py --input_video $1 --output_dir $2 --encoder $3 --save_npz --max_res $4 --target_fps $5
# python run.py --input_video $1 --output_dir $2 --encoder $3 --save_npz --input_size 384 --max_res 720 --target_fps 10

# cd ../../..
# Deactivate the virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi
