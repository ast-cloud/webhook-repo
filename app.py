from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import dateutil.parser
from datetime import timedelta
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    client=MongoClient("mongodb+srv://ast:ast@cluster0.0kxgu.mongodb.net/action?retryWrites=true&w=majority")                    
    db=client.get_database('action')
    a=db.events
    listrev=list(a.find())
    listrev=listrev[::-1]           #Reversing list so that latest entry appear first in UI
    listrev.append({'datet':datetime.now()})
    print(listrev)
    
    return render_template('index.html',datalist=listrev)

@app.route('/github', methods=['GET','POST'])   #Route which processes webhook request
def newchange():
    data=request.json
    newdata={}
    if 'pull_request' in data.keys():  #Distinguishing between pull_request and push by seeing keys in json data
        if data['action']=='opened':     #Create new database entry only if it is a opened pull request
            ts=data['pull_request']['created_at']
            ts=dateutil.parser.parse(str(ts))
            ts=ts+timedelta(seconds=(5*3600)+1800)   #Adding 5:30 hrs for IST
            newdata={'request_id': data['pull_request']['id'],
                    'author': data['pull_request']['user']['login'], #Couldn't find author name in pull_request post message so saved 'github username' instead
                    'action': 'PULL_REQUEST',
                    'from_branch': data['pull_request']['head']['ref'],
                    'to_branch': data['pull_request']['base']['ref'],
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
    
    if bool(newdata):           #Avoiding empty entries in database
        client=MongoClient("mongodb+srv://ast:ast@cluster0.0kxgu.mongodb.net/action?retryWrites=true&w=majority")
        db=client.get_database('action')
        a=db.events
        a.insert_one(newdata)

    return data
        


if __name__=='__main__':
    app.run(debug=True)
