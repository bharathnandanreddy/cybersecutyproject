from flask import Blueprint,request
from flask import render_template,send_file
from flask_login import login_required, current_user
from io import BytesIO
from models import Upload
from models import db

main = Blueprint('main', __name__)
import os
@main.route('/')
def index():
    
    return render_template('index.html',loggedin=current_user.is_authenticated)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname,lname=current_user.lname, email=current_user.email, loggedin=current_user.is_authenticated)


@main.route('/upload')
@login_required
def upload():
    uploaded_file_ids = [upload.upload_date for upload in current_user.uploads]
    print(uploaded_file_ids)
    return render_template('upload.html',display=False,loggedin=current_user.is_authenticated)

@main.route('/upload',methods=['POST'])
@login_required
def upload_post():
    if('uploadfile' in request.files):
        file = request.files['uploadfile']
        upload = Upload(filename=file.filename, data=file.read(),user_id=current_user.id)
        db.session.add(upload)
        db.session.commit()
        print(upload.id)
    
        
    return render_template('upload.html', fileID=upload.id,display=True,loggedin=current_user.is_authenticated)


@main.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True )