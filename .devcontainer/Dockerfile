# Base image with Python 3.12
FROM mcr.microsoft.com/devcontainers/python:3-3.12-trixie

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    graphviz \
    libmagic1 \
    build-essential \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set workdir (optional, VS Code mounts your repo anyway)
WORKDIR /workspace

# Upgrade pip
RUN pip install --upgrade pip