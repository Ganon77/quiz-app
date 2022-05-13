from models import Question
import sqlite3

def AddQuestionToDatabase(question:Question):
    db_connection = sqlite3.connect("../database.db")
    db_connection.isolation_level = None
    cur = db_connection.cursor()

    cur.execute("begin")

    try:
        print(question.title)
        insertion_result = cur.execute(
        f"insert into questions (title, text, position, image) values"
        f"(\"{question.title}\",\"{question.text}\",\"{question.position}\",\"{question.image}\")")
        cur.execute("commit")

        db_connection.close()
    except Exception as e:
        cur.execute('rollback')
        db_connection.close()
        raise RuntimeError(str(e))