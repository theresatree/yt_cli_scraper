import yt_dlp
from urllib.parse import urlparse
from dataclasses import dataclass
import os

########################################################## 
##########
##########              CLASS TO GET PARAMETERS 
##########            TO PASS TO YT_DLP TO INTERACT
##########
##########################################################

# -------------------------------
# 🎥 YouTube Video-Only Formats
# -------------------------------
# Format ID   Extensions   Resolution   Codec     Notes
# ----------  ----------  -----------  --------  ---------------------
# 160         mp4         144p         H.264     video only
# 133         mp4         240p         H.264     video only
# 134         mp4         360p         H.264     video only
# 135         mp4         480p         H.264     video only
# 136         mp4         720p         H.264     video only
# 137         mp4         1080p        H.264     video only
# 264         mp4         1440p        H.264     video only (rare)
# 266         mp4         2160p (4K)   H.264     video only (rare)
# 298         mp4         720p60       H.264     video only, 60fps
# 299         mp4         1080p60      H.264     video only, 60fps
# 278         webm        144p         VP9       video only
# 242         webm        240p         VP9       video only
# 243         webm        360p         VP9       video only
# 244         webm        480p         VP9       video only
# 247         webm        720p         VP9       video only
# 248         webm        1080p        VP9       video only
# 271         webm        1440p        VP9       video only
# 313         webm        2160p (4K)   VP9       video only
# 302         webm        720p60       VP9       video only, 60fps
# 303         webm        1080p60      VP9       video only, 60fps
# 308         webm        1440p60      VP9       video only, 60fps
# 315         webm        2160p60      VP9       video only, 60fps

# ------------------------------------------
# 🎬 YouTube Combined Video + Audio Formats
# ------------------------------------------
# Format ID   Extensions   Resolution   Codec             Notes
# ----------  ----------  -----------  ----------------  ---------------------
# 18          mp4         360p         H.264 + AAC       both video and audio
# 22          mp4         720p         H.264 + AAC       both video and audio
# 43          webm        360p         VP8 + Vorbis      legacy webm format
# 44          webm        480p         VP8 + Vorbis      legacy webm format
# 45          webm        720p         VP8 + Vorbis      legacy webm format
# 46          webm        1080p        VP8 + Vorbis      legacy webm format

@dataclass
class VideoParameters:
    channelOrVideo: str = ""
    resolution: str = ""
    extension: str = ""
    mode: str = ""
    url: str = ""
    num_downloads: int = 0  
    throttleDownloadSpeed: int = 2 # Default 2Mbps to prevent IP from being blocked

videoParameter = VideoParameters()

########################################################## 
##########
##########               BELOW ARE ALL THE 
##########             INTERFACE TO INTERACT.
##########
##########################################################

# ANSI escape codes for styles
ITALIC = "\033[3m"
RESET = "\033[0m"
RED = "\033[31m"

def startingInterface():
    clearCMD()
    print(f"{RED}Welcome to YT video downloader{RESET}\n")
    print("Select from the following options")
    print("=================================")
    print("1. Download a video from URL")
    print("2. Download from a channel")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in [1,2]:
            startingInterface()
        else:
            match (choice):
                case 1:
                    videoParameter.channelOrVideo = "video"
                case 2:
                    videoParameter.channelOrVideo = "channel"
            getURL(False)
    except ValueError:
        startingInterface()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def getURL(err: bool):
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}\n\n")
    print(f"Please enter the URL for the {videoParameter.channelOrVideo}")
    if err == True:
            print(f"{RED}Invalid URL!{RESET}")
    print("=====================================")
    try:
        choice = input("URL: ").strip()
        choice = str(choice)
        if is_valid_url(choice):
            videoParameter.url = choice
            if videoParameter.channelOrVideo == "video":
                selectVideoDownloadFormat()
            else:
                selectChannelExtension()
        else:
            getURL(True)
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)



