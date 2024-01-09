#!С:/Python/python.exe

import base64
import hashlib
import json
import mysql.connector
import os
import re
import sys
sys.path.append( '../../' )   # додатковий шлях для пошуку модулів
import db_ini

db_connection = None
def connect_db_or_exit() :
    global db_connection
    if not db_connection :        
        try :
            db_connection = mysql.connector.connect( **db_ini.connection_params )
        except mysql.connector.Error as err :
            send_response( 500, "Internal Server Error", str(err) )   # TODO: прибрати str(err) 
    return db_connection

def stringify( func ) :
    def wrapper( *args, **kwargs ) :
        return str( func( *args, **kwargs ) )
    return wrapper


def get_auth_header_or_exit( auth_scheme:str="Basic " ) :
    auth_header_name = "HTTP_AUTHORIZATION"
    if not auth_scheme.endswith( ' ' ) :
        auth_scheme += ' '
    if not auth_header_name in os.environ :
        send_response( 401, "Unauthorized",
                      { "message": "Missing 'Authorization' header" } )
    auth_header_value = os.environ[auth_header_name]
    if not auth_header_value.startswith( auth_scheme ) :
        send_response( 401, "Unauthorized",
                      { "message": f"Authorization scheme {auth_scheme} required" } )
    return auth_header_value[ len(auth_scheme): ]


@stringify
def get_bearer_token_or_exit() :
    auth_token = get_auth_header_or_exit( 'Bearer ' )
    token_pattern = r"^[0-9a-f-]+$"   # numer, hash or UUID
    if not re.match( token_pattern, auth_token ) :
        send_response( 401, "Unauthorized",
                      { "message": f"Malformed Token" } )
    return auth_token


def send_response( status_code:int=200, reason_phrase:str=None, body:object=None ) -> None :
    status_header = f"Status: {status_code} {reason_phrase if reason_phrase else ''}"
    print( status_header )    
    print( "Content-Type: application/json" )
    print( "Connection: close" )
    print()   # порожній рядок - кінець заголовків
    print( json.dumps( body ) if body else '' )
    exit()


# Розбираємо рядок QUERY_STRING на dict
def query_params() :
    qs = os.environ['QUERY_STRING']
    return { k: v for k, v in 
    ( pair.split('=', 1) for pair in 
        qs.split('&') ) } if len(qs) > 0 else { }


def do_get() -> None :
    # params = query_params()
    # if not 'login' in params :
    #     send_response( 400, "Bad request", { "message": "Missing required parameter 'login'" } )
    # if not 'password' in params :
    #     send_response( 400, "Bad request", { "message": "Missing required parameter 'password'" } )
    # login, password = params['login'], params['password']
    # Замінюємо алгоритм на Basic Auth (https://datatracker.ietf.org/doc/html/rfc7617)
    auth_token = get_auth_header_or_exit()
    try :
        login, password = base64.b64decode( auth_token, validate=True ).decode().split(':', 1)
    except :
        send_response( 401, "Unauthorized",
                      { "message": "Malformed credentials" } )

    sql = "SELECT u.* FROM users u WHERE u.`login`=%s AND u.`password`=%s"
    try :
        with connect_db_or_exit().cursor() as cursor :
            cursor.execute( sql, ( login, 
                hashlib.md5( password.encode() ).hexdigest() ) )
            row = cursor.fetchone()
            if row == None :
                send_response( 401, "Unauthorized", { "message": "Credentials rejected" } )
            user_data = dict( zip( cursor.column_names, row ) )
            send_response( body={ "scheme": "Bearer", "token": str(user_data['id']) } )
    except mysql.connector.Error as err :
        send_response( 500, "Internal Server Error", str(err) )   # TODO: прибрати str(err) 
    

def do_post() -> None :
    send_response( body=get_bearer_token_or_exit() )


def main() :
    method = os.environ.get( 'REQUEST_METHOD', '' )
    match method :
        case 'GET' :
            return do_get()
        case 'POST' :
            return do_post()
        case _ :
            send_response( 501, "Not Implemented", { "message": f"Method '{method}' not supported" } )


if __name__ == "__main__" :
    main()

# пояснюючи безпекою, веб-сервер не передає за замовчанням заголовок 
# Authorization до скриптів CGI. Для передачі слід вказати налаштування
# віртуального хосту
# 