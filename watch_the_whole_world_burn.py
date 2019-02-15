from app import db
import shutil, os
db.session.remove()
db.drop_all()
shutil.rmtree('migrations')
os.remove('app.db')
