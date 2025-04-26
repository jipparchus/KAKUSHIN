
VENV_DIR="../env/venv_vda"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
cd ./core/models/Video-Depth-Anything
bash get_weights.sh

# cd ../../..
# Deactivate the virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi

echo "... Video-Depth-Anything initialisation complete ..."