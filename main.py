from flask import Flask, render_template, request, send_from_directory
from summarizer import web_scrapping, text_summarization, youtube_summarization, text_to_speech

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    choice = request.form['choice']
    summary = ""
    if choice == '1':
        link = request.form['link']
        summary = web_scrapping(link)
    elif choice == '2':
        text = request.form['text']
        summary = text_summarization(text)
    elif choice == '3':
        video_link = request.form['video_link']
        summary = youtube_summarization(video_link)

    # TEXT TO SPEAK
    listen = request.form.get('listen')
    audio_file = None
    if listen == "yes":
        audio_file = text_to_speech(summary)

    return render_template('result.html', summary=summary, audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
