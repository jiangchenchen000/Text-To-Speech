import streamlit as st
from gtts import gTTS
import tempfile
from PyPDF2 import PdfReader
import docx

st.set_page_config(
    page_title="Text-to-Speech",
    page_icon="✅", 
)

LANGUAGES = {
    'English': 'en',
    'Japanese' : 'ja',
    'Spanish': 'es',
    'French': 'fr',
}

# Get the text to speech
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    return tts

# Read the pdf
def read_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)

    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    return text

# Read the .docx
def read_docx(file):
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def main():
    st.title("Text-to-Speech")

    # Create a sidebar for radio options
    st.sidebar.title("Options")
    text_input_method = st.sidebar.radio("Select the text input method:", ("Text", "Document"))

    # Get user input based on the radio option selected
    if text_input_method == "Text":
        text = st.text_area("Enter the text you want to convert to speech:")
    else:
        file = st.file_uploader("Document (PDF or DOCX):", type=["pdf", "docx"])
        if file:
            if file.type == "application/pdf":
                text = read_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = read_docx(file)
        else:
            text = ""

    lang = st.sidebar.selectbox("Select a language:", options=list(LANGUAGES.keys()))

    # Convert the text
    if st.button("Convert Text to Speech"):
        if text:
            with st.spinner("Converting..."):
                tts = text_to_speech(text, LANGUAGES[lang])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format="audio/mp3")
                    # st.download_button("Download Audio", fp.name, key='audio_download')
                    st.markdown(get_binary_file_downloader_html(fp.name, "Download Audio", "mp3"), unsafe_allow_html=True)
                    # st.write('<span style="color: red;">Note: The downloaded file is a text file.Paste the path in the explorer to get the audio file.</span>', unsafe_allow_html=True)

                    # st.write(
                    #     "Note: The downloaded file is a text file. "
                    #     "Paste the path in the explorer to get the audio file."
                    # )
        else:
            st.warning("Please enter some text or upload a document to convert.")

def get_binary_file_downloader_html(file_path, label="Download", key="default"):
    with open(file_path, "rb") as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'data:application/octet-stream;base64,{b64}'
    return f'<a href="{href}" download="{key}.mp3">{label}</a>'

if __name__ == '__main__':
    main()
