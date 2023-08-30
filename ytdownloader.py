from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from urllib.parse import urlparse, parse_qs
import yt_dlp as youtube_dl


def get_time_value_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if 't' in query_params:
        time_value = query_params['t'][0]
        if time_value.isdigit():
            return int(time_value)
    return None


def download_video(url, save_path, start_time, end_time, sub_text):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s_original.%(ext)s')
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = os.path.join(save_path, f"{info_dict['title']}_original.{info_dict['ext']}")

        trimmed_video_path = os.path.splitext(video_path)[0] + "_" + sub_text + ".mp4"
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
    video_url_1 = input(
        "Enter the first YouTube video URL (start): ")  #
    video_url_2 = input(
        "Enter the second YouTube video URL (end): ")  # https://youtu.be/dQw4w9WgXcQ?feature=shared&t=71
    save_folder = get_downloads_folder_path()  # C:/Users/Prathamesh/Downloads/yt_download/
    sub_text = input("Enter subtitle of the video: ")
    start_time = get_time_value_from_url(video_url_1)
    end_time = get_time_value_from_url(video_url_2)
    download_video(video_url_1, save_folder, start_time, end_time, sub_text)
