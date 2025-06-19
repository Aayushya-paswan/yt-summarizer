# Import required libraries
import streamlit as st    # For creating Streamlit web app
import Summarizer         # Your own module for summarizing YouTube videos
import validators         # To validate the URL entered
import yt_dlp             # YouTube downloader library (if needed in future)
import io                 # For handling text files in memory

# Set the title of the app
st.title("YOUTUBE VIDEO SUMMARIZER")

# Create a form where user can input data
with st.form(key="Yt_form"):
    # Text input for the YouTube URL
    url = st.text_input(
        "ENTER VIDEO URL", 
        help="Enter a valid Youtube video url with valid subtitles", 
        placeholder="Eg: https://www.youtube.com/watch?v=7nb3gdchiKA&pp=ygUiZW5nbGlzaCBzdWJ0aXRsZXMgc3RvcnkgaW4gZW5nbGlzaA%3D%3D"
    )
    
    # Number input for minimum summary length
    minlen = st.number_input(
        "MINIMUM LENGTH", 
        value=20, 
        help="Minimum length of the summary. Change only if needed"
    )
    
    # Number input for maximum summary length
    maxlen = st.number_input(
        "MAXIMUM LENGTH", 
        value=60, 
        help="Maximum length of the summary. Change only if needed"
    )
    
    # Radio button for randomness (whether to generate creative/random summary)
    randomness = st.radio(
        "Randomness: ", 
        ["high", "low"], 
        index=1, 
        help="How random you want your summary to be. recommended: low"
    )

    # Submit button
    button = st.form_submit_button("GENERATE SUMMARY")

    # When the user clicks the button:
    if button:
        # First check if the entered URL is valid
        if not validators.url(url):
            st.warning("INVALID URL!!", icon="⚠️")
        else:
            # Convert radio button value into boolean flag
            flag = False
            if randomness == "high":
                flag = True
            else:
                flag = False

            # Show loading spinner while the model runs
            with st.spinner("Loading model and summarizing... Please wait ⏳"):
                summaryy = Summarizer.summarize(url, maxlen, minlen, flag)

            # If the video is too long for the model (too many tokens)
            if summaryy == "token":
                st.warning("VIDEO LENGTH TOO LONG", icon="⚠️")

            # If the function returned None → could not process the video
            if summaryy == None:
                st.warning("""Cannot process your request due to following reasons:\n
                              1. Invalid/No Subtitles of the video.\n
                              2. Video length too long(long tokens unsupported by the model)\n""")
            
            # If a valid summary is returned → display it
            if summaryy != None and summaryy != "token":
                st.balloons()  # Show animation
                st.header("SUMMARY")
                st.subheader(summaryy)

                # Prepare the summary text for download
                txt_buffer = io.StringIO()
                txt_buffer.write(summaryy)
                txt_buffer.seek(0)

# Show download button below the form if a summary is available
if button and summaryy != None:
    st.download_button(
        label="📄 Download Summary as .txt",
        data=summaryy.encode("utf-8"),
        file_name="summary.txt",
        mime="text/plain"
    )

# Footer with copyright
st.markdown("""
    <p style='text-align: center; font-size: 12px; color: gray;'>
    © 2025 Aayushya Paswan. All rights reserved.
    </p>
""", unsafe_allow_html=True)
