import api_controller
import  json
import sys

class ProductController( api_controller.ApiController ) :

    def do_get( self ) :
        self.send_response( body="ProductController works!" )


    def do_put( self ) :
        # Тіло запиту при CGI передається до stdin
        request_body = sys.stdin.read().encode("cp1251").decode("utf-8")
        body_data = json.loads( request_body )
        if not ( 'name' in body_data and 'price' in body_data ) :
            self.send_response( 400, "Bad Request",
                               { "message": "Required: 'name' and 'price' " } )
        self.send_response( body=request_body )