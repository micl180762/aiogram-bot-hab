# import psycopg2
# conn = psycopg2.connect(dbname='for_python', user='postgres',
#                         password='123123123', host='localhost')
# # print(conn)
#
# cursor = conn.cursor()
# #cursor.execute("CREATE TABLE students (first_name TEXT, last_name TEXT, age INTEGER);")
# #cursor.execute("INSERT INTO students VALUES ('Mick', 'de Piani', 20);")
# #conn.commit()
# #
# # cursor.execute('SELECT version()')
# # db_version = cursor.fetchone()
# # print(db_version)
# cursor.execute('SELECT * FROM students LIMIT 10')
# records = cursor.fetchall()
# [print(row) for row in records]
# # for rec in records:
# #     print(rec)
# conn.close()