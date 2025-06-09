FROM python:3.11-slim

WORKDIR /app

# System dependencies (for ffmpeg and build tools if needed)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Always install the latest versions of these 3 tools
RUN pip install --no-cache-dir --force-reinstall --upgrade \
    yt-dlp-get-pot \
    bgutil-ytdlp-pot-provider

RUN pip install --no-cache-dir --upgrade --pre "yt-dlp[default]"

COPY . .

CMD ["python", "main.py"]
