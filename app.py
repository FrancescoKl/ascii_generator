from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from asciigen import convert_image

UPLOADED_PHOTOS_DEST = '/tmp'

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = '/tmp'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/show/<string:filename>')
def show(filename):
    image_matrix = convert_image('/tmp/' + filename, moreLevels=True)
    for row in image_matrix:
        print(row + '\n')
    return render_template('ascii.html', image_matrix=image_matrix)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('show', filename=filename))
    return render_template('upload.html')

@app.route('/')
def index():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
