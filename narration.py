from gtts import gTTS
import os

def generate_narration(text, output_audio="output/narration.mp3"):
    """
    Converts text into speech using gTTS and saves it as an MP3 file.
    """
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    tts = gTTS(text=text, lang="en")
    tts.save(output_audio)
    
    print(f"Narration saved as: {output_audio}")
    return output_audio

if __name__ == "__main__":
    # Example usage:
    generate_narration("A majestic lioness stands proudly, scanning the horizon across the vast savanna.")
