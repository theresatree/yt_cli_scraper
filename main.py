import yt_dlp
import copy
from urllib.parse import urlparse
from dataclasses import dataclass
import os
import re

########################################################## 
##########
##########              CLASS TO GET PARAMETERS 
##########            TO PASS TO YT_DLP TO INTERACT
##########
##########################################################
@dataclass
class VideoParameters:
    channelOrVideo: str = ""
    resolution: str = "best"
    extension: str = ""
    mode: str = ""
    url: str = ""
    num_downloads: int = 0  
    videos: bool = False
    playlist: bool = False
    shorts: bool = False
    no_of_video: int = 0
    filter: str = ""
    throttleDownloadSpeed: int = 2 # Default 2Mbps to prevent IP from being blocked

videoParameter = VideoParameters()
output_path: str = "./videos" # Video Download Path

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
                downloadIndividualVideo()
            else:
               selectChannelExtension() if is_youtube_channel_url(choice) else getURL(True)
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
                    videoParameter.mode = "video"
                case 2:
                    videoParameter.mode = "video+audio"
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
        selectVideoGroups() 
    except ValueError:
        selectVideoQuality()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def selectVideoGroups():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}")
    print(f"Mode: {videoParameter.mode}")
    print(f"Resolution: {videoParameter.resolution}\n\n")
    print("Select type of videos to download")
    print("=================================")
    print("1. Only Videos")
    print("2. Video + Shorts")
    print("3. Video + Shorts + Playlist")
    print("4. Video + Playlist")
    print("5. Only Playlist")
    print("6. Only Shorts")
    print("7. Shorts + Playlist")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in range(1,9):
            selectVideoGroups()
        else:
            match (choice):
                case 1:
                    videoParameter.videos = True
                case 2:
                    videoParameter.videos = True
                    videoParameter.shorts = True
                case 3:
                    videoParameter.videos = True
                    videoParameter.shorts = True
                    videoParameter.playlist = True
                case 4:
                    videoParameter.videos = True
                    videoParameter.playlist = True
                case 5:
                    videoParameter.playlist = True
                case 6:
                    videoParameter.shorts = True
                case 7:
                    videoParameter.shorts = True
                    videoParameter.playlist = True
            selectNoOfVideos()
    except ValueError:
       selectVideoGroups()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def selectNoOfVideos():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}")
    print(f"Mode: {videoParameter.mode}")
    print(f"Resolution: {videoParameter.resolution}")
    print(f"Videos: {videoParameter.videos}")
    print(f"Shorts: {videoParameter.shorts}")
    print(f"Playlist: {videoParameter.playlist}\n\n")
    print("Number of Videos Limit?")
    print(f"{RED}Enter an integer{RESET}")
    print(f"{ITALIC}0 for no limit.{RESET}")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        videoParameter.no_of_video=choice
        selectFilterWords()
    except ValueError:
        selectNoOfVideos()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def selectFilterWords():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}")
    print(f"Mode: {videoParameter.mode}")
    print(f"Resolution: {videoParameter.resolution}")
    print(f"Videos: {videoParameter.videos}")
    print(f"Shorts: {videoParameter.shorts}")
    print(f"Playlist: {videoParameter.playlist}")
    print(f"Limit: {videoParameter.no_of_video}\n\n")
    print("Select words to filter. Leave blank if no filter")
    print(f"{ITALIC}Separate words with ,{RESET}")
    print(f"{RED}redlight, red, light{RESET}")
    print("=================================")
    try:
        choice = input("Words: ").strip()
        choice = str(choice)
        videoParameter.filter=choice
        confirmSelection()
    except ValueError:
        selectFilterWords()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)

