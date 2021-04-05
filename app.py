from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/github', methods=['GET','POST'])
def newchange():
    data=request.json
    print(data)
    newdata={}
    if 'pull_request' in data.keys():
        if data['action']=='opened':
            newdata={'request_id': data['pull_request']['id'],
                    'author': data['pull_request']['user']['login'],
                    'action': 'PULL_REQUEST',
                    'from_branch': data['pull_request']['title'],
                    'to_branch': data['repository']['default_branch'],
                    'timestamp': data['pull_request']['created_at']
            }


    if 'pusher' in data.keys():
        newdata={'request_id': data['after'],
             'author': data['head_commit']['author']['name'],
             'action': 'PUSH',
             'from_branch': data['repository']['default_branch'],
             'to_branch': data['repository']['default_branch'],
             'timestamp': data['head_commit']['timestamp']
            }
    
    if bool(newdata):
        client=MongoClient("mongodb+srv://ast:ast@cluster0.0kxgu.mongodb.net/action?retryWrites=true&w=majority")
        db=client.get_database('action')
        a=db.events
        a.insert_one(newdata)

    


    return data
        


if __name__=='__main__':
    app.run(debug=True)
