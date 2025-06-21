# Use NVIDIA PyTorch image as base
FROM nvcr.io/nvidia/pytorch:23.07-py3

# ENV DEBIAN_FRONTEND=noninteractive
# Install basic tool
RUN apt-get update && apt-get install -y wget


# Install Conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /opt/miniconda && \
    rm ~/miniconda.sh

# Set Conda in the PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Create a new Conda environment (Python 3.10)
RUN conda create -n kakushin python=3.10 -y

# Set Conda environment activation
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc
RUN echo "conda activate kakushin" >> ~/.bashrc

# Install necessary packages inside Conda environment
RUN conda install -n kakushin -y pip numpy opencv && \
    /opt/miniconda/bin/pip install torch_geometric

# Default to using Conda environment
ENV CONDA_DEFAULT_ENV=kakushin
ENV PATH="/opt/miniconda/envs/kakushin/bin:$PATH"

# Install FFmpeg and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libgl1-mesa-glx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /backend

# Install python package dependencies
RUN python -m pip install --upgrade pip
COPY /backend/requirements.txt ./requirements.txt
RUN conda run -n kakushin pip install --no-cache-dir -r requirements.txt

# Set Python path
ENV PYTHONPATH=/backend

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
# --host 0.0.0.0: the server will listen to ALL internal IPs inside container
# EXPOSE 8000: tells docker that container will open 8000
CMD ["conda", "run", "--no-capture-output", "-n", "kakushin", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
