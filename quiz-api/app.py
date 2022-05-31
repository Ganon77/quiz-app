from flask import Flask, request
from jwt_utils import JwtError, build_token, decode_token
from mapping import CastJsonToParticipation, CastJsonToQuestion, CastParticipationToJson, CastQuestionToJson
from services import *

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():

    numberOfQuestion = GetNumberOfQuestions()
    
    return {"size": numberOfQuestion, "scores": []}, 200


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

@app.route("/questions", methods=['POST'])
def AddQuestion():
    try:
        token = request.headers.get("Authorization")[7:]
        
        valid = decode_token(token)

        payload = request.get_json()

        question = CastJsonToQuestion(payload)

        AddQuestionToDatabase(question)

        return CastQuestionToJson(question)

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except JwtError as e:
        return {"error": 401, "message": "You do not have the permission to do this", "details":e.message}, 401
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth"}, 401
    except RuntimeError as e:
        return {"error": 500, "message": "Something went wrong while adding the question", "details": str(e)}, 500

@app.route("/questions/<id>", methods=['GET','DELETE', 'PUT'])
def GetOrDelQuestion(id:str):
    try:

        if(request.method == 'GET'):       

            question = GetQuestionFromDatabase(id)

            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            return CastQuestionToJson(question)

        if(request.method == 'PUT'):       
            
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            question = GetQuestionFromDatabase(id)
            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            payload = request.get_json()
            question = CastJsonToQuestion(payload)

            UpdateQuestionFromDatabase(id, question)          

            return CastQuestionToJson(question)

        elif(request.method == 'DELETE'):
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            question = GetQuestionFromDatabase(id)

            if(question is None):
                return {"error": 404, "message": f"Question with id {id} not found"}, 404

            DeleteQuestionFromDatabase(id)
            
            return {"question": CastQuestionToJson(question)}, 204

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except JwtError as e:
        return {"error": 401, "message": "You do not have the permission to do this", "details":e.message}, 401
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth"}, 401
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

            if(len(participation.answers) != GetNumberOfQuestions()):
                return {"error": 400, "message": "Number of answers must match the number of questions"}, 400

            participation = AddParticipationToDatabase(participation)

            return CastParticipationToJson(participation)
        elif(request.method == 'DELETE'):
            token = request.headers.get("Authorization")[7:]
            valid = decode_token(token)

            DeleteAllParticipations()

            return {"message": "participations deleted"}, 204

    except KeyError:
        return {"error": 400, "message": "Wrong request format"}, 400
    except IndexError as e:
        return {"error": 404, "message": str(e)}, 404
    except TypeError as e:
        return {"error": 401, "message": "You need to specify an Auth"}, 401
    except RuntimeError as e:
        return {"error": 500, "message": "Something went wrong while adding the pariticipation", "details": str(e)}, 500

if __name__ == "__main__":
    app.run()