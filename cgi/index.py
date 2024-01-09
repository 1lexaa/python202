# #! C:/Python/python.exe
# import os

# envs = f"<ul>{"".join([f"<li>{k} = {v}</li>" for k,v in os.environ.items()])}</ul>"

# print( "Content-Type: text/html; charset=cp1251" )
# print( "Connection: close" )
# print()
# with open( 'home.html' ) as file :
#     print( file.read() )


#! C:\Users\scrin\AppData\Local\Programs\Python\Python36-32\python.exe
import os
import mysql.connector


from db_ini import connection_params

connection = mysql.connector.connect(**connection_params)
cursor = connection.cursor()
sql_query = "SHOW DATABASES"
cursor.execute(sql_query)
databases = [row[0] for row in cursor.fetchall()]

cursor.close()
connection.close()

table_content = "<table border='1'><tr><th>База данных</th></tr>"

for db in databases:
    table_content += f"<tr><td>{db}</td></tr>"
table_content += "</table>"

# print("Content-Type: text/html; charset=cp1251")
# print("Connection: close")
# print()
# print(f"<html><body>{table_content}</body></html>")



envs = {k: v for k, v in os.environ.items() if k in ["REQUEST_URI", "QUERY_STRING", "REQUEST_METHOD", "REMOTE_ADDR", "REQUEST_SCHEME"]}
envs_html = f"<ul>{ "".join([f"<li>{k} = {v}</li>" for k,v in envs.items()]) }"
envs_html += "</ul>"
envs_html += f"<p>QUERY_STRING: {f"<ul>{ "".join([f"<li>{k} = {v}</li>" for k,v in {k: v for k, v in (pair.split('=') for pair in envs["QUERY_STRING"].split('&'))}.items()]) }"}</p>"

print( "Content-Type: text/html; charset=cp1251" )
print( "Connection: close" )
print()   # порожній рядок - кінець заголовків
print(envs_html)
# with open( 'home.html' ) as file :
#     print( file.read() )