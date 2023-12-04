from flask import Flask, render_template
flask_app_ = Flask(__name__)
@flask_app_.route('/')
def index():
    return render_template('index_data.html')

if __name__ == '__main__':
    flask_app_.run(port=8003)  # Run on a different port than FastAPI
