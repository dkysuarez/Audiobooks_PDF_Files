import streamlit as st
import pyttsx3
import PyPDF2
import time

st.title("Convert file to audio")
img = ("https://observatorio.tec.mx/wp-content/uploads/2022/05/audiolibros.jpeg")
st.image(img, caption='Audiobooks' )

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://observatorio.tec.mx/wp-content/uploads/2022/05/audiolibros.jpeg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True) 

class TextToSpeech:
    engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume: float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty('voice', voice)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def list_avalilable_voices(self):
        voices: list = [self.engine.getProperty('voices')]

        for i, voice in enumerate(voices[0]):
            print(
                f'{i + 1} {voice.name} {voice.age}: {voice.languages[0]} ({voice.gender}) [{voice.id}]')


def main():
    
    file = st.sidebar.file_uploader("Upload your PDF file", type="pdf")
    if file is not None:
        #uses PyPDF2 library to read it
        pdfReader = PyPDF2.PdfReader(file)
        pages = len(pdfReader.pages)
        st.sidebar.write(f"The file has {pages} pages.")
        speaker = pyttsx3.init()
        text = ''

        for num in range(pages):
            page = pdfReader.pages[num]
            text += page.extract_text()
            #speaker.say(text)
            speaker.save_to_file(text,"audio.mp3")
            speaker.runAndWait()
            
            time.sleep(0.5) #pause between pages

            #Displays the pdf converted to audio
            st.sidebar.audio('audio.mp3')
        speaker.stop()



if __name__ == "__main__":
# Set voices, speed and volume
    tts = TextToSpeech(None, 180, 1.0)
    main()


