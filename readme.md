# AI Video Pipeline

This project generates a short video based on a user-provided topic. It uses Google Gemini for script generation, gTTS for voiceover, Pexels for background video, and MoviePy to combine everything into a final video.

## Prerequisites

- Python 3.8 or higher
- A Google Cloud API Key for Gemini
- A Pexels API Key

## Setup

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment** (recommended):

    ```sh
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:

    Create a file named `.env` in the root directory and add your API keys:

    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    PEXELS_API_KEY=your_pexels_api_key_here
    ```

    You can use `.envSample` as a reference.

## Usage

1.  **Run the main script**:

    ```sh
    python main.py
    ```

2.  **Enter a topic** when prompted (e.g., "AI", "Space", "Nature").

3.  **Wait for the pipeline to finish**. The script will:
    - Generate a script using Gemini.
    - Convert the script to audio (`voice.mp3`).
    - Download a relevant background video from Pexels (`background.mp4`).
    - Merge them into a final video.

4.  **Output**:
    - The final video will be saved as `final_video.mp4`.

## Troubleshooting

- **504 Deadline Exceeded**: If you encounter this error during script generation, the API might be experiencing high latency. Try running the script again.
- **ImageMagick Error**: MoviePy requires ImageMagick for some operations (like `TextClip`). Since this project uses `ColorClip` and basic composition, it should work fine. However, if you get ImageMagick errors, ensure it is installed and configured correctly for MoviePy.
