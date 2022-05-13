from models import Question


def CastJsonToQuestion(payload):

    keys = payload.keys()
    if("title" not in keys or "text" not in keys or "position" not in keys or "image" not in keys):
        raise KeyError("Wrong format")

    return Question(payload["title"], payload["text"] , payload["position"], payload["image"])

def CastQuestionToJson(question:Question):

    return {
        "title": question.title,
        "text": question.text,
        "position": question.position,
        "image": question.image
    }