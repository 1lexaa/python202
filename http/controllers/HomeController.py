import appsettings
from starter import MainHandler


class HomeController :

    def __init__( self, handler:MainHandler ) -> None:
        self.handler = handler
        self.short_name = self.__class__.__name__.removesuffix('Controller').lower()
        self.view_path = f"{appsettings.VIEWS_PATH}/{self.short_name}"


    def index( self ) -> None :
        self.handler.return_view() 


    def privacy( self ) :
        self.handler.return_view() 
