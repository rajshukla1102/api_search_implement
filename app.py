from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)
url = "https://dev.ylytic.com/ylytic/test"

@app.route('/')
def home():
    return jsonify({'comments': "hello world"})

def filter_comments(comments, search_params):

    fc = []
    for comment in comments:
        format_dt = datetime.strptime(comment['at'], '%a, %d %b %Y %H:%M:%S %Z')
        print("hello",format_dt)
        if (search_params['search_author'].lower() in comment['author'].lower()) and \
           (not search_params.get('at_from') or format_dt >= search_params['at_from']) and \
           (not search_params.get('at_to') or format_dt <= search_params['at_to']) and \
           (not search_params.get('like_from') or comment['like'] >= search_params['like_from']) and \
           (not search_params.get('like_to') or comment['like'] <= search_params['like_to']) and \
           (not search_params.get('reply_from') or comment['reply'] >= search_params['reply_from']) and \
           (not search_params.get('reply_to') or comment['reply'] <= search_params['reply_to']) and \
            (search_params['search_text'].lower() in comment['text'].lower()):
            fc.append(comment)
    return fc


@app.route('/search', methods=['GET'])
def search_comments():
    search_params = {
        'search_author': request.args.get('search_author','').lower(),
        'at_from': datetime.strptime(request.args.get('at_from', ''), '%d-%m-%Y') if request.args.get('at_from') else None,
        'at_to': datetime.strptime(request.args.get('at_to', ''), '%d-%m-%Y') if request.args.get('at_to') else None,
        'like_from': int(request.args.get('like_from')) if request.args.get('like_from') else None,
        'like_to': int(request.args.get('like_to')) if request.args.get('like_to') else None,
        'reply_from': int(request.args.get('reply_from')) if request.args.get('reply_from') else None,
        'reply_to': int(request.args.get('reply_to')) if request.args.get('reply_to') else None,
        'search_text': request.args.get('search_text', '').lower()
    }
    response = requests.get(url)
    print(search_params['search_author'])
    if response.status_code != 200:
        return jsonify({'error': 'Error fetching comments.'})

    comments = response.json()['comments']
    filtered_comments = filter_comments(comments, search_params)

    return jsonify({'comments': filtered_comments}), 200
