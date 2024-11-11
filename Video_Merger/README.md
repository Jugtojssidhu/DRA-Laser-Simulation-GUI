# Video Merger for Simulation and Comparison Videos

## Overview
The video merger component combines the simulation output video with an input comparison video to create a unified view. It also generates a similarity video that highlights pixel-by-pixel matches and differences, making it easy to visually compare the simulated and real data.

## Features
- **Video Comparison**: Combines simulation output, input video, and similarity video into a single display.
- **Similarity Analysis**: Generates a video with green pixels for identical areas and red pixels for differing areas.
- **Output as Merged Video**: Produces a final video file with the merged display.

## File Structure
- **`merge.py`**: Script that analyzes, merges, and saves the final comparison video.

## Usage
1. **Run the Video Merger**: Execute `merge.py` to merge the selected videos.
2. **Select Videos for Merging**: Ensure the paths to the simulation output, input video, and similarity video are set in the script.
3. **View Merged Video**: The output will be saved as `merged_video.mp4` for review.

## Code Structure
- **Similarity Analysis**: Uses color detection to calculate and display matching pixels.
- **Video Merging**: Combines multiple video inputs into a unified view using `moviepy`.

## Dependencies
- **moviepy**: For video manipulation and merging.
- **OpenCV**: Used for frame-by-frame analysis in similarity detection.
