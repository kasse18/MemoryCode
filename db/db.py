import psycopg2
import asyncio
from dotenv import load_dotenv
import warnings
import os

load_dotenv()

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DB_NAME = os.environ.get("DB_NAME_PEOPLE")
DB_NAME_QUESTIONS = os.environ.get("DB_NAME_QUESTIONS")

warnings.simplefilter("always")


async def create_data_people():
    connection = None

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                F"""CREATE TABLE {DB_NAME}(
                        id INT,
                        first_name varchar(100),
                        last_name varchar(100),
                        surname varchar(100),
                        data_born varchar(50),
                        data_die varchar(50),
                        epitaph varchar(10000),
                        biography_1 varchar(10000),
                        biography_2 varchar(10000),
                        biography_3 varchar(10000),
                        biography_4 varchar(10000),
                        word_familiar varchar(10000)
                        );
                        """
            )
        print("[INFO] Table created")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"


async def create_data_quesins():
    connection = None

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                F"""CREATE TABLE {DB_NAME_QUESTIONS}(
                        id INT,
                        question_1 varchar(10000),
                        question_2 varchar(10000),
                        question_3 varchar(10000),
                        question_4 varchar(10000),
                        question_5 varchar(10000),
                        question_6 varchar(10000),
                        question_7 varchar(10000),
                        question_8 varchar(10000),
                        question_9 varchar(10000),
                        question_10 varchar(10000));"""
            )
        print("[INFO] Table created")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"




async def load_data(data):
    connection = None
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO {DB_NAME} (id, name, biography, epitaph) VALUES (%s, %s, %s, %s)", data)

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"


async def load_data_quesions(data):
    connection = None
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {DB_NAME_QUESTIONS} (id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                data)

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"


async def return_data(id):
    connection = None
    return_ = ""

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {DB_NAME} WHERE id = %s", str(id))

            return_ = cursor.fetchone()
            print("Id: {}".format(return_))

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return return_


async def put_data(data):
    connection = None
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE {DB_NAME} SET name = '%s'  WHERE id = %s", data)

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"


async def put_data_question(data):
    connection = None
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE {DB_NAME_QUESTIONS} SET name = '%s'  WHERE id = %s", data)

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"

if __name__ == '__main__':
    asyncio.run(create_data_people())
