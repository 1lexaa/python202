import json
import mysql.connector
import os
import sys
import re

class ApiController :

    def __init__( self ) -> None:
        self.db_connection = None

    def serve( self ) -> None :
        '''Основний метод оброблення запиту з розглажунням
        у відповідності до НТТР-методу'''
        
        method = os.environ.get( 'REQUEST_METHOD', '' )   # "GET"
        action = f"do_{method.lower()}"                   # "do_get"
        attr = getattr( self, action, None )              # obj.do_get
        if attr is None :
            self.send_response( 405, "Method Not Allowed", 
                               { "message": f"Method '{method}' not allowed" } )
        else :
            attr()

    def send_response( self, 
                      status_code:int=200, 
                      reason_phrase:str="OK", 
                      body:object=None,
                      data:object=None,
                      meta:object=None ) -> None :
        status_header = f"Status: {status_code} {reason_phrase if reason_phrase else ''}"
        print( status_header )    
        print( "Content-Type: application/json" )
        print( "Connection: close" )
        print()   # порожній рядок - кінець заголовків
        if body :
            print( json.dumps( body ), end='' )
        else :
            print( json.dumps( { "meta": meta, "data": data } ), end='' )
        exit()

    def get_request_json(self) -> dict:
        request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
        return json.loads( request_body )
    

    def get_auth_header_or_exit(self, auth_scheme:str="Basic " ) :
        self.auth_header_name = "HTTP_AUTHORIZATION"
        if not auth_scheme.endswith( ' ' ) :
            auth_scheme += ' '
        if not self.auth_header_name in os.environ :
            self.send_response( 401, "Unauthorized",
                        { "message": "Missing 'Authorization' header" } )
        auth_header_value = os.environ[self.auth_header_name]
        if not auth_header_value.startswith( auth_scheme ) :
            self.send_response( 401, "Unauthorized",
                        { "message": f"Authorization scheme {auth_scheme} required" } )
        return auth_header_value[ len(auth_scheme): ]

    def get_bearer_token_or_exit(self) :
        auth_token = self.get_auth_header_or_exit( 'Bearer ' )
        token_pattern = r"^[0-9a-f-]+$"   # numer, hash or UUID
        if not re.match( token_pattern, auth_token ) :
            self.send_response( 401, "Unauthorized",
                        { "message": f"Malformed Token" } )
        return auth_token