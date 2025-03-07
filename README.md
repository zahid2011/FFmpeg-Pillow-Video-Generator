# FFmpeg & Pillow Video Generator

This project generates a **short video from an image** using **FFmpeg & Pillow**, with:

✅ **Image processing** (grayscale & text overlay)  
✅ **Background music** integration  
✅ **Subtitles** for description  
✅ **Narration voiceover** (text-to-speech)  

## 📌 Expected Output:
🎥 [Sample Video Demo](https://drive.google.com/file/d/1BlEFCEh6SOwEC_fS0Fg8aBjLfQYaYCws/view?usp=sharing)

---

## 📂 Download Required Files
To run the script, download the required files from Google Drive:

- 🎵 **Background Music:** [Download background_music.mp3](https://drive.google.com/file/d/1MT1owc3qw_YLU3SSdKvkuEiEZzKlXkGV/view?usp=sharing)
- 🖼️ **Sample Input Image:** [Download input.jpg](https://drive.google.com/file/d/1GeTrtRJ4ddiBkcQg-HHId_nUrp4fK7uW/view?usp=sharing)

After downloading, place them in the **project root folder** before running the script.

---

## Installation Instructions
### **1️⃣ Install Dependencies**
Make sure you have Python installed. Then, install the required libraries:
```sh
pip install -r requirements.txt
```
### Install FFmpeg

#### 🔹 Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html).
2. Extract the downloaded `.zip` file to a folder (e.g., `C:\ffmpeg`).
3. Add FFmpeg to `PATH`:
   - Open **System Properties** → **Advanced** → **Environment Variables**.
   - Under **System Variables**, find **Path**, then click **Edit**.
   - Click **New** and add the path to `ffmpeg\bin`
   - Click **OK** to save.
4. Verify the installation by running:
   ```sh
   ffmpeg -version
   ```
---
## How to Use

### 1️⃣ Configure `config.json`
Edit the `config.json` file to set your desired parameters:

```json
{
    "image": "input.jpg",
    "text": "Lioness",
    "music": "background_music.mp3",
    "subtitles": "A majestic lioness stands proudly.",
    "duration": 7,
    "output_video": "output/final_video.mp4"
}
```
### 2️⃣ Run the Script
Execute the following command in your terminal:

```sh
python3 main.py
```
### ✅ What This Script Will Do:
- ✅ Process the image (apply transformations & overlay text)
- ✅ Generate a video from the image
- ✅ Add background music
- ✅ Embed subtitles
- ✅ Merge narration voiceover

### 📂 Output File:
The **final video** will be saved on the output folder as:

```sh
output/final_video_with_voiceover.mp4
```
