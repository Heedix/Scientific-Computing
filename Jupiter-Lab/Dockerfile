FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLCONFIGDIR=/tmp/matplotlib \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash gcc libc6-dev openmpi-bin libopenmpi-dev maxima-sage maxima-sage-share pari-gp libpari-dev \
    && ln -s /usr/bin/maxima-sage /usr/local/bin/maxima \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt \
    && python -m ipykernel install --prefix=/usr/local --name python3 --display-name "Python 3 (Scientific Computing)" \
    && python -m bash_kernel.install --sys-prefix \
    && useradd --create-home --uid 1000 student \
    && mkdir -p /workspace && chown student:student /workspace

USER student
WORKDIR /workspace
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.root_dir=/workspace"]
