from youtube_transcript_api import YouTubeTranscriptApi  # For fetching subtitles
from transformers import pipeline, AutoTokenizer  # LLM Model for summarizing the text
import re
import os

# Function to extract video_id from the url
def extract_video_id(url):
    # Support both long and short forms
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Function which will return summarized string taking video url and some parameters
def summarize(video_url, maxlen, minlen, randomness):
    video_id = extract_video_id(video_url)

    try:  # to handle errors
        # Load tokenizer and model with token
        hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        tokenizer = AutoTokenizer.from_pretrained(
            "sshleifer/distilbart-cnn-12-6",
            use_auth_token=hf_token
        )

        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            tokenizer=tokenizer,
            use_auth_token=hf_token
        )

        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent + " "  # add each line

        # Token count check
        tokens = tokenizer.encode(subtitles_str)
        if len(tokens) > 1024:
            return "token"

        # Generate summary
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)

        return summary[0]['summary_text']  # Returning the summarized string

    except Exception as e:
        print("Summarizer ERROR:", e)  # for debugging (check streamlit cloud logs)
        return None  # if error then return None
