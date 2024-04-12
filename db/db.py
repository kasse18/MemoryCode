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
                        name varchar(100),
                        second_name varchar(100),
                        patronymic varchar(100),
                        birth_data varchar(50),
                        death_data varchar(50),
                        birth_place varchar(100),
                        death_place varchar(100),
                        partner varchar(100),
                        kind varchar(100),
                        workplace varchar(100),
                        awards varchar(100),
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



async def update_data(data):
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
            cursor.execute(f"UPDATE {DB_NAME_QUESTIONS} SET {list(data.keys())[1]} = %s WHERE id = %s", [data[list(data.keys())[1]], data["id"]])

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        print(_ex)
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
            cursor.execute(f"INSERT INTO {DB_NAME_QUESTIONS} (id) VALUES (%s)", data)

        print("[INFO] add info")

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return "ok"


async def load_data_people(data):
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
                f"INSERT INTO {DB_NAME_QUESTIONS} ({", ".join(list(data.keys()))}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                list(data.value()))

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
            cursor.execute(f"SELECT * FROM {DB_NAME_QUESTIONS} WHERE id = %s", str(id))

            return_ = cursor.fetchone()
            print("Id: {}".format(return_))

    except Exception as _ex:
        warnings.warn(f"Error: {_ex}")
        return "error"

    finally:
        if connection:
            connection.close()

        return return_


async def return_data_people(id):
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


if __name__ == '__main__':
    asyncio.run(create_data_quesins())
