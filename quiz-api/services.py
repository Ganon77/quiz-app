from models import Answer, PossibleAnswers, Question
import sqlite3

database_path = "../database.db"

def AddQuestionToDatabase(question:Question):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()

    cur.execute("begin")

    try:

        insert_question = f"""insert into questions (title, text, position, image) values
        ("{question.title}","{question.text}",{question.position},"{question.image}")"""

        insertion_result = cur.execute(insert_question)

        question_id = cur.lastrowid

        print(question_id)

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

def GetQuestionFromDatabase(id:str):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    try:

        question_data = f"""SELECT questions.text, title, position, image, answers.text, isCorrect FROM questions
        JOIN answers ON answers.questionId = questions.id
        WHERE questions.id = {id}"""

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

def UpdateQuestionFromDatabase(id:str, questionUpdated:Question):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:
        update_question = f"""UPDATE questions
        SET text="{questionUpdated.text}",
        title="{questionUpdated.title}",
        position={questionUpdated.position},
        image="{questionUpdated.image}"
        WHERE id={id}"""

        delete_answers = f"""DELETE FROM answers WHERE questionId = {id}"""

        delete_result = cur.execute(update_question)
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

def DeleteQuestionFromDatabase(id:str):
    db_connection = sqlite3.connect(database_path)
    db_connection.isolation_level = None
    cur = db_connection.cursor()    

    cur.execute("begin")

    try:

        delete_answers = f"""DELETE FROM answers WHERE questionId = {id}"""
        delete_questions = f"""DELETE FROM questions WHERE id = {id}"""
                         
        delete_result = cur.execute(delete_answers)
        delete_result = cur.execute(delete_questions)
        
        cur.execute("commit")

        db_connection.close()

    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))