from flask import Flask
import logging

from api.views import api_bp
from bookmarks.views import bookmarks_bp
from main.views import main_bp

logging.basicConfig(filename="basic.log", level=logging.INFO)

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(bookmarks_bp, url_prefix='/bookmarks')
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
