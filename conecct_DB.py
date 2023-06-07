import psycopg2
from postgres_cnf import postgre

try:
    # пытаемся подключиться к базе данных
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="rasmus78",
        database="crossD",
    )
    print("Succesful Connected.....")
    cur = connection.cursor()
    sql = """ CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        news_name TEXT,
        status INT,
        title TEXT,
        text TEXT,
        photo BYTEA,
        qwelle TEXT,
        download_day TIMESTaMP
    ) """
    cur.execute(sql)
    connection.commit()
    print("DB table is created....")
except Exception as errstr:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print(f"Can`t establish connection to database\n{errstr}")
finally:
    if connection:
        connection.close()
        print("Connection close......")
