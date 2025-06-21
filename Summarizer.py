# Importing necessary libraries
from youtube_transcript_api import YouTubeTranscriptApi    # Library to fetch YouTube video subtitles/transcript
from transformers import pipeline, AutoTokenizer            # Transformers library to load tokenizer and summarization pipeline
import re                                                   # For regular expressions (to extract video ID)

# Function to extract video_id from YouTube URL
def extract_video_id(url):
    # Supports both long and short YouTube URL formats
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)    # Return video ID if found
    else:
        return None              # Return None if invalid URL

# Function to generate the summary of the video subtitles
def summarize(video_url, maxlen, minlen, randomness):
    # Step 1: Extract video ID from URL
    video_id = extract_video_id(video_url)
    
    # Step 2: Load tokenizer for the summarization model
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    
    try:
        # Step 3: Fetch transcript/subtitles of the video using video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Step 4: Combine all subtitles text into one string
        subtitles_str = ""
        for entry in transcript:
            sent = entry["text"]
            subtitles_str += sent + " "
        
        # Step 5: Tokenize the subtitles text
        tokens = tokenizer.encode(subtitles_str)
        
        # Step 6: If token length exceeds model limit (1024), return "token"
        if len(tokens) > 1024:
            return "token"
        
        # Step 7: Load summarization pipeline
        summarizer = pipeline("summarization", model="t5-small")
        
        # Step 8: Generate summary with the given parameters
        summary = summarizer(subtitles_str, max_length=maxlen, min_length=minlen, do_sample=randomness)
        
        # Step 9: Return the summarized text
        return summary[0]['summary_text']
    
    except Exception as e:
        # If any error occurs, print the error and return None
        print(e)
        return None
