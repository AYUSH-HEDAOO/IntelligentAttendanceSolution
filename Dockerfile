# Use an official Python runtime as the base image
FROM python:3.10.4-buster

# Set the working directory in the container
WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV IAS_SETTINGS_IN_DOCKER true

# Install dependencies
RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && pip install virtualenvwrapper poetry==1.4.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
# Ensure the correct path to the dlib wheel file or remove this line if not required
COPY ["pyproject.toml", "./"]
# Connection pool is full, discarding connection: pypi.org. Connection pool size: 10
RUN poetry config installer.max-workers 20
RUN apt-get update && apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev
RUN poetry add dlib
RUN poetry install --no-root --no-interaction --no-ansi -vvv
RUN poetry env info

# Copy project files
COPY ["README.md", "Makefile", "./"]
COPY staticfiles staticfiles
COPY IAS IAS
COPY shape_predictor_68_face_landmarks.dat shape_predictor_68_face_landmarks.dat

# Expose the Django development server port (change port if needed)
EXPOSE 8000

# Set up the entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
