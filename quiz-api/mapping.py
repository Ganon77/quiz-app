from models import Answer, PossibleAnswers, Question


def CastJsonToQuestion(payload):

    keys = payload.keys()
    if("title" not in keys or "text" not in keys or "position" not in keys or "image" not in keys or "possibleAnswers" not in keys):
        raise KeyError("Wrong format")

    possibleAnswer = CastJsonToPossibleAnswers(payload["possibleAnswers"])

    return Question(payload["title"], payload["text"] , payload["position"], payload["image"], possibleAnswer)

def CastQuestionToJson(question:Question):

    return {
        "title": question.title,
        "text": question.text,
        "position": question.position,
        "image": question.image,
        "possibleAnswers": CastPossibleAnswersToJson(question.possibleAnswers)
    }


def CastJsonToAnswer(json):
    keys = json.keys()
    if("text" not in keys or "isCorrect" not in keys):
        raise KeyError("Wrong format")

    answer = Answer(json["text"], json["isCorrect"])

    return answer

def CastAnswerToJson(answer: Answer):
    return {
        "text": answer.text,
        "isCorrect": answer.isCorrect
    }

def CastJsonToPossibleAnswers(json):

    if(type(json) != list):
        raise TypeError("Wrong format")

    answers = [CastJsonToAnswer(obj) for obj in json]

    return PossibleAnswers(answers)

def CastPossibleAnswersToJson(answers: PossibleAnswers):
    return [
        CastAnswerToJson(answer) for answer in answers.possibleAnswers
    ]