def selectChannelExtension():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}\n\n")
    print("Select video extension")
    print(f"{RED}If unavailable, other extension will be chosen{RESET}")
    print("=================================")
    print("1. mp4")
    print("2. webm")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in range(1,3):
            selectChannelExtension()
        else:
            match (choice):
                case 1:
                    videoParameter.extension = "mp4"
                case 2:
                    videoParameter.extension = "webm"
            selectMode()
    except ValueError:
        startingInterface()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def selectMode():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}\n\n")
    print("Select download format")
    print("=================================")
    print("1. Video Only")
    print("2. Video + Audio")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in [1,2]:
            selectMode()
        else:
            match (choice):
                case 1:
                    videoParameter.mode = "v"
                case 2:
                    videoParameter.mode = "av"
            selectVideoQuality()
    except ValueError:
        selectMode()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def selectVideoQuality():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}")
    print(f"Mode: {videoParameter.mode}\n\n")
    print("Select video quality")
    print(f"{RED}If quality not available, next highest selected{RESET}")
    print(f"{RED}** Default means highest quality{RESET}")
    print("=================================")
    print("0. Default")
    print("1. 4K")
    print("2. 1440p")
    print("3. 1080p")
    print("4. 720p")
    print("5. 480p")
    print("6. 360p")
    print("7. 144p")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in range(0,8):
            selectVideoQuality()
        else:
            match (choice):
                case 1:
                    videoParameter.resolution = "2160"
                case 2:
                    videoParameter.resolution = "1440"
                case 3:
                    videoParameter.resolution = "1080"
                case 4:
                    videoParameter.resolution = "720"
                case 5:
                    videoParameter.resolution = "480"
                case 6:
                    videoParameter.resolution = "360"
                case 7: 
                    videoParameter.resolution = "144"
                case _:
                    videoParameter.resolution = "best"  # default fallback
            print(f"{videoParameter.resolution}")
    except ValueError:
        selectVideoQuality()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

########################################################## 
##########
##########            yt_dlp library
##########
##########################################################

def selectVideoDownloadFormat():
    clearCMD()
    ydl_opts = {}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(videoParameter.url, download=False)

            if info and 'formats' in info:
                formats = info['formats']
                title = info.get('title', 'Unknown Title')

                clearCMD()
                
                print(f"Title of Video: {title}\n\n")
                print(f"Please selected desired format for {videoParameter.channelOrVideo}")
                print("==============================================")


                # Filter video formats with resolution and unique combos
                filtered_formats = []
                seen_combos = set()
                
                for fmt in formats:
                    ext = fmt.get('ext')
                    resolution = fmt.get('resolution')
                    has_video = fmt.get('vcodec') != 'none'
                    has_audio = fmt.get('acodec') != 'none'
                    av_type = 'unknown'

                    if has_video and has_audio:
                        av_type = 'audio+video'
                    elif has_audio:
                        av_type = 'audio'
                    else:
                        av_type = 'video only' 

                    if not resolution or not has_video:
                        continue

                    combo_key = (ext, resolution, av_type)
                    if combo_key in seen_combos:
                        continue
                    seen_combos.add(combo_key)
                    filtered_formats.append((fmt, av_type))

                # Sort by ext priority: mp4 first, then webm, then others
                def sort_key(item):
                    fmt, _ = item
                    return (0 if fmt['ext'] == 'mp4' else 1 if fmt['ext'] == 'webm' else 2, fmt.get('height', 0))

                filtered_formats.sort(key=sort_key)

                # Print with clean index starting at 1
                for idx, (fmt, av_type) in enumerate(filtered_formats, 1):
                    print(f"{idx:>3}. {fmt['ext']:>4} | {fmt.get('resolution'):<10} | {av_type}") 

                try:                
                    print("==============================================")
                    choice = input("Selection: ").strip()
                    choice = int(choice)
                    if not (1 <= choice <= len(filtered_formats)):
                        selectVideoDownloadFormat()
                    else:
                        print("\n\nDownloading video\n")
                        selected_format, _ = filtered_formats[choice - 1]
                        downloadYoutubeVideo(selected_format)
                except ValueError:
                    selectVideoDownloadFormat()
                except KeyboardInterrupt:
                    print("\nExiting program")
                exit(0)

            else:
                print("No format information available.")
    except Exception:
        getURL(True)

def downloadYoutubeVideo(format):
    format_code = format['format_id']
    ydl_opts = {
            'format': format_code,
            'ratelimit': 2 * 1024 * 1024,  # 2 MB/s speed limit to prevent IP from being blocked
    } 
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoParameter.url])


########################################################## 
##########
##########            SUPPORTING FUNCTIONS 
##########
##########################################################

def clearCMD():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


########################################################## 
##########
##########             
##########             MAIN FUNCTION
##########
##########################################################

if __name__ == "__main__":
    startingInterface()

