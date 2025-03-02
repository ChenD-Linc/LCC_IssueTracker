import os
import secrets
from PIL import Image
from flask import current_app
from app import app

def save_profile_picture(form_picture):
    """
    Save profile picture with a randomized name to prevent conflicts
    and resize it to a standard size to save storage space
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
    
    # Resize image to save space
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_filename

def delete_profile_picture(filename):
    """
    Delete a profile picture file if it's not the default
    """
    if filename != 'default.jpg':
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            # If file doesn't exist or can't be deleted, just continue
            pass