def confirmSelection():
    clearCMD()
    print(f"Selected: {videoParameter.channelOrVideo}")
    print(f"URL: {videoParameter.url}")
    print(f"Extension: {videoParameter.extension}")
    print(f"Mode: {videoParameter.mode}")
    print(f"Resolution: {videoParameter.resolution}")
    print(f"Videos: {videoParameter.videos}")
    print(f"Shorts: {videoParameter.shorts}")
    print(f"Playlist: {videoParameter.playlist}")
    print(f"Limit: {videoParameter.no_of_video}")
    print(f"Filters: {videoParameter.filter}\n\n")
    print("Confirm download?")
    print("=================================")
    print("1. Yes")
    print("2. No, restart selection")
    print("=================================")
    try:
        choice = input("Selection: ").strip()
        choice = int(choice)
        if choice not in range(1,3):
            confirmSelection()
        else:
            match (choice):
                case 1:
                    downloadChannelVideo()
                case 2:
                    startingInterface()
    except ValueError:
        confirmSelection()
    except KeyboardInterrupt:
        print("\nExiting program")
        exit(0)


########################################################## 
##########
##########            yt_dlp library
##########
##########################################################

def downloadChannelVideo():
    print("\nStarting YouTube channel download process...")

    output_dir = os.path.join(output_path, '')
    os.makedirs(output_dir, exist_ok=True)

    channel_url = videoParameter.url.strip()
    while channel_url.endswith('/'):
        channel_url = channel_url[:-1]
    channel_identifier = channel_url.split('/')[-1]
    print(f"Channel identifier: {channel_identifier}")

    filter_keywords = []
    if videoParameter.filter:
        filter_keywords = [kw.strip() for kw in videoParameter.filter.split(',') if kw.strip()]
        print(f"Using filter keywords: {', '.join(filter_keywords)}")

    res_filter = "" if videoParameter.resolution == "best" else f"[height<={videoParameter.resolution}]"

    if videoParameter.mode == "video+audio":
        format_string = (
            f"bv*{res_filter}[ext=mp4]+ba[ext=m4a]/"
            f"b{res_filter}[ext=mp4]/best"
        )
    elif videoParameter.mode == "video":
        format_string = (
            f"bv*{res_filter}[ext=mp4]/"
            f"b{res_filter}[ext=mp4]/bestvideo"
        )
    else:
        raise ValueError(f"Unknown mode: {videoParameter.mode}")

    print(f"Using format: {format_string}")

    base_ydl_opts = {
        'format': format_string,
        'ignoreerrors': True,
        'quiet': False,
        'no_warnings': True,
        'hls_prefer_native': True,
        'hls_prefer_ffmpeg': True,
        'verbose': True,
        'skip_unavailable_fragments': True,
        'compat_opts': ['no-youtube-unavailable-videos'],
        'allow_unplayable_formats': False,
        'extractor_args': {'youtube': {'player_client': 'android'}},
    }

    if videoParameter.throttleDownloadSpeed > 0:
        base_ydl_opts['ratelimit'] = int(videoParameter.throttleDownloadSpeed * 1024 * 1024)

    try:
        print("\nExtracting channel information...")

        urls_to_process = []
        if videoParameter.videos:
            urls_to_process.append(f"{channel_url}/videos")
        if videoParameter.shorts:
            urls_to_process.append(f"{channel_url}/shorts")
        if videoParameter.playlist:
            urls_to_process.append(f"{channel_url}/playlists")

        if not urls_to_process:
            urls_to_process.append(channel_url)

        if filter_keywords:
            keyword_string = ' '.join(filter_keywords)
            if channel_identifier.startswith('@'):
                channel_name = channel_identifier[1:]
            else:
                channel_name = channel_identifier
            search_query = f"ytsearch:{keyword_string} channel:{channel_name}"
            urls_to_process.append(search_query)

        successful_downloads = 0
        total_videos_found = 0

        for url_index, url in enumerate(urls_to_process):
            print(f"\nProcessing URL {url_index + 1}/{len(urls_to_process)}: {url}")

            # Extract full info (no extract_flat to avoid SABR)
            extract_opts = copy.deepcopy(base_ydl_opts)
            extract_opts.update({
                'quiet': True,
                'skip_download': True,
            })

            with yt_dlp.YoutubeDL(extract_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    print(f"No information found for {url}")
                    continue

                entries = []
                if 'entries' in info:
                    entries = [e for e in info['entries'] if e is not None]
                    print(f"Found {len(entries)} videos in this section")
                elif info.get('_type') != 'playlist':
                    entries = [info]
                    print("Found a single video")

                if not entries:
                    print("No videos found in this section")
                    continue

                total_videos_found += len(entries)

                # Filter videos by keywords if needed (for non-search URLs)
                if filter_keywords and not url.startswith('ytsearch'):
                    print(f"Filtering {len(entries)} videos by keywords...")
                    filtered_entries = []
                    for i, entry in enumerate(entries):
                        video_url = entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                        if not video_url:
                            continue
                        try:
                            detail_opts = {
                                'quiet': True,
                                'skip_download': True,
                                'extractor_args': {'youtube': {'player_client': 'android'}}
                            }
                            with yt_dlp.YoutubeDL(detail_opts) as detail_ydl:
                                print(f"Checking video {i + 1}/{len(entries)}...", end="\r")
                                video_info = detail_ydl.extract_info(video_url, download=False)
                                if video_info:
                                    title = str(video_info.get('title', '')).lower()
                                    description = str(video_info.get('description', '')).lower()
                                    if any(kw.lower() in title or kw.lower() in description for kw in filter_keywords):
                                        filtered_entries.append(video_info)
                        except Exception as e:
                            print(f"\nError checking video: {e}")

                    entries = filtered_entries
                    print(f"\nFound {len(entries)} videos matching keywords")

                # Limit number of videos
                if videoParameter.no_of_video > 0:
                    entries = entries[:videoParameter.no_of_video]

                if entries:
                    print(f"\nDownloading {len(entries)} videos...")

                    for i, entry in enumerate(entries):
                        video_url = entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                        if not video_url:
                            continue

                        title = entry.get('title', f"Video #{i + 1}")
                        print(f"\n[{i + 1}/{len(entries)}] Downloading: {title}")

                        # Prepare download options, keep all your params intact
                        download_opts = copy.deepcopy(base_ydl_opts)
                        download_opts['extractor_args'] = {'youtube': {'player_client': 'android'}}

                        # Use format string from above, throttling included
                        if videoParameter.throttleDownloadSpeed > 0:
                            download_opts['ratelimit'] = int(videoParameter.throttleDownloadSpeed * 1024 * 1024)

                        with yt_dlp.YoutubeDL(download_opts) as download_ydl:
                            download_ydl.download([video_url])
                            print(f"✓ Successfully downloaded: {title}")
                            successful_downloads += 1

        print(f"\nDownload process completed.")
        print(f"Total videos found (before filtering): {total_videos_found}")
        print(f"Successfully downloaded: {successful_downloads}")

    except Exception as e:
        print(f"An error occurred in the main process: {e}")
        import traceback
        traceback.print_exc()


def downloadIndividualVideo():
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
                        downloadIndividualVideo()
                    else:
                        print("\n\nDownloading video\n")
                        selected_format, _ = filtered_formats[choice - 1]
                        downloadYoutubeVideo(selected_format)
                except ValueError:
                    downloadIndividualVideo()
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
            'ratelimit': videoParameter.throttleDownloadSpeed * 1024 * 1024,  # 2 MB/s speed limit to prevent IP from being blocked
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

def is_youtube_channel_url(url):
    pattern = re.compile(
        r'^(https?://)?(www\.)?youtube\.com/(@[\w\-]+|channel/[\w\-]+|user/[\w\-]+|c/[\w\-]+)/?$'
    )
    return bool(pattern.match(url))

########################################################## 
##########
##########             
##########             MAIN FUNCTION
##########
##########################################################

if __name__ == "__main__":
    startingInterface()

