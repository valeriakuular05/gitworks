import os
from dotenv import load_dotenv
import requests
from libs.func import key_list, key_del_list, delete_f, commits_inf, _base_operation
from base64 import b64decode
import urllib.parse

load_dotenv()
token = os.getenv('TOKEN')
_user = os.getenv('USERNAME')
passw = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
_api_url = os.getenv('API_URL')

while True:
      api_url = _api_url + "/repository/commits"
      headers = {"PRIVATE-TOKEN": token}
      response = requests.get(api_url, headers=headers)
      #upload all commits from gitlab
      commits = response.json()                             
      connection = (_user,passw,host,port, database)
      data_base = _base_operation(connection, 'select', 'SELECT * FROM commits')     

      # ID of old commits from the database
      old_commits = []
      for comm in data_base:
            old_commits.append(comm[0])
      # creating a list of ID new commits
      commits_id = list(set(key_list(commits, "id")) - set(old_commits))  
      # the data list of new commits
      commits_info = commits_inf(commits, commits_id)                    
      # insert new commits into data base
      for commit in commits_info:        
            insert_query = f""" INSERT INTO commits (id, short_id, created_at, title, message, author_name, author_email, authored_date, committer_name, committer_email, committed_date, web_url, is_update) VALUES ('{commit['id']}', '{commit['short_id']}', '{commit['created_at']}', '{commit['title']}', '{commit['message']}', '{commit['author_name']}','{commit['author_email']}', '{commit['authored_date']}', '{commit['committer_name']}', '{commit['committer_email']}', '{commit['committed_date']}', '{commit['web_url']}', 'true')"""
            res = _base_operation(connection, 'insert', insert_query)

      file_folder = os.getenv('FOLDER')
      deleted_files = [] 
      # find path of files
      for commithash in commits_id:    
            api_url = _api_url + f'/repository/commits/{commithash}/diff'
            response = requests.get(api_url, headers=headers)
            path = (key_del_list(response.json()))["path"]    
            if len((key_del_list(response.json()))["delete"]) != 0: deleted_files = deleted_files + ((key_del_list(response.json()))["delete"])  # if the file has been deleted
            # downloading files of new commits
            for fileurl in path:     
                  urllib.parse.quote(fileurl)
                  dir_name = os.path.dirname(fileurl)  
                  # if the file is in a separate folder(create new folder)
                  if dir_name != '':     
                        folder_path = os.path.join(file_folder, dir_name)
                        if not os.path.exists(folder_path):
                              os.makedirs(folder_path)
                        dir_name = dir_name + "/"
                  _fileurl = urllib.parse.quote_plus(fileurl)
                  api_url = _api_url + f'/repository/files/{_fileurl}?ref={commithash}'
                  response = requests.get(api_url, headers=headers)
                  file_name = response.json()["file_name"]
                  # decoding content from files
                  sha = response.json()["blob_id"]
                  api = _api_url + f'/repository/blobs/{sha}'
                  response = requests.get(api, headers=headers)
                  base64_message = response.json()["content"]
                  base64_bytes = base64_message.encode('utf-8')
                  message_bytes = b64decode(base64_bytes)
                  message = message_bytes.decode('utf-8')
                  # saving to a file
                  with open(file_folder + '/' + dir_name + file_name, "w") as file:
                        file.write(message)

      # deleting files from a folder that have been deleted
      delete_f(deleted_files)