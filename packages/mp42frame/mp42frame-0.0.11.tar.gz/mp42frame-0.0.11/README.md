# mp42frame.py

This Python script, `mp42frame.py`, is used to convert a video file or multiple video files in a directory into a series of image frames.

## Dependencies

- OpenCV (cv2)
- sys
- os
- glob

## Usage
1. For a single video file:
    ```
    pip install mp42frame
    ```

2. For a single video file:
    ```
    mp42frame <video_file.mp4>
    ```
    This will create a new directory with the same name as the video file (without the '.mp4' extension) and save the extracted frames as JPEG files in this directory.

3. For multiple video files in a directory:
    ```
    mp42frame <directory_path>
    ```
    This will process all '.mp4' files in the specified directory. For each video file, a new directory will be created with the same name as the video file (without the '.mp4' extension) and the extracted frames will be saved as JPEG files in these directories.

## Note
- The script will exit if no argument is provided.
- The frames are saved as 'frame_n.jpg', where 'n' is the frame number.
- The script will stop if the 'Escape' key is hit during the frame extraction process.
