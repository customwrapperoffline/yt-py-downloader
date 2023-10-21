from pytube import YouTube
from tqdm import tqdm
import os
import requests
import time

def DownloadAudioAndVideo(link, output_dir, video_quality, max_retries=3):
    for retry in range(max_retries):
        try:
            youtube = YouTube(link)

            if video_quality == 'highest':
                video_stream = youtube.streams.get_highest_resolution()
            elif video_quality == 'lowest':
                video_stream = youtube.streams.filter(res='144p').first()
            else:
                valid_resolutions = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']
                if video_quality in valid_resolutions:
                    video_stream = youtube.streams.filter(res=video_quality).first()
                else:
                    print("Invalid video quality option.")
                    return False

            audio_stream = youtube.streams.filter(only_audio=True).first()

            # Ensure the output directory exists or create it
            os.makedirs(output_dir, exist_ok=True)

            # Define the output file paths
            video_output_path = os.path.join(output_dir, 'video.mp4')
            audio_output_path = os.path.join(output_dir, 'audio.mp3')

            # Download video with progress bar
            video_request = requests.get(video_stream.url, stream=True)
            video_size = int(video_request.headers.get('content-length', 0))

            print("Downloading video...")
            with open(video_output_path, 'wb') as video_file, tqdm(
                desc="Video", total=video_size, unit='B', unit_scale=True, unit_divisor=1024
            ) as progress_bar:
                for data in video_request.iter_content(chunk_size=1024):
                    video_file.write(data)
                    progress_bar.update(len(data))

            # Download audio with progress bar
            audio_request = requests.get(audio_stream.url, stream=True)
            audio_size = int(audio_request.headers.get('content-length', 0))

            print("Downloading audio...")
            with open(audio_output_path, 'wb') as audio_file, tqdm(
                desc="Audio", total=audio_size, unit='B', unit_scale=True, unit_divisor=1024
            ) as progress_bar:
                for data in audio_request.iter_content(chunk_size=1024):
                    audio_file.write(data)
                    progress_bar.update(len(data))

            return True
        except Exception as e:
            print(f"Download attempt {retry + 1} failed. Retrying...")
            time.sleep(5)  # Wait for a moment before retrying

    print("Download failed after multiple attempts.")
    return False

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    output_dir = input("Enter the output directory: ")

    video_quality = input("Enter the video quality ('highest', 'lowest', or specific resolution like '720p'): ")

    if DownloadAudioAndVideo(link, output_dir, video_quality):
        print("Audio and video downloaded successfully.")
    else:
        print("Downloading audio and video failed.")
