import flask
from flask import request, jsonify
import json
import os


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/news_api/renew', methods=['GET'])
def renew():
    os.system("python3 1.py")
    return '''<h1>DONE</h1>'''



@app.route('/news_api', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'q' in request.args:
        title = request.args['q']
    else:
        return "Error: No id field provided. Please specify an title."
    if 'n' in request.args:
        n = int(request.args['n'])
    if 'w' in request.args:
        w = int(request.args['w'])

    # Create an empty list for our results
    results = []

    #Open json file
    with open('yahoo-news.json') as f:
        news = json.load(f)
        print(news)

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for new in news:
        if n == 0:
            break
        if (title in new['title']) or (title in new['content']):
            n -= 1
            t = new['title']
            url = new['url']
            c = new['content'][:w]
            tmp = {'title':t, 'url':url, 'content':c}
            results.append(tmp)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
