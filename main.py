import streamlit as st
import Summarizer    # Custom module to generate the summary
import validators    # To check if URL is valid
import yt_dlp        # Not used here but can be useful for audio extraction etc.
import io

# Main title of the app
st.title("YOUTUBE VIDEO SUMMARIZER")

# User input form for taking the YouTube URL and options
with st.form(key="Yt_form"):
    url = st.text_input("ENTER VIDEO URL", help="Enter a valid Youtube video url with valid subtitles", placeholder="Eg: https://www.youtube.com/watch?v=...")

    minlen = st.number_input("MINIMUM LENGTH", value=20, help="Minimum length of the summary. Change only if needed")
    maxlen = st.number_input("MAXIMUM LENGTH", value=60, help="Maximum length of the summary. Change only if needed")

    randomness = st.radio("Randomness: ", ["high", "low"], index=1, help="How random you want your summary to be. Recommended: low")

    button = st.form_submit_button("GENERATE SUMMARY")

    if button:
        if not validators.url(url):
            st.warning("INVALID URL!!", icon="⚠️")
        else:
            # setting randomness flag for summarizer pipeline
            flag = True if randomness == "high" else False

            with st.spinner("Loading model and summarizing... Please wait ⏳"):
                summaryy = Summarizer.summarize(url, maxlen, minlen, flag)

            # Handling possible outcomes from summarizer
            if summaryy == "token":
                st.warning("VIDEO LENGTH TOO LONG", icon="⚠️")

            elif summaryy is None:
                st.warning("""Cannot fetch request from API""")
            else:
                st.balloons()
                st.header("SUMMARY")
                st.subheader(summaryy)

                # Preparing summary as downloadable text
                txt_buffer = io.StringIO()
                txt_buffer.write(summaryy)
                txt_buffer.seek(0)

# Add download button if summary is available
if button and summaryy is not None:
    st.download_button(
        label="📄 Download Summary as .txt",
        data=summaryy.encode("utf-8"),
        file_name="summary.txt",
        mime="text/plain"
    )

# Footer note
st.markdown("""
    <p style='text-align: center; font-size: 12px; color: gray;'>
    © 2025 Aayushya Paswan. All rights reserved.
    </p>
""", unsafe_allow_html=True)
