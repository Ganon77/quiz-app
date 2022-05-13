from flask import Flask, request
from jwt_utils import build_token

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200


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

    return {"access_token": token}

if __name__ == "__main__":
    app.run(ssl_context='adhoc')