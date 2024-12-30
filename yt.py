from os.path import isdir
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import json
import sys
import re


# def sanitize_filename(filename):
#     # Replace invalid characters with an underscore
#     return re.sub(r'[<>:"/\\|?*\']', '_', filename)
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".yt_downloader.json")
def sanitize_filename(filename):
    """Sanitize the filename to make it file-system safe."""
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[<>:"/\\|?*\']', '_', filename)
    # Remove trailing periods or spaces
    sanitized = sanitized.strip().strip(". ")
    # Limit filename length to avoid issues
    return sanitized[:255]


def setup_config():
    """Setup or retrieve the default download path."""
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.loads(f.read()).get("download_path")

    print("\x1b[38;5;217mNo default download path found.\x1b[0m")
    download_path = input("\x1b[38;5;217mEnter the default download path: \x1b[0m").strip()
    save_config(download_path)
    return download_path


def save_config(download_path):
    """Save the default download path to the config file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"download_path": download_path}, f)

print(f"\n  \x1b[1;38;5;203m    YouTube Video Downloader\x1b[0m\n\x1b[38;5;167m{'='*40}\x1b[0m\n" )

p = "\x1b[38;5;69m"
end = "\x1b[0m"
ainfo = "\x1b[38;5;220m"
info = "\x1b[1;38;5;40m"

def get_videos():
    """Download video/audio and handle high-quality merging."""
    link = input("\x1b[38;5;41mEnter the link of video\x1b[0m: ").strip()
    results = YouTube(link, on_progress_callback=on_progress)

    all_streams = results.streams
    videos = [video for video in all_streams if video.mime_type == "video/mp4"]
    audios = [audio for audio in all_streams if audio.mime_type in ("audio/mp4", "audio/webm")]

    print(f"\n\x1b[38;5;39mVideo Title{end}: \x1b[38;5;42m{results.title}\x1b[0m\n")
    print(f"\x1b[38;5;39mDuration{end}: \x1b[38;5;42m{results.length/60:.2f} Minutes{end}")


    print(f"\n\x1b[38;5;220m{' '*14}Video\n{'_'*40}\x1b[0m\n")
    for i, video in enumerate(videos, start=1):
        print(f" {info}{i}. Resolution:{end} {p}{video.resolution}{end}{info}, Size:{end} {p}{video._filesize_mb} MB{end}")

    print(f"\n{' '*14}\x1b[38;5;220mAudio\n{'_'*36}\x1b[0m\n")
    for i, audio in enumerate(audios, start=len(videos) + 1):
        print(f" {info}{i}. Bitrate:{end} {p}{audio.abr}{end}{info}, Size:{end} {p}{audio._filesize_mb} MB{end}")




    index = int(input("\n\x1b[38;5;217mChoose a number\x1b[0m: "))

    if index <= len(videos):
        chosen_video = videos[index - 1]
        if chosen_video.is_progressive:
            chosen_video.download(download_path)
            sanitized_title = sanitize_filename(results.title)
            print("\n\x1b[38;5;41m[•] Successfully downloaded Video ✓\x1b[0m\n")
            print(f"\n\x1b[38;5;41m[•] Saved in {download_path}/{sanitized_title}.mp4 ✓\x1b[0m\n")

        else:
            # Download adaptive video and audio, then merge
            tmp_dir_path = f"{download_path}/temp_dir"
            if not isdir(tmp_dir_path):
                os.mkdir(tmp_dir_path)
            tmp_download_path = os.path.join(tmp_dir_path)
            sanitized_title = sanitize_filename(results.title)
            output_path = os.path.join(download_path, f"{sanitized_title}.mp4")

            print("\n\x1b[38;5;43m[•] Downloading video...\x1b[0m")
            chosen_video.download(output_path=tmp_download_path, filename="video.mp4")

            print("\n\x1b[38;5;43m[•] Downloading audio...\x1b[0m")
            best_audio = audios[-1]  # Pick the best available audio
            best_audio.download(output_path=tmp_download_path, filename="audio.mp4")

            print("\x1b[38;5;43m[•] Merging video and audio...\x1b[0m")
            os.system(f'ffmpeg -loglevel error -i "{tmp_download_path}/video.mp4" -i "{tmp_download_path}/audio.mp4" -c:v copy -c:a aac -strict experimental "{output_path}"')

            # Cleanup
            os.remove(f"{tmp_download_path}/video.mp4")
            os.remove(f"{tmp_download_path}/audio.mp4")

            print("\n\x1b[38;5;41m[•] Successfully merged Video and Audio ✓\x1b[0m\n")
            print(f"\n\x1b[38;5;41m[•] Saved in {output_path} ✓\x1b[0m\n")


    elif index > len(videos):
        chosen_audio = audios[index - len(videos) - 1]
        chosen_audio.download(download_path)
        print("\n\x1b[38;5;41m[•] Successfully downloaded Audio ✓\x1b[0m\n")
        sanitized_title = sanitize_filename(results.title)
        print(f"\n\x1b[38;5;41m[•] Saved in {download_path}/{sanitized_title}.mp4a ✓\x1b[0m\n")



def main():
    """Main menu for the YouTube downloader."""
    print("""\x1b[38;5;221m
    Choose an option:

    1. Set default download path
    2. Download Videos/Audios
    3. Exit
    \x1b[0m
    """)
    option = int(input("\x1b[38;5;217mEnter a number: \x1b[0m").strip())

    if option == 1:
        new_path = input("\x1b[38;5;217mEnter full path: \x1b[0m").strip()
        save_config(new_path)
        print("\x1b[38;5;41m[•] Default download path updated successfully ✓\x1b[0m\n")
    elif option == 2:
        get_videos()
    elif option == 3:
        print("\x1b[38;5;203mExiting...\x1b[0m")
        sys.exit(0)
    else:
        print("\x1b[38;5;203mInvalid option. Please try again.\x1b[0m\n")


if __name__ == "__main__":
    download_path = setup_config()
    while True:
        main()

