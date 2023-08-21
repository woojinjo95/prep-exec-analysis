import subprocess
import os


def crop_video(video_path, output_path, start_time, end_time):
    cmd = [
        'ffmpeg', 
        '-i', video_path,
        '-ss', seconds_to_time(start_time),  # Start time, e.g., '00:00:10' for 10 seconds in
        '-to', seconds_to_time(end_time),    # End time, e.g., '00:01:00' for 1 minute in
        '-c:v', 'copy',     # Use the same codec for video
        '-c:a', 'copy',     # Use the same codec for audio
        '-y',
        output_path
    ]

    subprocess.run(cmd)


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"



video_path = '/home/jade-m32-05/projects/prep-exec-analysis/data/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-18T163309F381036+0900_1800.mp4'
output_path = 'output.mp4'


crop_video(video_path=video_path,
            output_path=output_path,
            start_time=30,
            end_time=60)
