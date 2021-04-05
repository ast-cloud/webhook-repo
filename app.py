from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import dateutil.parser
from datetime import timedelta
app = Flask(__name__)

@app.route('/')
def index():
    client=MongoClient("mongodb+srv://ast:ast@cluster0.0kxgu.mongodb.net/action?retryWrites=true&w=majority")
    db=client.get_database('action')
    a=db.events
    print(list(a.find()))
    return render_template('index.html',list1=list(a.find()))

@app.route('/github', methods=['GET','POST'])
def newchange():
    data=request.json
    print(data)
    newdata={}
    if 'pull_request' in data.keys():
        if data['action']=='opened':
            ts=data['pull_request']['created_at']
            ts=dateutil.parser.parse(str(ts))
            ts=ts+timedelta(seconds=(5*3600)+1800)
            newdata={'request_id': data['pull_request']['id'],
                    'author': data['pull_request']['user']['login'],
                    'action': 'PULL_REQUEST',
                    'from_branch': data['pull_request']['title'],
                    'to_branch': data['repository']['default_branch'],
                    'timestamp': ts.strftime('%#I:%M %p %#d %B, %Y')
            }


    if 'pusher' in data.keys():
        ts=data['head_commit']['timestamp']
        ts=dateutil.parser.parse(str(ts))
        newdata={'request_id': data['after'],
             'author': data['head_commit']['author']['name'],
             'action': 'PUSH',
             'from_branch': data['repository']['default_branch'],
             'to_branch': data['repository']['default_branch'],
             'timestamp': ts.strftime('%#I:%M %p %#d %B, %Y')
            }
    
    if bool(newdata):
        client=MongoClient("mongodb+srv://ast:ast@cluster0.0kxgu.mongodb.net/action?retryWrites=true&w=majority")
        db=client.get_database('action')
        a=db.events
        a.insert_one(newdata)

    


    return data
        


if __name__=='__main__':
    app.run(debug=True)
