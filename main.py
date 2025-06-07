import flask
import os

app = flask.Flask(__name__)

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8081

@app.route('/')
def index():
    for _, _, files in os.walk('static/outputs'): 
        stories = files
    
    if ".gitignore" in stories: stories.remove(".gitignore")
    if ".DS_Store" in stories: stories.remove(".DS_Store")

    return flask.render_template('Index/index.html', stories=stories)

@app.route('/generate_new_story')
def generate_new_story():
    os.system("python3 story_generator.py")
    return flask.jsonify({"success": True})

app.run(SERVER_HOST, SERVER_PORT, debug=True)