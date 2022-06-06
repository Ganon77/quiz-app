from mapping import CastParticipationToJson, CastQuestionToJson
from models import Answer, Participation, PossibleAnswers, Question
import sqlite3

database_path = "../database.db"

def GetNumberOfQuestions():
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()

    try:

        question_data = """SELECT * FROM questions"""

        get_result = cur.execute(question_data)

        rows = cur.fetchall()

        return len(rows)

    except Exception as e:
        db_connection.close()
        raise RuntimeError(str(e))


def AddQuestionToDatabase(question:Question):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()

    cur.execute("begin")

    try:

        update_question_all = f"""UPDATE questions
        SET position=position+1
        WHERE position >= {question.position}"""

        insert_question = f"""insert into questions (title, text, position, image) values
        ("{question.title}","{question.text}",{question.position},"{question.image}")"""

        cur.execute(update_question_all)

        insertion_result = cur.execute(insert_question)
        

        question_id = cur.lastrowid

        for answer in question.possibleAnswers.possibleAnswers:
            insert_answers = f"""insert into answers (text, isCorrect, questionId) values
            ("{answer.text}", {answer.isCorrect}, {question_id})"""

            insertion_answer = cur.execute(insert_answers)

        cur.execute("commit")        

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))

def GetAllQuestionsFromDatabase():
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    try:

        question_data = f"""SELECT questions.text, title, position, image, answers.text, isCorrect FROM questions
        JOIN answers ON answers.questionId = questions.id"""

        get_result = cur.execute(question_data)

        rows = cur.fetchall()

        questions = []
        answers = []

        for i in range(1, len(rows)):
            if i % 4 == 0:
                question = Question(title=rows[i-1][1], text=rows[i-1][0], position=rows[i-1][2], image=rows[i-1][3], possibleAnswers=PossibleAnswers(answers))
                questions.append(CastQuestionToJson(question))
                answers = []
                answers.append(Answer(text=rows[i][-2], isCorrect=bool(rows[i-1][-1])))
            else:
                answers.append(Answer(text=rows[i][-2], isCorrect=bool(rows[i-1][-1])))
                
        
        question = Question(title=rows[-1][1], text=rows[-1][0], position=rows[-1][2], image=rows[-1][3], possibleAnswers=PossibleAnswers(answers))
        questions.append(CastQuestionToJson(question))

        db_connection.close()

        return questions

    except Exception as e:
        db_connection.close()
        raise RuntimeError(str(e))

def GetQuestionFromDatabase(position:str):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    try:

        question_data = f"""SELECT questions.text, title, position, image, answers.text, isCorrect FROM questions
        JOIN answers ON answers.questionId = questions.id
        WHERE questions.position = {position}"""

        get_result = cur.execute(question_data)

        rows = cur.fetchall()

        if(len(rows) == 0):
            return None

        answers = []

        for row in rows:
            answers.append(Answer(text=row[-2], isCorrect=bool(row[-1])))

        question = Question(title=rows[0][1], text=rows[0][0], position=rows[0][2], image=rows[0][3], possibleAnswers=PossibleAnswers(answers))

        db_connection.close()

        return question

    except Exception as e:
        db_connection.close()
        raise RuntimeError(str(e))

