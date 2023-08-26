from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from urllib.parse import urlparse, parse_qs


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
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading: {yt.title}")
        video_path = stream.download(output_path=save_path)

        trimmed_video_path = os.path.splitext(video_path)[0] + "_" + sub_text + ".mp4"
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=trimmed_video_path)
        os.remove(video_path)
        print("Download complete!")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    video_url_1 = input("Enter the first YouTube video URL: ") # https://youtu.be/dQw4w9WgXcQ?feature=shared&t=39
    video_url_2 = input("Enter the second YouTube video URL: ") # https://youtu.be/dQw4w9WgXcQ?feature=shared&t=71
    save_folder = input("Enter the path to save the video: ") # C:/Users/Prathamesh/Downloads/yt_download/
    sub_text = input("Enter subtitle of the video: ")
    start_time = get_time_value_from_url(video_url_1)
    end_time = get_time_value_from_url(video_url_2)
    download_video(video_url_1, save_folder, start_time, end_time, sub_text)

