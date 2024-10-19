from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloaded_files'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fungsi untuk download video dari YouTube
def download_youtube_video(url, format='mp4'):
    if format == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }
    elif format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['youtube_url']
    format_type = request.form['format']

    # Download the YouTube video based on format (mp4 or mp3)
    download_youtube_video(youtube_url, format=format_type)
    
    return redirect(url_for('download_complete'))

@app.route('/download_complete')
def download_complete():
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template('download_complete.html', files=files)

@app.route('/downloaded_files/<filename>')
def get_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
