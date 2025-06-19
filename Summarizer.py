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

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "sshleifer/distilbart-cnn-12-6",
        use_auth_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )

    try:  # to handle errors
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # getting transcript using library
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent + " "  # adding each line

        # Token count check
        tokens = tokenizer.encode(subtitles_str)
        if len(tokens) > 1024:
            return "token"

        # Load summarizer pipeline
        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            use_auth_token=os.getenv("from youtube_transcript_api import YouTubeTranscriptApi  # For fetching subtitles
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

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "sshleifer/distilbart-cnn-12-6",
        use_auth_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )

    try:  # to handle errors
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # getting transcript using library
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent + " "  # adding each line

        # Token count check
        tokens = tokenizer.encode(subtitles_str)
        if len(tokens) > 1024:
            return "token"

        # Load summarizer pipeline
        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            use_auth_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )

        # Generate summary
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)

        return summary[0]['summary_text']  # Returning the summarized string

    except Exception as e:
        print("Summarizer ERROR:", e)  # for debugging (check streamlit logs)
        return None  # if error then return None
")
        )

        # Generate summary
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)

        return summary[0]['summary_text']  # Returning the summarized string

    except Exception as e:
        print("Summarizer ERROR:", e)  # for debugging (check streamlit logs)
        return None  # if error then return None

