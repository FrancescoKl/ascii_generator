"""
Flask app
"""
import os

from urllib.parse import urljoin

from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DecimalField, IntegerField, BooleanField
from wtforms.validators import NumberRange, Optional
from werkzeug.utils import secure_filename

from asciigen import convert_image
from exception import FormValidationFailed

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = '/tmp'
app.config['WTF_CSRF_ENABLED'] = False

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/show/<string:filename>')
def show(filename):
    """
    View for rendering ascii matrix
    :param filename: image path
    :return: ascii.html
    """
    qs_params = {k: v for k, v in request.args.to_dict().items() if v}
    photo_path = urljoin('/tmp/', secure_filename(filename))
    image_matrix = convert_image(photo_path, **qs_params)
    try:
        #os.remove(photo_path)
        pass
    except OSError:
        print(f'{photo_path} not found')
    return render_template('ascii.html', image_matrix=image_matrix)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Upload image
    :return: redirect to ascii.html
    """
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = photos.save(form.photo.data)
        qs_argument = {k: v for k, v in form.data.items() if k != 'photo'}
        return redirect(url_for('show', filename=filename, **qs_argument))
    else:
        try:
            error_message = list(form.errors.values())[0][0]
            raise FormValidationFailed(error_message)
        except IndexError:
            raise FormValidationFailed()


@app.route('/')
def index():
    """
    View for index page
    :return: upload.html
    """
    return render_template('upload.html', form=UploadForm())


@app.errorhandler(Exception)
def index_exception(error):
    """
    View for error
    :param error: exception handled
    :return: upload.html
    """
    return render_template('upload.html', error=error, form=UploadForm())


class UploadForm(FlaskForm):
    """
    Form for upload
    """
    photo = FileField('photo', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    scale = DecimalField('scale', validators=[Optional(), NumberRange(min=0)])
    cols = IntegerField('cols', validators=[Optional(), NumberRange(min=1)])
    morelevels = BooleanField('moreLevels', validators=[Optional()])
    edge = BooleanField('edge', validators=[Optional()])


if __name__ == '__main__':
    app.run()
