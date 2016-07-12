import subprocess
import sys
import os
from flask import Flask, flash, redirect, request, render_template, url_for

DEBUG = False
SECRET_KEY = 'this is needed for flash messages'

BINARY = '/usr/bin/youtube-dl'
DEST_DIR = '/home/dash/down/static/videos/'
#DEST_DIR = '/home/vagrant/git/down/static/videos'
OUTPUT_TEMPLATE = '%s/%%(title)s-%%(id)s.%%(ext)s' % DEST_DIR

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        print url
        p = subprocess.Popen([BINARY, '-o', OUTPUT_TEMPLATE, '-q', url])
        p.communicate()
        flash('Successfully downloaded!', 'success')
        return redirect(url_for('videos'))
    return render_template('download.html')

# For holding all of the videos
@app.route('/videos')
def videos():
    names = os.listdir(os.path.abspath(DEST_DIR))
    return render_template('videos.html', video_url=names)

# For deleting specified file
@app.route('/delete/<filename>')
def remove_file(filename):
    filename_full = os.path.join(DEST_DIR, filename)
    print filename_full
    os.remove(filename_full)
    return redirect(url_for('videos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8801)
