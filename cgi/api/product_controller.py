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


'''
REST - Representation State Transfer - архітектура для роботи з API 
  = в наших задачах - веб-АРІ (або НТТР)
- єдиний інтерфейс
  = всі запити мають схожу семантику (роль методів GET, POST, ....), 
  = у них схожі принципи передачі даних (структура Query параметрів, 
      тіла, заголовків тощо)
  = єдиний формат відповіді (у т.ч. помилок), включення до відповіді
      окремих деталей запиту
- відсутність збереження стану
  = кожен запит виконується незалежно від попередніх запитів
  = авторизація кожного запиту

GET /auth
Authorization: Basic as5djas= 

200 OK                                          401 Unathorized            
{                                               {        
    meta: {                                         meta: {                
        service: 'auth',                                service: 'auth',                                
        status: 200,                                    status: 401,                            
        scheme: Basic                                   scheme: Basic                            
    }                                               }            
    data: {                                         data: {                
        "scheme": "Bearer",                             "message": "Credentials rejected",                                     
        "token": 100630152223916036,                                                             
        "expires": 630152223916                                                     
    }                                               }            
}                                               }        


GET /product

200 OK  
{   
    meta: { 
        service: 'product', 
        status: 200,    
        count: 15   
    },  
    data: [ 
        {product1}, 
        ... 
        {product15} 
    ]   
}   

GET /product/123

200 OK                                     404 Not Found     
{                                          { 
    meta: {                                    meta: {         
        service: 'product',                        service: 'product',                         
        status: 200,                               status: 404,                     
        count: 1,                                  count: 0,                 
        requestedId: 123                           requestedId: 123                         
    },                                         },     
    data: {                                    data: null     
        id: 123                                                
        name: product5,                                                 
        ...                                                 
    }                                          }     
}                                           }

Д.З. Переробити відповіді сервіса 'auth' за закладеними REST 
правилами. В ідеалі позбутись параметра 'body' у формувачі
відповіді (тільки 'meta' та 'data')
'''