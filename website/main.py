from flask import Blueprint,request
from flask import render_template,send_file
from flask_login import login_required, current_user
from io import BytesIO
from models import Upload, AccessKey
from models import db
from aes256 import aes256
from Crypto.Cipher import AES
import secrets


main = Blueprint('main', __name__)
import os
@main.route('/')
def index():
    return render_template('index.html',loggedin=current_user.is_authenticated)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname,lname=current_user.lname, email=current_user.email, loggedin=current_user.is_authenticated)




######################## MODULE 1 #################################
@main.route('/upload')
@login_required
def upload():
    #fetch filenames uploaded by the user
    uploaded_files = [upload.filename for upload in current_user.uploads]
    print(uploaded_files)

    return render_template('upload.html',display=False,loggedin=current_user.is_authenticated)

@main.route('/upload',methods=['POST'])
@login_required
def upload_post():
    if('uploadfile' in request.files):
        file = request.files['uploadfile']
        data=file.read()
            
        AES256 = aes256()
        rn = secrets.token_bytes(32)
        key = AES256.shake_256(secrets.token_bytes(48), 32)
        message = data + (16 - len(data) % 16) * b'\0' #padding to a multple of 16
        print(key)

        # encrypt AES256
        iv = AES256.shake_256(rn, AES.block_size)
        ct = AES256.encrypt(key, message, iv)
        
        #save public key
        upload = Upload(filename=file.filename, data=ct, iv=iv, user_id=current_user.id)
        db.session.add(upload)
        db.session.commit()

        #save private key
        access_key = AccessKey(upload_id=upload.id,key=key, user_id=current_user.id)
        db.session.add(access_key)
        db.session.commit()
        
    return render_template('upload.html', fileID=upload.id,display=True,loggedin=current_user.is_authenticated)


@main.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()

    access_key = AccessKey.query.filter_by(upload_id=upload.id, user_id=current_user.id).first()
    if access_key:
        # decrypt AES256
        AES256 = aes256()
        key=access_key.key
        ct=upload.data
        iv=upload.iv
        pt = AES256.decrypt(ct, key, iv)
        
        return send_file(BytesIO(pt), download_name=upload.filename, as_attachment=True )
    else:
        return "Access Denied", 403
    