class Answer():
    def __init__(self, text, isCorrect):
        self.text = text
        self.isCorrect = isCorrect

class PossibleAnswers():
    def __init__(self, possibleAnswers):
        self.possibleAnswers = possibleAnswers

class Question():
    def __init__(self, title, text, position, image, possibleAnswers):
        self.title = title
        self.text = text
        self.position = position
        self.image = image
        self.possibleAnswers = possibleAnswers

class Participation():
    def __init__(self, playerName, answers, score=0):
        self.playerName = playerName
        self.answers = answers
        self.score = score