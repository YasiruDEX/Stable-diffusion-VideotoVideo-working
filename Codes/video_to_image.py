import cv2
import os

def video_to_png(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Loop through each frame and save it as a PNG image
    for frame_number in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Create a file name for the PNG image
        png_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")

        # Save the frame as a PNG image
        cv2.imwrite(png_filename, frame)

        print(f"Frame {frame_number + 1}/{frame_count} saved as {png_filename}")

    # Release the video capture object
    cap.release()

    print("Conversion complete.")

# Example usage
video_path = "video.mp4"
output_folder = "video_to_img_output"

video_to_png(video_path, output_folder)
