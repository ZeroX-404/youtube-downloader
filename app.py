from flask import Flask, send_from_directory, render_template
import os
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloaded_files'

@app.route('/')
def index():
    # Daftar file yang ada di folder downloaded_files
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

def convert_video(url, format):
    # Contoh konversi menggunakan yt-dlp
    ydl_opts = {
        'format': format,
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    # Buat folder jika tidak ada
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)  # Jalankan di semua alamat IP pada port 5000
