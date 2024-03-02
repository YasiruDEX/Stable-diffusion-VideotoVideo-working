from flask import Flask, render_template, request, redirect, url_for
import requests
import base64
import os
import json

seed = -1
output_directory = "img_to_ai_gen"
os.makedirs(output_directory, exist_ok=True)

# Specify the folder containing video frames
video_frames_folder = "video_to_img_output"

# Define the prompt
prompt = "anime style"

# Read and process each image in the folder
for filename in os.listdir(video_frames_folder):
    if filename.endswith(".png"):  # assuming all frames are PNG, adjust if needed
        # Read the image file and convert it to base64
        with open(os.path.join(video_frames_folder, filename), "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        # Define the payload to send for each image
        payload = {
            "negative_prompt": "(((deformed face))),(side view:1.2), worst quality, low quality, low res, blurry, text, watermark, logo, banner, extra digits, cropped, jpeg artifacts, error, sketch ,duplicate, monochrome, geometry, mutation, fused face, cloned face",
            "prompt": prompt,
            "steps": 2,
            "width": 512,
            "height": 512,
            "seed": seed,
            "init_images": [img_data]
        }

        # Send payload to the API for each image
        response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/img2img', json=payload)
        r = response.json()

        data = json.loads((r['info']))

        # Extract the seed for the next iteration
        seed = data.get("seed")

        print(seed)

        base64_img = r['images'][0]

        # Decode and save the processed image with a unique filename
        output_filename = f"processed_{filename}"
        with open(os.path.join(output_directory, output_filename), 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

# End of the loop
