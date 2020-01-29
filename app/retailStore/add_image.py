from app import app, db
from app.models import Item, Receipt, Image
import os
import requests

# Checks to see if the image is in the database. If it isn't than it downloads
#   the image and saves the path of the file location.
def add_image_to_folder(url_path, upc):
    i = Image.query.filter_by(url_path=url_path).first()

    if i is None or not i.in_db(url_path):
        print('Img not in db')
        imgData = requests.get(url_path).content
        with open(os.path.join(app.config['IMG_DIR'], str(upc+'.jpg')), 'wb') as handler:
            handler.write(imgData)

        i = Image(url_path=url_path, file_name=upc)
        db.session.add(i)
        db.session.commit()
        return i.id
    else:
        print('Img in db')
        return i.id
