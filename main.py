import flask
import os

app = flask.Flask(__name__)

@app.route('/')
def index():
    for _, _, files in os.walk('static/outputs'): 
        stories = files
    
    if ".gitignore" in stories: stories.remove(".gitignore")
    if ".DS_Store" in stories: stories.remove(".DS_Store")

    return flask.render_template('Index/index.html', stories=stories)

app.run(host="0.0.0", port=8081, debug=True)