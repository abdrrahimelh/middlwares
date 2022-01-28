from flask import Flask, jsonify, request
from pymongo import MongoClient, errors
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# global variables for MongoDB host (default port is 27017)
DOMAIN = '15.236.141.54'
PORT = 27017
 
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "root",
        password = "1234",
)
    # print the version of MongoDB server if connection successful
mydb = client.stocks
mydb = client['stocktsla']
mycol = mydb["TSLA"]
col = mydb["TSLA30"]
 
@app.route('/stock/TSLA', methods=['GET'])
def get_all_frameworks():
    output = []
    for x in mycol.find():
        output.append({'day':x['day'],'hour':x['hour']+1,'minute':x['minute'],'second' : x['second'], 'data' : x['data']})
    return jsonify({'result' : output})
 
@app.route('/stock/TSLA/30', methods=['GET'])
def get_all_framew():
    output = []
    for x in col.find():
        output.append({'Datetime':x['Datetime'],'Open' : x['Open'], 'High' : x['High'], 'Low' : x['Low'], 'Close' : x['Close']})
    return jsonify(output)
 
@app.route('/stock/TSLA/<day>/<hour>/<minute>/<second>', methods=['GET'])
def get_all_framework(day,hour,minute,second):
    output = []
    q = mycol.find_one({'day':int(day),'hour':int(hour),'minute':int(minute),'second':int(second)})
 
    if q:
        output = {'day':q['day'],'hour':q['hour'],'minute':q['minute'],'second' : q['second'], 'data' : q['data']}
    else:
        output = 'No results found'
 
    return jsonify({'result' : output})
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
 
 