def UpdateQuestionFromDatabase(position:str, questionUpdated:Question):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:

        question = f"""SELECT id, position FROM questions WHERE position = {position}"""
        cur.execute(question)

        rows = cur.fetchall()

        id = rows[0][0]
        old_position = rows[0][1]

        if(old_position < questionUpdated.position):
            update_question_all_back = f"""UPDATE questions
            SET position=position-1
            WHERE position <= {questionUpdated.position} AND position > {old_position}"""
            cur.execute(update_question_all_back)
        elif(old_position > questionUpdated.position):
            update_question_all_back = f"""UPDATE questions
            SET position=position+1
            WHERE position >= {questionUpdated.position} AND position < {old_position}"""
            cur.execute(update_question_all_back)


        update_question = f"""UPDATE questions
        SET text="{questionUpdated.text}",
        title="{questionUpdated.title}",
        position={questionUpdated.position},
        image="{questionUpdated.image}"
        WHERE id={id}"""

        delete_answers = f"""DELETE FROM answers WHERE questionId = {id}"""        
        cur.execute(update_question)
        delete_result = cur.execute(delete_answers)

        for answer in questionUpdated.possibleAnswers.possibleAnswers:
            insert_answers = f"""insert into answers (text, isCorrect, questionId) values
            ("{answer.text}", {answer.isCorrect}, {id})"""
            insertion_answer = cur.execute(insert_answers)
                    
        cur.execute("commit")

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))

def DeleteQuestionFromDatabase(position:str):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:

        question = f""" SELECT id FROM questions WHERE position = {position}"""

        cur.execute(question)

        rows = cur.fetchall()

        id = rows[0][0]

        delete_answers = f"""DELETE FROM answers WHERE questionId = {id}"""
        delete_questions = f"""DELETE FROM questions WHERE id = {id}"""
                         
        delete_result = cur.execute(delete_answers)
        delete_result = cur.execute(delete_questions)

        update_question_all_back = f"""UPDATE questions
            SET position=position-1
            WHERE position > {position}"""

        print(update_question_all_back)
        cur.execute(update_question_all_back)
        
        cur.execute("commit")

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))

def DeleteQuestionsFromDatabase():
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:


        delete_answers = f"""DELETE FROM answers"""
        delete_questions = f"""DELETE FROM questions"""
                         
        delete_result = cur.execute(delete_answers)
        delete_result = cur.execute(delete_questions)
        
        cur.execute("commit")

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))


def AddParticipationToDatabase(participation:Participation):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()

    cur.execute("begin")

    try:

        insert_player = f"""insert into participation (playerName) values
        ("{participation.playerName}")"""

        cur.execute(insert_player)

        player_id = cur.lastrowid

        for i in range(len(participation.answers)):

            get_question = f"""SELECT id FROM questions WHERE position={i+1}"""

            get_result = cur.execute(get_question)

            rows = cur.fetchall()

            if(len(rows) == 0):
                raise IndexError("Not found")

            questionId = rows[0][0]

            get_answers = f"""SELECT id, isCorrect FROM answers WHERE questionId={questionId}"""

            get_result = cur.execute(get_answers)

            if(len(rows) == 0):
                raise IndexError(f"No answers for question with id : {questionId}")

            rows = cur.fetchall()

            answerId = rows[participation.answers[i] - 1][0]           

            if(rows[participation.answers[i] - 1][1]):
                participation.score += 1

            insert_player_answer = f"""insert into playerAnswer (playerId, answerId) values
            ({player_id}, {answerId})"""

            cur.execute(insert_player_answer)

        update_question = f"""UPDATE participation
        SET score={participation.score}
        WHERE id={player_id}"""

        cur.execute(update_question)

        cur.execute("commit")        

        db_connection.close()

        return participation
        
    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))


def DeleteAllParticipations():
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:

        delete_participation = f"""DELETE FROM participation"""
        delete_answers = f"""DELETE FROM playerAnswer"""
                         
        delete_result = cur.execute(delete_participation)
        delete_result = cur.execute(delete_answers)
        
        cur.execute("commit")

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))


def getAllParticipation():
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    try:

        delete_participation = f"""SELECT DISTINCT playerName,score FROM participation JOIN playerAnswer ON participation.id = playerAnswer.playerId"""
                         
        delete_result = cur.execute(delete_participation)

        rows = cur.fetchall()

        participations = []

        for row in rows:
            participations.append(CastParticipationToJson(Participation(answers=[], playerName=row[0], score=row[1])))
        
        db_connection.close()

        return participations

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))