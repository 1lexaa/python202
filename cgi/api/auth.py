#!C:/Python/python.exe

import base64
import hashlib
import json
import mysql.connector
import os
import re
import sys
sys.path.append('../../')
import db_ini
import api_controller  

db_connection = None

def connect_db_or_exit() :
    global db_connection
    
    if not db_connection :        
        try :
            db_connection = mysql.connector.connect(**db_ini.connection_params)
        except mysql.connector.Error as err:
            send_response(500, "Internal Server Error", str(err)) 
    return db_connection

def stringify(func) :
    def wrapper(*args, **kwargs) :
        return str(func(*args, **kwargs))
    return wrapper

def get_auth_header_or_exit(auth_scheme:str="Basic "):
    auth_header_name = "HTTP_AUTHORIZATION"
    
    if not auth_scheme.endswith(' ') :
        auth_scheme += ' '
    if not auth_header_name in os.environ :
        send_response(401, "Unauthorized", {  "message": "Missing 'Authorization' header"  })
    auth_header_value = os.environ[auth_header_name]
    if not auth_header_value.startswith(auth_scheme):
        send_response(401, "Unauthorized", {  "message": f"Authorization scheme { auth_scheme } required"  })
    return auth_header_value[len(auth_scheme):]

@stringify
def get_bearer_token_or_exit() :
    auth_token = get_auth_header_or_exit('Bearer ')
    token_pattern = r"^[0-9a-f-]+$"

    if not re.match(token_pattern, auth_token) :
        send_response(401, "Unauthorized", {  "message": f"Malformed Token"  })
    return auth_token

def send_response(status_code:int=200, reason_phrase:str=None, body:object=None) -> None :
    status_header = f"Status: { status_code } { reason_phrase if reason_phrase else '' }"
    print(status_header)    
    print("Content-Type: application/json")
    print("Connection: close")
    print()
    print(json.dumps(body) if body else '')
    exit()

def query_params() :
    qs = os.environ['QUERY_STRING']
    return {  k: v for k, v in (pair.split('=', 1) for pair in qs.split('&')) } if len(qs) > 0 else {   }


def do_get(controller: api_controller.ApiController) -> None:
    auth_token = controller.get_bearer_token_or_exit()
    
    try:
        login, password = base64.b64decode(auth_token, validate=True).decode().split(':', 1)
    except:
        controller.send_response(401, "Unauthorized", { "message": "Malformed credentials" })

    sql = "SELECT u.* FROM users u WHERE u.`login`=%s AND u.`password`=%s"
    
    try:
        with controller.connect_db_or_exit().cursor() as cursor:
            cursor.execute(sql, (login, hashlib.md5(password.encode()).hexdigest()))
            row = cursor.fetchone()
            
            if row is None:
                controller.send_response(401, "Unauthorized", { "message": "Credentials rejected" })
            
            user_data = dict(zip(cursor.column_names, row))
            controller.send_response(meta={"scheme": "Bearer"}, data={"token": str(user_data['id'])})
    except mysql.connector.Error as err:
        controller.send_response(500, "Internal Server Error", str(err))

    
def do_post(self) -> None:
    try:
        token = self.get_bearer_token_or_exit()
        user_id = dao.Auth.get_user_id_by_token(token)
        
        if user_id is None:
            self.send_response( meta={"service": self.service_name, "count": 0, "status": 403}, 
                               data={"message": "Token expired or invalid"})

        body = self.get_request_json()

        if 'id_product' not in body:
            self.send_response(meta={"service": self.service_name, "count": 0, "status": 400}, 
                               data={"message": "Missing required parameter 'id_product'"})

        cart_item = {'id_product': body['id_product'], 'id_user': user_id, 'cnt': 1}
        
        dao.Cart.add(cart_item)
    except Exception as err:
        self.send_response(meta={"service": self.service_name, "count": 0, "status": 500}, 
                           data={"message": "Internal server error, see logs for details", 'err': str(err)})
    else:
        self.send_response(meta={"service": self.service_name, "count": cart_item['cnt'], "status": 200}, data=cart_item)


def main():
    controller = api_controller.ApiController()
    method = os.environ.get('REQUEST_METHOD', '')

    match method:
        case 'GET':
            return do_get(controller)
        case 'POST':
            return do_post(controller)
        case _:
            controller.send_response(501, "Not Implemented", { "message": f"Method '{ method }' not supported" })

if __name__ == "__main__" :
    main()