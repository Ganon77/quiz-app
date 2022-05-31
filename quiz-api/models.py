class Answer():
    def __init__(self, text:str, isCorrect:bool):
        self.text = text
        self.isCorrect = isCorrect

class PossibleAnswers():
    def __init__(self, possibleAnswers:list[Answer]):
        self.possibleAnswers = possibleAnswers

class Question():
    def __init__(self, title:str, text:str, position:int, image:str, possibleAnswers:PossibleAnswers):
        self.title = title
        self.text = text
        self.position = position
        self.image = image
        self.possibleAnswers = possibleAnswers

class Participation():
    def __init__(self, playerName:str, answers: list[int], score: int=0):
        self.playerName = playerName
        self.answers = answers
        self.score = score