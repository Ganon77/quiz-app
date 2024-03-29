from flask_mysqldb import MySQL
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from jwt_utils import JwtError, build_token, decode_token
from mapping import CastJsonToParticipation, CastJsonToQuestion, CastParticipationToJson, CastQuestionToJson
from services import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.environ.get("MYSQL_SERVICE_HOST")
app.config['MYSQL_USER'] = os.environ.get("DB_LOGIN")
app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")

print(app.config)

mysql = MySQL(app)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

    numberOfQuestion = GetNumberOfQuestions(mysql)
    participations = getAllParticipation(mysql)

    participations = sorted(participations, key=lambda d: d['score'], reverse=True) 
    
    return {"size": numberOfQuestion, "scores": participations}, 200


@app.route('/login', methods=['POST'])
def login():
    # username = "admin"
    password = "Vive l'ESIEE !"

    payload = request.get_json()

    if("password" not in payload.keys()):
        return {"Error": 400, "message": "must indicate a password"}, 400

    if(password != payload["password"]):
        return {"Error": 401, "message": "Wrong password"}, 401

    token = build_token()

    return {"token": token}

@app.route("/questions", methods=['POST', 'GET', 'DELETE'])
def AddQuestion():
    try:
        if(request.method == 'POST'):
            token = request.headers.get("Authorization")[7:]
            
            valid = decode_token(token)

            payload = request.get_json()

            question = CastJsonToQuestion(payload)

            AddQuestionToDatabase(question, mysql)

            return CastQuestionToJson(question)
        
        if(request.method == 'GET'):
            questions = GetAllQuestionsFromDatabase(mysql)

            return {"questions": sorted(questions, key=lambda d: d['position']) } 

        elif(request.method == 'DELETE'):
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            DeleteQuestionsFromDatabase(mysql)
            
            return {"message": "successfully deleted questions"}, 204

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except JwtError as e:
        return {"error": 401, "message": "You do not have the permission to do this", "details":e.message}, 401
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth", "details": str(e)}, 401
    except RuntimeError as e:
        return {"error": 500, "message": "Something went wrong while adding the question", "details": str(e)}, 500

@app.route("/questions/<id>", methods=['GET','DELETE', 'PUT'])
def GetOrDelQuestion(id:str):
    try:

        if(request.method == 'GET'):       

            question = GetQuestionFromDatabase(id, mysql)

            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            return CastQuestionToJson(question)

        if(request.method == 'PUT'):       
            
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            question = GetQuestionFromDatabase(id, mysql)

            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            payload = request.get_json()

            question = CastJsonToQuestion(payload)

            UpdateQuestionFromDatabase(id, question, mysql)          

            return CastQuestionToJson(question)

        elif(request.method == 'DELETE'):
            print(request.headers.get("Authorization"))
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            question = GetQuestionFromDatabase(id, mysql)

            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            DeleteQuestionFromDatabase(id, mysql)
            
            return {"question": CastQuestionToJson(question)}, 204

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except JwtError as e:
        return {"error": 401, "message": "You do not have the permission to do this", "details":e.message}, 401
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth", "details": str(e)}, 401
    except RuntimeError as e:
        return {"error": 500, "message": "Something went wrong while fetching the question", "details": str(e)}, 500
    except IndexError as e:
        return {"error": 500, "message": "Something went wrong while fetching the question", "details": str(e)}, 500


@app.route('/participations', methods=['POST', 'DELETE'])
def createParticipation():
    try:
        if(request.method == 'POST'):
            payload = request.get_json()

            participation = CastJsonToParticipation(payload)

            if(len(participation.answers) != GetNumberOfQuestions(mysql)):
                return {"error": 400, "message": "Number of answers must match the number of questions"}, 400

            participation = AddParticipationToDatabase(participation, mysql)

            return CastParticipationToJson(participation)
        elif(request.method == 'DELETE'):
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            DeleteAllParticipations(mysql)

            return {"message": "participations deleted"}, 204

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except IndexError as e:
        return {"error": 404, "message": str(e)}, 404
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth", "details": str(e)}, 401
    except RuntimeError as e:
        return {"error": 500, "message": "Something went wrong while adding the pariticipation", "details": str(e)}, 500

if __name__ == "__main__":
    app.run()