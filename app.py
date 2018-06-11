from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DecimalField, IntegerField,BooleanField
from wtforms.validators import NumberRange, Optional
from urllib.parse import urljoin

from asciigen import convert_image

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = '/tmp'
app.config['WTF_CSRF_ENABLED'] = False

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/show/<string:filename>')
def show(filename):
    qs_params = {k: v for k, v in request.args.to_dict().items() if v}
    image_matrix = convert_image(urljoin('/tmp/', filename), **qs_params)
    return render_template('ascii.html', image_matrix=image_matrix)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = photos.save(form.photo.data)
        qs_argument = {k: v for k, v in form.data.items() if k != 'photo'}
        return redirect(url_for('show', filename=filename, **qs_argument))
    else:
        try:
            error_message = list(form.errors.values())[0][0]
        except IndexError:
            error_message = 'Unrecognized error in form validation'
        raise Exception(error_message)

@app.route('/')
def index():
    return render_template('upload.html', form=UploadForm())

@app.errorhandler(Exception)
def index_exception(error):
    return render_template('upload.html', error=error, form=UploadForm())

class UploadForm(FlaskForm):
    photo = FileField('photo', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    scale = DecimalField('scale', validators=[Optional(), NumberRange(min=0)])
    cols = IntegerField('cols', validators=[Optional(), NumberRange(min=1)])
    moreLevels = BooleanField('moreLevels', validators=[Optional()])
    edge = BooleanField('edge', validators=[Optional()])

if __name__ == '__main__':
    app.run()
