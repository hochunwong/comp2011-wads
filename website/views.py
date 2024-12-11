from flask import Blueprint, render_template, request, flash, url_for, redirect, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import User, Livery, Like
import uuid
import os


views = Blueprint('views', __name__)



@views.route('/')
def index():
    return render_template("index.html", user=current_user)


@views.route('/liveries')
def liveries():
    liveryList = Livery.query.all()
    return render_template("liveries.html", user=current_user, liveryList=liveryList)


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        type = request.form.get('type')
        name = request.form.get('name')
        img = request.files['img']

        fileName = str(uuid.uuid1()) + secure_filename(img.filename)
        mimeType = img.mimetype
        print(mimeType)

        if len(title) < 1:
            flash("Please input title.", category="error")
        elif len(desc) < 1:
            flash("Please input description.", category="error")
        elif type == "Select Type":
            flash("Please select vehicle type.", category="error")
        elif len(name) < 1:
            flash("Please input vehicle name.", category="error")
        elif len(desc) < 1:
            flash("Please input description.", category="error")
        #elif not img:
        #    flash("Please upload an image.", category="error")
        elif img and (mimeType != "image/jpeg" and mimeType != "image/png"):
            flash("Only png and jpg images supported.", category="error")
        else:
            if img:
                if not os.path.exists(current_app.config['UPLOADS']):
                    os.makedirs(current_app.config['UPLOADS'])
                img.save(os.path.join(current_app.config['UPLOADS'], fileName))
            else:
                fileName = ''

            new_livery = Livery(user_id=current_user.id, title=title, desc=desc, type=type, name=name, img=fileName)
            db.session.add(new_livery)
            db.session.commit()
            flash("Livery uploaded successfully!", category="success")
            return redirect(url_for('views.liveries'))

    return render_template("upload.html", user=current_user)


@views.route("/like/<livery_id>", methods=['GET'])
@login_required
def likePost(livery_id):
    livery = Livery.query.filter_by(id=livery_id)
    like = Like.query.filter_by(user_id=current_user.id, livery_id=livery_id).first()

    if not livery:
        flash("Error liking post: livery not found", category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
        flash("Like removed.", category="success")
    else:
        like = Like(user_id=current_user.id, livery_id=livery_id)
        db.session.add(like)
        db.session.commit()
        flash("Liked livery!", category="success")

    return redirect(url_for('views.liveries'))
