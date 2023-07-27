mkdir -p real_time_videos
rm real_time_videos/*.mp4

# ffmpeg -re -f v4l2 -framerate 60 -video_size 1920x1080 -i /dev/video0 \
# -f alsa -i hw:1  -af ebur128 \
# -map 0:v -c:v libx264 -preset ultrafast -fflags nobuffer -crf 23 -bf 0 \
# -map 1:a -c:a aac -b:a 128k -f segment -segment_time 10 -reset_timestamps 1 real_time_videos/output%03d.mp4 \
# -map 0:v -c:v libx264 -s 960x540 -preset ultrafast -fflags nobuffer -crf 30 -bf 0  \
# -map 1:a -c:a libopus -b:a 96k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live


ffmpeg -re -f v4l2 -framerate 60 -video_size 1920x1080 -i /dev/video0 \
-f alsa -i hw:1  -af ebur128 \
-map 0:v -c:v libx264 -preset ultrafast -fflags nobuffer -crf 23 -bf 0 \
-map 1:a -c:a aac -b:a 128k -f segment -segment_time 10 -reset_timestamps 1 real_time_videos/output%03d.mp4 \
-map 0:v -c:v libx264 -s 960x540 -preset ultrafast -fflags nobuffer -tune zerolatency -crf 30 -bf 0  \
-map 1:a -c:a aac -b:a 64k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live

# ffmpeg -f v4l2 -framerate 60 -video_size 1920x1080 -i /dev/video0 \
# -f alsa -i hw:1  -af ebur128 \
# -map 0:v -c:v libx264 -preset ultrafast -fflags nobuffer -tune zerolatency -cr 30 -bf 0  \
# -map 1:a -c:a libopus -b:a 256k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live
