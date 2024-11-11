from moviepy.editor import VideoFileClip, clips_array, ColorClip
import cv2
import numpy as np

def analyze_video(input_video_path):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)
    
    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('SimilarityVideo.mp4', fourcc, fps, (frame_width, frame_height))
    
    # Define the lower and upper bounds for green
    # Assuming that your video's green is exactly [0, 255, 0] in RGB
    lower_green = np.array([60, 200, 0], dtype="uint8") # HSV for light green
    upper_green = np.array([90, 255, 255], dtype="uint8") # HSV for dark green
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to HSV (better for color detection)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Calculate the percentage of green pixels
        green_mask = cv2.inRange(frame_hsv, lower_green, upper_green)
        green_pixels = np.sum(green_mask > 0)
        total_pixels = frame.shape[0] * frame.shape[1]
        green_percentage = (green_pixels / total_pixels) * 100
        
        # Create a black image for displaying similarity
        black_image = np.zeros((frame_height, frame_width, 3), dtype="uint8")
        
        # Put the similarity text in the center of the black image
        text = f'Similarity: {green_percentage:.2f}%'
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = (frame_height + text_size[1]) // 2
        cv2.putText(black_image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Write the black image with the similarity text to the output video
        out.write(black_image)
    
    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

analyze_video(r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\output_video.mp4")

def merge_videos(video_path1, video_path2, video_path3, video_path4):
    # Load the videos
    video1 = VideoFileClip(video_path1)
    video2 = VideoFileClip(video_path2)
    video3 = VideoFileClip(video_path3)
    video4 = VideoFileClip(video_path4)

    # Calculate the minimum width and height among the videos
    target_width = min(video1.w, video2.w, video3.w, video4.w)
    target_height = min(video1.h, video2.h, video3.h, video4.h)

    # Resize videos to the same size
    video1 = video1.resize(newsize=(target_width, target_height))
    video2 = video2.resize(newsize=(target_width, target_height))
    video3 = video3.resize(newsize=(target_width, target_height))
    video4 = video4.resize(newsize=(target_width, target_height))

    # Create a composite video
    final_clip = clips_array([[video1, video2], [video3, video4]])

    # Write the result to a file
    final_clip.write_videofile("merged_video.mp4", fps=24)

# Example of how to use the function
merge_videos(
    r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\simulation_video_1.mp4",
    r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\test_video.mp4",
    r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\output_video.mp4",
    r"C:\Users\Jugto\Desktop\DRA\CustomTkinter-master\SimilarityVideo.mp4"
)