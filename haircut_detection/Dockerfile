# https://saturncloud.io/blog/how-to-install-pytorch-on-the-gpu-with-docker/
# https://github.com/anibali/docker-pytorch

FROM anibali/pytorch:2.0.1-cuda11.8-ubuntu22.04

# Set up time zone.
ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

# Install system libraries required by OpenCV.
RUN sudo apt-get update \
 && sudo apt-get install -y libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
 && sudo rm -rf /var/lib/apt/lists/*

# Install OpenCV from PyPI.
RUN pip install opencv-python==4.5.1.48