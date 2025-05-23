# 🎥 yt_cli_scraper

An interactive YouTube video & channel downloader built with [yt-dlp](https://github.com/yt-dlp/yt-dlp), powered by Docker.

> 💡 **Note:**  
> This project is designed to work alongside [`bgutil-ytdlp-pot-provider`](https://github.com/Brainicism/bgutil-ytdlp-pot-provider),  
> which automates the collection of PO Tokens and supplies them to [`yt-dlp-get-pot`](https://github.com/coletdjnz/yt-dlp-get-pot).  
> 
> 📌 Learn more about [cases where a PO token is required](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide).
---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/theresatree/yt_cli_scraper.git
cd yt_cli_scraper
```

### 2. Build the Docker image
```bash
docker compose build
```

### 3. Run the yt-scraper image as cli.
```bash
docker compose run --rm yt-scraper
```

## 📁 Output

All downloaded videos are saved into a Docker-managed volume (`videos-data`).  
To copy the files to your local machine after a run:

### 💡 Optional: Change back to a host bind mount

If you want downloaded videos to appear directly on your host:
Adjust the `volumes` section in `docker-compose.yml`

```yaml
volumes:
  - ./videos:/app/videos
