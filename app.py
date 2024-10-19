from flask import Flask, request, render_template, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['youtube_url']
    format = request.form['format']

    # Set options for yt-dlp based on selected format
    ydl_opts = {
        'format': 'bestaudio' if format == 'mp3' else 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio' if format == 'mp3' else None,
            'preferredcodec': 'mp3' if format == 'mp3' else None,
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return "Download completed!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
