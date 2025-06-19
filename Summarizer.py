from youtube_transcript_api import YouTubeTranscriptApi    # For fetching subtitles
from transformers import pipeline, AutoTokenizer    # LLM Model for summarizing the text
import re
def extract_video_id(url):    # Function to extract video_id from the url
    # Support both long and short forms
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def summarize(video_url, maxlen, minlen, randomness):    # Function which will return summarized string taking video url and some parameters
    video_id = extract_video_id(video_url)
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    try:    # to handle errors
        transcript = YouTubeTranscriptApi.get_transcript(video_id)    #getting transcript using library
        subtitles_str = ""

        for entry in transcript:
            sent = entry["text"]    
            subtitles_str += sent
            subtitles_str += " "    # adding each line from the fetched string/line
        tokens = tokenizer.encode(subtitles_str)

        if len(tokens) > 1024:    # Because the model doesn't support tokens greater than 1024
            return "token"
        summarizer = pipeline("summarization")    
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)

        return summary[0]['summary_text']    #Returning the summarized string

    except Exception:
        return None    # if error then return None

