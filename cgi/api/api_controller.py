import json
import os

class ApiController :

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


    def send_response( self, status_code:int=200, reason_phrase:str="OK", body:object=None ) -> None :
        status_header = f"Status: {status_code} {reason_phrase if reason_phrase else ''}"
        print( status_header )    
        print( "Content-Type: application/json" )
        print( "Connection: close" )
        print()   # порожній рядок - кінець заголовків
        print( json.dumps( body ) if body else '', end='' )
        exit()