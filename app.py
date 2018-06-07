from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from asciigen import convert_image

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = '/tmp'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/show/<string:filename>')
def show(filename):
    image_matrix = convert_image('/tmp/' + filename)
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

@app.errorhandler(Exception)
def index_exception(error):
    return render_template('upload.html', error=error)


if __name__ == '__main__':
    app.run()
