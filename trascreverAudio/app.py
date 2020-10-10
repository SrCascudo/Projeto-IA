import os
import speech_recognition as sr
from fuzzywuzzy import fuzz

import youtube_dl
from pydub import AudioSegment
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/converter/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('upload_arq', None)
        link = request.form['youtube']
        if link is not None:
            coverter = transcrever(download(link))
            possibilidade = 'A Pauta tem {}% de chance de estar no video'.format(fuzz.partial_ratio(coverter, request.form['pauta']))
            return render_template('index.html', conversion=coverter, possibilidade=possibilidade)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = convert_format(filename, str.replace(filename, '.mp3', ''))
            return render_template('index.html', conversion=transcrever(filename))


def transcrever(nome_arq):
    r = sr.Recognizer()
    file = sr.AudioFile(nome_arq)
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio, language='pt-br')
        delete_dir()
    return result.__str__().upper()


def convert_format(before_name, after_name):
    sound = AudioSegment.from_mp3(UPLOAD_FOLDER + before_name)
    sound.export(UPLOAD_FOLDER + after_name + '.wav', format="wav")
    return UPLOAD_FOLDER + after_name + '.wav'


def download(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': UPLOAD_FOLDER + '/converter.%(ext)s',

    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return UPLOAD_FOLDER + 'converter.wav'


def delete_dir():
    for files in os.walk(UPLOAD_FOLDER):
        for file in files[2]:
            os.remove(UPLOAD_FOLDER+file)


if __name__ == '__main__':
    app.run()
