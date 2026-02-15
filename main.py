import os
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, ColorClip
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY not found in .env")

genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# 1️⃣ Generate Script
# -----------------------------
def generate_script(topic):
    print("Generating script...")
    model = genai.GenerativeModel('gemini-3-flash-preview')

    prompt = f"Write a short 20-word YouTube narration script about {topic}. No markdown."

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print("Error in Genenrating script")
        print("Error generating script:", e)
        return None

    script = response.text.strip()

    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("Script generated:\n", script)
    return script

# -----------------------------
# 2️⃣ Generate Voice
# -----------------------------
def generate_voice(script_text, output_file="voice.mp3"):
    print("Generating voice...")
    tts = gTTS(script_text, lang='en', slow=False)
    tts.save(output_file)
    print(f"Voice saved as {output_file}")
    return output_file

# -----------------------------
# 3️⃣ Fetch Video from Pexels
# -----------------------------
def fetch_video_from_pexels(topic, output_file="background.mp4"):
    print("Fetching video from Pexels...")
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=1"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
    except Exception as e:
        print("Error fetching video:", e)
        return None

    if "videos" not in data or len(data["videos"]) == 0:
        print("No Pexels video found. Using black background.")
        return None

    video_url = data["videos"][0]["video_files"][0]["link"]
    video_data = requests.get(video_url).content

    with open(output_file, "wb") as f:
        f.write(video_data)

    print(f"Video downloaded as {output_file}")
    return output_file

# -----------------------------
# 4️⃣ Create Final Video
# -----------------------------
def create_video(video_file, audio_file="voice.mp3", output_file="final_video.mp4"):
    print("Creating final video...")
    audio = AudioFileClip(audio_file)

    # If video missing, use black background
    if video_file and os.path.exists(video_file):
        video = VideoFileClip(video_file)
        if video.duration < audio.duration:
            video = video.loop(duration=audio.duration)
        video = video.subclip(0, audio.duration)
    else:
        video = ColorClip((1280,720), color=(0,0,0)).set_duration(audio.duration)

    final = video.set_audio(audio)
    final.write_videofile(output_file, codec="libx264", audio_codec="aac")
    print(f"Final video saved as {output_file}")

# -----------------------------
# 🚀 MAIN PIPELINE
# -----------------------------
def main():
    topic = input("Enter topic for video: ")

    # 1. Generate script
    script = generate_script(topic)
    if not script:
        print("Script generation failed. Exiting.")
        return

    # 2. Generate voice
    voice_file = generate_voice(script)

    # 3. Fetch Pexels video
    video_file = fetch_video_from_pexels(topic)

    # 4. Combine video + voice
    create_video(video_file, voice_file)

    print("✅ Pipeline complete! Check final_video.mp4")

if __name__ == "__main__":
    main()
