import streamlit as st
import Summarizer
import validators
import yt_dlp
import io

st.title("YOUTUBE VIDEO SUMMARIZER")

with st.form(key="Yt_form"):
    url = st.text_input("ENTER VIDEO URL", help="Enter a valid Youtube video url with valid subtitles", placeholder="Eg: https://www.youtube.com/watch?v=7nb3gdchiKA&pp=ygUiZW5nbGlzaCBzdWJ0aXRsZXMgc3RvcnkgaW4gZW5nbGlzaA%3D%3D")
    minlen = st.number_input("MINIMUM LENGTH", value=20, help="Minimum length of the summary. Change only if needed")
    maxlen = st.number_input("MAXIMUM LENGTH", value=60, help="Maximum length of the summary. Change only if needed")
    randomness = st.radio("Randomness: ", ["high", "low"],index=1, help="How random you want your summary to be. recommended: low")

    button = st.form_submit_button("GENERATE SUMMARY")
    if button:
        if not validators.url(url):
            st.warning("INVALID URL!!", icon="⚠️")
        else:
            flag = False
            if randomness == "high":
                flag = True
            else:
                flag = False
            with st.spinner("Loading model and summarizing... Please wait ⏳"):
                summaryy = Summarizer.summarize(url, maxlen, minlen, flag)
            if summaryy == "token":
                st.warning("VIDEO LENGTH TOO LONG", icon="⚠️")

            if summaryy == None:
                st.warning("""Cannot process your request due to following reasons:\n
                              1. Invalid/No Subtitles of the video.\n
                              2. Video length too long(long tokens unsupported by the model)\n""")
            if summaryy != None and summaryy != "token":
                st.balloons()
                st.header("SUMMARY")
                st.subheader(summaryy)

                txt_buffer = io.StringIO()
                txt_buffer.write(summaryy)
                txt_buffer.seek(0)

if button:
    st.download_button(
        label="📄 Download Summary as .txt",
        data=summaryy.encode("utf-8"),
        file_name="summary.txt",
        mime="text/plain"
    )

st.markdown("""
    <p style='text-align: center; font-size: 12px; color: gray;'>
    © 2025 Aayushya Paswan. All rights reserved.
    </p>
""", unsafe_allow_html=True)
