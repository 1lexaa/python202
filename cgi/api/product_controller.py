import api_controller
import sys
sys.path.append('../../')
import dao

class ProductController( api_controller.ApiController ) :

    def do_get( self ) :
        try :
            products = dao.Products.get_all()
        except :
            self.send_response( 
                meta={ "service": "product", "count": 0, "status": 500 },
                data={ "message": "Internal server error, see logs for details" } )
        else :
            self.send_response( 
                meta={ "service": "product", "count": len(products), "status": 200 },
                data=products )


    def do_post( self ) :
        product = self.get_request_json()
        if not ( 'name' in product and 'price' in product ) :
            self.send_response( 400, "Bad Request",
                               { "message": "Required: 'name' and 'price' " } )
        try :
            dao.Products.add( product )
        except :
            self.send_response( 
                meta={ "service": "product", "count": 0, "status": 500 },
                data={ "message": "Internal server error, see logs for details" } )
        else :
            self.send_response( 
                meta={ "service": "product", "count": 1, "status": 201 },
                data={ "message": "Created" } )

