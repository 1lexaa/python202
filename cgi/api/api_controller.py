import logging 
logging.basicConfig(filename='logs.txt', level=logging.INFO, 
    format='%(asctime)s %(levelname)s [%(filename)s::%(lineno)d] %(message)s %(args)s', datefmt='%Y-%m-%d %H:%M:%S')
import json
import os
import re
import sys

class ApiController :

    def __init__(self) -> None:
        self.db_connection = None

    def serve(self) -> None :
        method = os.environ.get('REQUEST_METHOD', '')
        action = f"do_{ method.lower() }"                
        attr = getattr(self, action, None)

        if attr is None :
            self.send_response(405, "Method Not Allowed", { "message": f"Method '{method}' not allowed" })
        else :
            attr()

    def send_response(self, status_code:int=200, reason_phrase:str="OK", body:object=None, data:object=None, 
                      meta:object=None) -> None :
        status_header = f"Status: { status_code } { reason_phrase if reason_phrase else '' }"
        
        print(status_header)    
        print("Content-Type: application/json")
        print("Connection: close")
        print()
        
        if body :
            print(json.dumps(body), end='')
        else :
            print(json.dumps({ "meta": meta, "data": data }), end='')
        exit()

    def get_request_json(self) -> dict :
        request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
        return json.loads(request_body)
    
    def get_auth_header_or_exit(self, auth_scheme:str="Basic "):
        auth_header_name = "HTTP_AUTHORIZATION"
        
        if not auth_scheme.endswith(' '):
            auth_scheme += ' '
        if not auth_header_name in os.environ :
            self.send_response(401, "Unauthorized", { "message": "Missing 'Authorization' header" })
        
        auth_header_value = os.environ[auth_header_name]
        
        if not auth_header_value.startswith(auth_scheme) :
            self.send_response(401, "Unauthorized", { "message": f"Authorization scheme {auth_scheme} required" })
        
        return auth_header_value[len(auth_scheme):]

    def get_bearer_token_or_exit(self) :
        auth_token = self.get_auth_header_or_exit('Bearer ')
        token_pattern = r"^[0-9a-f-]+$"
        
        if not re.match(token_pattern, auth_token) :
            self.send_response(401, "Unauthorized", { "message": f"Malformed Token" })
        return auth_token
    
    def do_get(self) -> None:
        auth_token = self.get_bearer_token_or_exit()
        
        try:
            login, password = base64.b64decode(auth_token, validate=True).decode().split(':', 1)
        except:
            self.send_response(401, "Unauthorized", {"message": "Malformed credentials"})

        sql = "SELECT u.* FROM users u WHERE u.`login`=%s AND u.`password`=%s"

        try:
            with self.connect_db_or_exit().cursor() as cursor:
                cursor.execute(sql, (login, hashlib.md5(password.encode()).hexdigest()))
                row = cursor.fetchone()
                
                if row is None:
                    self.send_response(401, "Unauthorized", {"message": "Credentials rejected"})
                
                user_data = dict(zip(cursor.column_names, row))
                
                self.send_response(body={"scheme": "Bearer", "token": str(user_data['id'])})
        except mysql.connector.Error as err:
            self.send_response(500, "Internal Server Error", str(err))