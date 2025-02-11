import os
from dotenv import load_dotenv
import psycopg2

# creating a data list with a key
def key_list(data_list, key):
    mas = []
    for i in range(len(data_list)):
          mas.append(data_list[i][key])
    return mas

# create a dictionary with list of path and list of deleted files
def key_del_list(data_list):
      mas = []
      deleted = []
      for i in range(len(data_list)):
            if data_list[i]["deleted_file"] is True:
                  deleted.append(data_list[i]["new_path"])
                  break
            mas.append(data_list[i]["new_path"])
      res ={"path": mas,
          "delete": deleted}
      return res

# deleting files from folder
def delete_f(mas):
      load_dotenv()
      file_folder = os.getenv('FOLDER') + '/'
      for i in mas:
            os.remove(file_folder + i)

# taking a list of commits data
def commits_inf(data_commits, new_id):
      res = []
      for commit in data_commits:
            for id in new_id:
                  if id == commit["id"]: 
                        res.append(commit) 
                        break
      return res

# operation with database
def _base_operation(connect, operation, script):
      if operation == 'select': old_commites = []
      try:
            connection = psycopg2.connect(user=connect[0],
                                  password=connect[1],
                                  host=connect[2],
                                  port=connect[3],
                                  database=connect[4])
            cursor = connection.cursor()
            cursor.execute(script)
            connection.commit()
            if operation == 'select': 
                  record = cursor.fetchall()
                  for rec in record:
                        old_commites.append(rec)
      except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            return None

      finally:
            if connection:
                  cursor.close()
                  connection.close()
            if operation == 'select': return old_commites
            else: return 'The operation was successful'