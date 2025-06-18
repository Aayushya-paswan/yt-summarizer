from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, AutoTokenizer
import re
def extract_video_id(url):
    # Support both long and short forms
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
def summarize(video_url, maxlen, minlen, randomness):
    video_id = extract_video_id(video_url)
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent
            subtitles_str += " "
        tokens = tokenizer.encode(subtitles_str)

        if len(tokens) > 1024:
            return "token"
        summarizer = pipeline("summarization")
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)

        return summary[0]['summary_text']

    except Exception:
        return None
