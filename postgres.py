import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="...",
                                  host="127.0...",
                                  port="5..2",
                                  database="test")

    cursor = connection.cursor()
    # # Executing a SQL query to insert data into  table
    # insert_query = """ INSERT INTO commits (id, short_id, created_at, title, message, author_name, author_email, authored_date, committer_name, committer_email, committed_date, web_url, is_update) VALUES
    #   ('b33eadcef84d7c3bd6130090f462698be', '1234dfd', '2024-08-06T10:19:18.000+00:00', 'Deleted Лицензия', 'Deleted Лицензия', 'ValeriyaKuular', 
    #   'vrkuular@gmail.com', '2024-08-06T10:19:18.000+00:00', 'ValeriyaKuular', 'vrkuular@gmail.com', '2024-08-06T10:19:18.000+00:00', 'http://gitlab.jelata.tech...0090f462698be', 'true')"""
    # cursor.execute(insert_query)
    # connection.commit()
    # print("1 Record inserted successfully")
    # # Fetch result
    # cursor.execute("SELECT * from commits")
    # record = cursor.fetchall()
    # print("Result ", record)

    # # Executing a SQL query to update table
    # update_query = """Update commits set title = 'new title' where id = """
    # cursor.execute(update_query)
    # connection.commit()
    # count = cursor.rowcount
    # print(count, "Record updated successfully ")
    # # Fetch result
    # cursor.execute("SELECT * from commits")
    # print("Result ", cursor.fetchall())

    # Executing a SQL query to delete table
    delete_query = """Delete from commits where id = 2"""
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    # Fetch result
    cursor.execute("SELECT * from commits")
    print("Result ", cursor.fetchall())


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")