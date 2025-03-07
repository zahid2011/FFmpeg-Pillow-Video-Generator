from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
from multi_subtitles import generate_multi_subtitles
from narration import generate_narration
import json

def process_image(image_path, text="TESTING SAMPLE TEXT"):
    """Applies grayscale, adds text, and saves the processed image."""

    if not os.path.exists(image_path):
        print(f" Error: {image_path} not found.")
        return None
    
    # Loading the Image
    image = Image.open(image_path)

    # Applying Grayscale
    gray_image = image.convert("L")
    draw = ImageDraw.Draw(gray_image)

    # Overlaying the Text
    overlay_text = text
    font = ImageFont.truetype("arial.ttf", 180)

    # Getting Image Dimensions
    image_width, image_height = gray_image.size

    # Getting the Text Size using textbbox()
    bbox = draw.textbbox((0, 0), overlay_text, font=font)
    text_width = bbox[2] - bbox[0]

    # Positioning the Text Lower 
    text_x = (image_width - text_width) // 2
    text_y = int(image_height * 0.80) 

    # Drawing Text with black Shadow for Better Visibility
    draw.text((text_x - 2, text_y - 2), overlay_text, font=font, fill=0)  # Shadow (Black)
    draw.text((text_x, text_y), overlay_text, font=font, fill=255)  # Main Text (White)

    # Making sure that the Output Directory Exists
    os.makedirs("output", exist_ok=True)

    # Generating Output File Path
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_image_path = f"output/{base_name}_processed.jpg"

    # Saving Processed Image
    gray_image.save(output_image_path)
    print(f"Image processing complete. Processed image saved as: {output_image_path}")

    return output_image_path 

