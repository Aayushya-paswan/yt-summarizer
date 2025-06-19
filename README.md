# YouTube Video Summarizer App

A simple Streamlit app to extract and summarize YouTube video subtitles using:

- Transformers
- youtube-transcript-api
- Streamlit
- yt-dlp (for advanced features)
- HuggingFace summarization models

---

## Features

✅ Paste any YouTube video URL  
✅ Auto-fetch English subtitles  
✅ Summarize the subtitles using transformer models  
✅ Simple and clean UI  
✅ Download summary as `.txt` file  

---

##  Live Demo

👉 https://yt-summarizer-bsr6eyoxamxq9resasxdxy.streamlit.app

---

##  How to Run Locally

Follow these simple steps to run this app on your machine:

# Step 1: Clone this repository
git clone https://github.com/Aayushya-paswan/yt-summarizer.git
cd yt-summarizer

# Step 2: (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On Linux / Mac

# Step 3: Install required packages
pip install -r requirements.txt

# Step 4: Run the Streamlit app
streamlit run main.py
