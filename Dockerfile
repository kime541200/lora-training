FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu128
COPY requirements.docker.txt /tmp/req.txt
RUN pip install --no-cache-dir -r /tmp/req.txt onnxruntime-gpu pillow
WORKDIR /work
