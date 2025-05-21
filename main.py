import yt_dlp
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
    """
    Download videos from a YouTube channel with smart format and resolution fallbacks.
    - Prefers requested extension, with fallback to alternative if not available
    - Selects closest available resolution (preferring next highest if exact match unavailable)
    """
    print("Starting channel video download process...")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(output_path, '')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process filter keywords
    filter_keywords = []
    if videoParameter.filter:
        filter_keywords = [kw.strip().lower() for kw in videoParameter.filter.split(',') if kw.strip()]
    
    # Build a smarter format selection string based on priorities
    if videoParameter.mode == "video+audio":
        # For combined video+audio
        if videoParameter.extension == "mp4":
            # Try mp4 first, then webm
            format_base = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=mp4]/best[ext=webm]/best"
        else:
            # Try webm first, then mp4
            format_base = "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=webm]/best[ext=mp4]/best"
    else:
        # For video only
        if videoParameter.extension == "mp4":
            # Try mp4 first, then webm
            format_base = "bestvideo[ext=mp4]/bestvideo[ext=webm]/best[ext=mp4]/best[ext=webm]/best"
        else:
            # Try webm first, then mp4
            format_base = "bestvideo[ext=webm]/bestvideo[ext=mp4]/best[ext=webm]/best[ext=mp4]/best"
    
    # Handle resolution constraints
    if videoParameter.resolution != "best":
        try:
            target_resolution = int(videoParameter.resolution)
            
            # Create resolution-specific format strings with fallbacks
            resolution_formats = []
            
            # First try: exact resolution match
            resolution_formats.append(f"{format_base}[height={target_resolution}]")
            
            # Second try: closest resolution below target (in descending order)
            standard_resolutions = [2160, 1440, 1080, 720, 480, 360, 240, 144]
            lower_resolutions = [r for r in standard_resolutions if r < target_resolution]
            lower_resolutions.sort(reverse=True)  # Highest to lowest
            
            for res in lower_resolutions:
                resolution_formats.append(f"{format_base}[height={res}]")
            
            # Third try: closest resolution above target (in ascending order)
            higher_resolutions = [r for r in standard_resolutions if r > target_resolution]
            higher_resolutions.sort()  # Lowest to highest
            
            for res in higher_resolutions:
                resolution_formats.append(f"{format_base}[height={res}]")
            
            # Finally add the base format as a last resort
            resolution_formats.append(format_base)
            
            # Join all format options with fallback operator
            format_string = '/'.join(resolution_formats)
        except ValueError:
            # If resolution parsing fails, use the base format
            format_string = format_base
    else:
        # For "best" resolution, just use the base format
        format_string = format_base
    
    print(f"Using format selector: {format_string}")
    
    # Main download logic
    try:
        print("Extracting channel information...")
        
        # First extraction to get list of videos
        info_opts = {
            'quiet': True,
            'extract_flat': True,
            'ignoreerrors': True
        }
        
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info_dict = ydl.extract_info(videoParameter.url, download=False)
            if not info_dict:
                print("Failed to extract information from URL.")
                return
            
            # Get entries from the extracted info
            entries = info_dict.get('entries', [])
            if not entries and not info_dict.get('_type') == 'playlist':
                # Single video case
                entries = [info_dict]
            
            if not entries:
                print("No videos found in the channel or playlist.")
                return
                
            print(f"Found {len(entries)} total videos in channel/playlist.")
            
            # Filter entries by type (video, shorts, playlist)
            filtered_entries = []
            for entry in entries:
                if not entry:
                    continue
                
                # Get video URL
                entry_url = entry.get('url') or entry.get('webpage_url')
                if not entry_url:
                    continue
                
                # Determine video type
                is_short = '/shorts/' in str(entry_url)
                is_playlist = 'playlist' in str(entry_url) or 'list=' in str(entry_url)
                
                # Apply user's video type filter
                should_include = False
                
                if (is_short and videoParameter.shorts) or \
                   (is_playlist and videoParameter.playlist) or \
                   (not is_short and not is_playlist and videoParameter.videos):
                    should_include = True
                
                if should_include:
                    filtered_entries.append(entry)
            
            print(f"After type filtering: {len(filtered_entries)} videos")
        
        # Content filtering based on keywords
        if filter_keywords:
            print(f"Applying content filters: {', '.join(filter_keywords)}")
            filtered_by_content = []
            
            # Content info extraction options
            content_opts = {
                'quiet': True,
                'skip_download': True,
                'ignoreerrors': True
            }
            
            for entry in filtered_entries:
                try:
                    entry_url = entry.get('url') or entry.get('webpage_url')
                    if not entry_url:
                        continue
                    
                    # Get detailed info for this video
                    with yt_dlp.YoutubeDL(content_opts) as ydl_info:
                        video_info = ydl_info.extract_info(entry_url, download=False)
                        
                        if not video_info:
                            continue
                        
                        # Get title and description for filtering
                        title = str(video_info.get('title', '')).lower()
                        description = str(video_info.get('description', '')).lower()
                        
                        # Check if any keyword matches
                        if any(kw in title or kw in description for kw in filter_keywords):
                            filtered_by_content.append(video_info)
                except Exception as e:
                    print(f"Error processing video: {e}")
            
            filtered_entries = filtered_by_content
            print(f"After content filtering: {len(filtered_entries)} videos")
        
        # Apply video count limit
        if videoParameter.no_of_video > 0:
            filtered_entries = filtered_entries[:videoParameter.no_of_video]
            print(f"Limited to first {videoParameter.no_of_video} videos")
        
        # Check if we have videos to download
        if not filtered_entries:
            print("No videos found after applying all filters.")
            return
        
        print(f"Proceeding to download {len(filtered_entries)} videos...")
        
        # Download videos one by one
        for idx, entry in enumerate(filtered_entries, 1):
            try:
                # Get video URL and title
                if isinstance(entry, dict):
                    entry_url = entry.get('url') or entry.get('webpage_url')
                    title = entry.get('title', f"Video #{idx}")
                else:
                    entry_url = entry
                    title = f"Video #{idx}"
                
                if not entry_url:
                    print(f"[{idx}/{len(filtered_entries)}] Skipping: No URL found")
                    continue
                
                print(f"\n[{idx}/{len(filtered_entries)}] Downloading: {title}")
                print(f"URL: {entry_url}")
                
                # Create download options for this specific video
                download_opts = {
                    'format': format_string,
                    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'verbose': False  # Set to True for debugging
                }
                
                # Apply rate limiting if specified
                if videoParameter.throttleDownloadSpeed > 0:
                    download_opts['ratelimit'] = int(videoParameter.throttleDownloadSpeed * 1024 * 1024)
                
                # Download this video
                with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                    ydl_download.download([entry_url])
                    print(f"✓ Successfully downloaded: {title}")
            except Exception as e:
                print(f"× Failed to download video #{idx}: {e}")
                print(f"  Error details: {str(e)}")
    
    except Exception as e:
        print(f"An error occurred during download process: {e}")
        import traceback
        traceback.print_exc()
        return

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

