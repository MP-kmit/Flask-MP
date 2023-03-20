from flask import Flask,Blueprint, render_template, request, flash, url_for, request, redirect, render_template
from werkzeug.utils import secure_filename
import os
import urllib.request
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, validators
from flask_login import login_required, current_user
from flask_pymongo import PyMongo
from . import db
import sqlite3

views = Blueprint('views', __name__, template_folder='Templates', static_folder='static')


UPLOAD_FOLDER = 'env/static/user_uploads/'

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["MONGO_DBNAME"] = "gallery"
app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

mongo = PyMongo(app)
f=[]

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/draw")
def draw():
    return render_template("draw.html")

@views.route("/upload")
def upload_form():
    return render_template('upload.html')
 
@views.route("/upload", methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
 
    return render_template('upload.html', filenames=file_names)

@views.route("/something" , methods=['GET'])
def SomeFunction():
    print('In SomeFunction')
    return render_template("result.html")

@views.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='user_uploads/' + filename), code=301)

@views.route("/gallery/")
def gallery():
    # global mongo
    # return render_template("gallery.html", gallery=mongo.db.gallery.find())
    imageList = os.listdir('env/static/uploads')
    imagelist = ['uploads/' + image for image in imageList]
    return render_template("gallery.html", imagelist=imagelist)


