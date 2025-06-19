from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, AutoTokenizer
import re

# Function to extract YouTube video ID from URL
def extract_video_id(url):
    # Support both long and short forms
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Main summarize function
def summarize(video_url, maxlen, minlen, randomness):
    video_id = extract_video_id(video_url)

    try:
        # Load tokenizer and model (small and fast — works on Streamlit Cloud)
        model_name = "google/pegasus-xsum"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=tokenizer,
            device=-1  # force CPU (Streamlit Cloud is CPU only)
        )

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent
            subtitles_str += " "

        # Tokenize and check length
        tokens = tokenizer.encode(subtitles_str)
        print("Token length:", len(tokens))

        max_input_tokens = 512  # for Pegasus

        if len(tokens) > 1024:
            return "token"

        # If text is too long → split into chunks
        if len(tokens) > max_input_tokens:
            chunk_size = 500  # characters
            chunks = [subtitles_str[i:i+chunk_size] for i in range(0, len(subtitles_str), chunk_size)]

            final_summary = ""
            for chunk in chunks:
                part = summarizer(chunk, max_length=maxlen, min_length=minlen, do_sample=randomness)
                final_summary += part[0]['summary_text'] + " "

            return final_summary

        else:
            # Short text → summarize normally
            result = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)
            return result[0]['summary_text']

    except Exception as e:
        print("Error occurred:", e)
        return None


