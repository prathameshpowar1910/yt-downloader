import os
from urllib.parse import urlparse, parse_qs
import yt_dlp as youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def get_time_value_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 't' in query_params:
        time_value = query_params['t'][0]
        if time_value.isdigit():
            return int(time_value)
    return None

def get_available_formats(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
        return video_formats

def download_video(url, save_path, sub_text, start_time=0, end_time=None, quality='best'):
    try:
        formats = get_available_formats(url)
        print("Available video qualities:")
        for i, format in enumerate(formats):
            print(f"{i + 1}. {format['format_note']} - {format['ext']}")
        
        if quality == 'best':
            selected_format = formats[-1]['format_id']
        else:
            choice = int(input("Enter the number of your preferred quality: ")) - 1
            selected_format = formats[choice]['format_id']

        ydl_opts = {
            'format': selected_format,
            'outtmpl': os.path.join(save_path, '%(title)s_original.%(ext)s')
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = os.path.join(save_path, f"{info_dict['title']}_original.{info_dict['ext']}")
        
        trimmed_video_path = os.path.splitext(video_path)[0] + "_" + sub_text + ".mp4"
        
        if end_time is None:
            end_time = info_dict['duration']
        
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=trimmed_video_path)
        os.remove(video_path)
        print("Download complete!")
    except Exception as e:
        print("Error:", str(e))

def get_downloads_folder_path():
    home = os.path.expanduser("~")
    downloads_folder = os.path.join(home, "Downloads")
    return downloads_folder

if __name__ == "__main__":
    video_url_1 = input("Enter the YouTube video URL: ")
    choice = int(input("Do you want to download full video or a part of it? (0 for full and 1 for part): "))
    save_folder = get_downloads_folder_path()
    sub_text = input("Enter subtitle of the video: ")
    
    if choice == 0:
        download_video(video_url_1, save_folder, sub_text)
    else:
        start_time = int(input("Enter start time in seconds: "))
        end_time = int(input("Enter end time in seconds: "))
        download_video(video_url_1, save_folder, sub_text, start_time, end_time)