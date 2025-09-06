from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import  jsonify
from pymongo import MongoClient
from datetime import date
import datetime
import random
database = MongoClient("MONGO URL")
discord_database = database["discord"]
web_database= discord_database["WEBSITE_DATABASE"]


#######################################################
#                                quiz
                                            #######################################################
client = MongoClient("mongodb+srv://quizdatabase:quizdatabase@quizdatabase.4a1ym.mongodb.net/")

quiz_database = client["Quiz"]
ANIME_COLLECTIONS = {
    "Anime": quiz_database["Anime"],
    "Games": quiz_database["Games"],
    "WorldCapital": quiz_database["WorldCapital"],
    "Python": quiz_database["Python"]
}

ALLOWED_NAMES = [
    "Anime",
    "Games",
    "WorldCapital",
    "Python"
]

#######################################################
#                               key database
                                            #######################################################
key_database = client["KeysDatabase"] 
quiz_key_database = key_database["KeyDatabase"]                                          



def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


@app.route('/api/v1/quiz', methods=['GET'])
def anime_quiz():
    try:
        service_key = request.args.get('apikey')
        if not service_key:
            return jsonify({"Api:error": "API error: Parameter 'apikey' not fulfilled.", "code": 400}), 400
        service_name = request.args.get('QuizType')
        if not service_name:
            return jsonify({"Api:error": "API error: Parameter 'QuizType' not fulfilled.","QuizType_names":ALLOWED_NAMES, "code": 400}), 400
    except:
        return jsonify({"Api:error": "API error: Parameters 'apikey' & 'QuizType' not fulfilled.","QuizType_names":ALLOWED_NAMES, "code": 400}), 400
    service_key_entry = quiz_key_database.find_one({"apikey": service_key})
    if not service_key_entry:
        return jsonify({"Api:error": "Invalid service key.","code": 403}), 403
    expiry_time = datetime.datetime.strptime(service_key_entry["time"], '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.now() > expiry_time:
        return jsonify({"Api:error": "Usage limit exceeded. Please contact the owner and buy a new key.", "code": 403}), 403
    if service_name not in ALLOWED_NAMES:
        return jsonify({"Api:error": "API error: Invalid QuizType parameter.", "QuizType_names":ALLOWED_NAMES, "code": 400}), 400
    anime_collection = ANIME_COLLECTIONS.get(service_name)
    doc_count = anime_collection.count_documents({})
    if doc_count == 0:
        return jsonify({"Api:error": f"No quiz questions available for {service_name}.", "code": 404}), 404
    quiz_question = anime_collection.find_one({"index": random.randint(0, doc_count - 1)})
    if quiz_question:
        return jsonify({
            "Api:Message": "Request successfully validated.",
            "questions": quiz_question["data"],
            "validtill": service_key_entry["time"],
            "code": 200
        }), 200
    return jsonify({"Api:error": "Unknown error occurred.", "code": 500}), 500




@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'icon.jpg', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= random.randint(2000,9000), debug=True)