def create_video(image_path, output_video="output/output_video.mp4", duration=7, 
                 music_file=None, subtitles_file=None, narration_file=None):
    """
    Generates a video from the processed image using FFmpeg and optionally adds
    background music, subtitles, and voiceover narration. Intermediate video
    files are removed, leaving only the final narrated video in the 'output' folder.
    """

    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Run image processing first.")
        return None

    # Step 1: Creating the Video from Image
    ffmpeg_command = [
        "ffmpeg",
        "-loop", "1",                               # loops the input image, treating it like a video.
        "-i", image_path,       
        "-c:v", "libx264",                          # encodes the video using the H.264 codec.
        "-t", str(duration),                        # sets the total video length in seconds.
        "-pix_fmt", "yuv420p",                      # ensures broad compatibility across players.
        "-vf", f"scale=-2:720:force_original_aspect_ratio=decrease", # scales the video to a maximum height of 720px while preserving aspect ratio.
        "-y", output_video                          # overwrites the output file if it already exists.
    ]
    
    print("Generating video from image...")
    subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Running the FFmpeg command

    # Checking if FFmpeg successfully created the output video.
    if not os.path.exists(output_video):
        print("Error: Video creation failed.")
        return None

    latest_video = output_video  # Keeping track of the most recent video

    # Step 2: Adding the Background Music
    if music_file and os.path.exists(music_file):
        output_video_with_music = "output/output_video_with_music.mp4"
        ffmpeg_music_command = [
            "ffmpeg",
            "-i", latest_video,     # Input video file (without music).
            "-i", music_file,       # Input audio file (background music).  
            "-c:v", "copy",         # Copies the video stream without re-encoding (faster processing)
            "-c:a", "libmp3lame",   # Re-encodes the audio to MP3 format for compatibility.
            "-b:a", "192k",         # Sets audio bitrate to 192kbps for good quality.
            "-shortest",            # Ensures the final video stops when the shorter of the two inputs ends.
            "-y", output_video_with_music
        ]
        
        print("Adding background music...")
        subprocess.run(ffmpeg_music_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(output_video_with_music):
            print(f"Video with music saved as: {output_video_with_music}")

            # Removing the previous intermediate file if it's not the same as the new one
            if os.path.exists(latest_video) and latest_video != output_video_with_music:
                os.remove(latest_video)
            latest_video = output_video_with_music
        else:
            print("Error: Failed to add background music.")
            return latest_video

    # Step 3: Adding Subtitles
    if subtitles_file and os.path.exists(subtitles_file):
        output_video_with_subtitles = "output/output_video_with_subtitles.mp4"
        ffmpeg_subtitle_command = [
            "ffmpeg",
            "-i", latest_video,
            "-vf", f"subtitles='{subtitles_file}'", # Applies the subtitles filter using the provided .srt file.
            "-c:v", "libx264",                      # Ensures the video is re-encoded with H.264 for compatibility.
            "-c:a", "copy",
            "-y", output_video_with_subtitles
        ]

        print("Adding subtitles to video...")
        result = subprocess.run(ffmpeg_subtitle_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("FFmpeg error while adding subtitles:")
            print(result.stderr) 
        else:
            print("FFmpeg output:", result.stdout)

        if os.path.exists(output_video_with_subtitles):
            print(f"Video with subtitles saved as: {output_video_with_subtitles}")
            # Removing previous intermediate file if it's not the same as the new one
            if os.path.exists(latest_video) and latest_video != output_video_with_subtitles:
                os.remove(latest_video)
            latest_video = output_video_with_subtitles
        else:
            print("Error: Failed to add subtitles.")

    # Step 4: Adding Voiceover
    if narration_file and os.path.exists(narration_file):
        final_video_output = "output/final_video_with_voiceover.mp4"
        ffmpeg_voiceover_command = [
            "ffmpeg",
            "-i", latest_video,
            "-i", narration_file,
            "-filter_complex", "[1:a]volume=1.3[a1]; [0:a]volume=0.4[a2]; [a1][a2]amix=inputs=2:duration=shortest[aout]",
            "-map", "0:v",            # Keeping the original video stream
            "-map", "[aout]",         # Merged audio track
            "-c:v", "copy",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-y", final_video_output
        ]
        
        print("🎤 Merging voiceover with existing audio...")
        subprocess.run(ffmpeg_voiceover_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(final_video_output):
            print(f"Final video with voiceover saved as: {final_video_output}")
            # Removing previous intermediate file if it's not the same as the new one
            if os.path.exists(latest_video) and latest_video != final_video_output:
                os.remove(latest_video)
            latest_video = final_video_output
        else:
            print("Error: Failed to merge voiceover.")
            return latest_video

    # latest_video now points to the final video (with narration)
    return latest_video

def load_config(config_path="config.json"):
    """Loads and validates the configuration file, ensuring required values are present."""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Config file is missing or contains invalid JSON.")
        return None

    # Required keys with default values
    required_fields = {
        "image": None,
        "text": None,
        "music": None,
        "subtitles": None,
        "duration": 7,
        "output_video": "output/final_video.mp4"
    }

    # Prompt messages based on key type
    prompts = {
        "image": "Enter the folder name and file path for the image: ",
        "music": "Enter the folder name and file path for the music file: ",
        "text": "Enter the input text: ",
        "subtitles": "Enter the subtitles text: ",
        "duration": "Enter video duration (seconds): ",
        "output_video": "Enter the output video file path: "
    }

    # Iteratering through required fields and check if they exist and are not empty
    for key, default_value in required_fields.items():
        if key not in config or not config[key]:  # Checking if missing or empty
            while True:
                user_input = input(f"⚠ {prompts[key]}").strip()
                if user_input:  # makiing sure that the input is not empty
                    config[key] = user_input if key != "duration" else int(user_input)  # Converting duration to integer
                    break
                else:
                    print(f"⚠ '{key}' cannot be empty! Please provide a valid value.")

    return config


if __name__ == "__main__":
    # Loading configuration from config.json
    config = load_config("config.json")
    
    # Retrieving the values from config with default fallbacks
    image_path = config.get("image", "input.jpg")
    text_overlay = config.get("text", "Lioness")
    music_file = config.get("music", "background_music.mp3")
    subtitles_text = config.get("subtitles", "A majestic lioness stands proudly, scanning the horizon across the vast savanna.")
    video_duration = config.get("duration", 7)
    output_video = config.get("output_video", "output/final_video.mp4")
    
    # Processing the image with the provided text overlay
    processed_image = process_image(image_path, text=text_overlay)

    # Generating multi-line subtitles (by having a gradual reveal effect)
    subtitles_file = generate_multi_subtitles(
        text=subtitles_text,
        line_duration=2,
        max_width=40,
        output_srt="output/subtitles.srt"
    )

    # Generating voiceover narration using gTTS
    narration_file = generate_narration(
        subtitles_text,
        output_audio="output/narration.mp3"
    )

    # Creating the video if image processing was successful
    if processed_image:
        create_video(
            processed_image, 
            output_video=output_video,
            duration=video_duration,  
            music_file=music_file, 
            subtitles_file=subtitles_file,
            narration_file=narration_file
        )