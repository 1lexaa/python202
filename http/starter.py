import inspect
import time
import uuid
import appsettings
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import importlib
import os
import sys
sys.path.append(appsettings.CONTROLLERS_PATH)

class MainHandler( BaseHTTPRequestHandler ) :
    sessions = dict()   # сесії усіх запитів

    def do_GET( self ) -> None :
        # print( self.path )
        url_parts = self.path.split('?')  # декілька ? у запиті - помилка
        if len(url_parts) > 2 :
            self.send_404()
            return
        path = url_parts[0]
        query_string = url_parts[1] if len(url_parts) > 1 else None
        filename = f"{appsettings.WWWROOT_PATH}/{path}"
        if os.path.isfile( filename ) :
            # передати файл (запит - назва існуючого файлу)
            self.flush_file( filename )
            return
        
        # Робота з Cookie
        self.response_headers = dict()
        self.cookies = dict( ( cookie.split('=') for cookie in 
                    self.headers['Cookie'].split('; ') ) ) if 'Cookie' in self.headers else {}
        
        # Робота з сесіями
        session_id = self.cookies['session-id'] if 'session-id' in self.cookies else str( uuid.uuid1() )
        if not session_id in MainHandler.sessions :  # сесії немає (або відсутній, або неактуальний заголовок)
            # стартуємо нову сесію
            MainHandler.sessions[session_id] = {
                'timestamp': time.time(),
                'session-id': session_id
            }
            self.response_headers['Set-Cookie'] = f'session-id={session_id}'

        self.session = MainHandler.sessions[session_id]
        print( self.session )
        # кінець блоку сесій
        
        path_parts = path.split('/')  # [0] завжди порожній т.як path починається з '/'
        controller_name = ( path_parts[1].capitalize() if path_parts[1] != '' else 'Home' ) + 'Controller'
        action_name = path_parts[2].lower() if len(path_parts) > 2 and path_parts[2] != '' else 'index'
        
        try :
            controller_module = importlib.import_module( controller_name )
            # controller_module = getattr( sys.modules[__name__], controller_name )
            controller_class  = getattr( controller_module, controller_name )
            controller_object = controller_class( handler=self )
            controller_action = getattr( controller_object, action_name )
        except Exception as err :
            print( err )
            controller_action = None

        if controller_action :
            controller_action()
        else :
            self.send_404()
        return
        
    def return_view( self, action_name=None ) :
        layout_name = f"{appsettings.VIEWS_PATH}/_layout.html"
        controller_object = inspect.currentframe().f_back.f_locals['self']
        view_path = f"{appsettings.VIEWS_PATH}/{controller_object.short_name}"

        action_name = f"{view_path}/{inspect.currentframe().f_back.f_code.co_name}.html"
        if not os.path.isfile( layout_name ) or not os.path.isfile( action_name ) :
            print( 'return_view:: file(s) not found: ', action_name, layout_name )
            self.send_404()
            return
        with open( action_name, encoding='utf-8' ) as action :
            with open( layout_name, encoding='utf-8' ) as layout :
                self.send_response( 200 )
                self.send_header( 'Content-Type', 'text/html' )
                for k, v in self.response_headers.items() :
                    self.send_header( k, v )
                self.end_headers()
                self.wfile.write( layout.read().replace( 
                    '<!-- RenderBody -->', action.read() ).encode('utf-8') )
        self.connection.close()

    def flush_file( self, filename:str ) -> None :
        if '..' in filename or not os.path.isfile( filename ) :
            self.send_404()
            return
        # для правильної інтерпретації файлу, а також з метою обмеження - перевіряємо розширення
        ext = filename.split('.')[-1] if '.' in filename else ''
        if ext in ( 'html', 'css' ) :
            content_type = 'text/' + ext
        elif ext == 'js' :
            content_type = 'text/javascript'
        elif ext == 'ico' :
            content_type = 'image/x-icon'
        elif ext in ( 'png', 'bmp', 'gif' ) :
            content_type = 'image/' + ext
        elif ext in ( 'py', 'jss', 'php', 'exe', 'env', 'log', 'bat', 'cmd', 'sql', 'gitignore' ) :
            self.send_404()
            return
        else :
            content_type = 'application/octet-stream'

        self.send_response( 200 )
        self.send_header( 'Content-Type', content_type )
        self.end_headers()
        # оскільки wfile приймає бінарні дані, відкриває файли в бінарному режимі
        with open( filename, "rb" ) as file :
            self.wfile.write( file.read() )
        return
    

    def send_404( self ) -> None :
        self.send_response( 404 )
        self.send_header( 'Status', "404 Not Found" )
        self.send_header( 'Content-Type', 'text/plain' )
        self.end_headers()
        self.wfile.write( b"Requested content not found" )

    
    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        # Замінити (прибрати) автоматичне логування кожного запиту
        return None  # super().log_request(code, size)


def main() -> None :
    server = ThreadingHTTPServer( ( '127.0.0.1', 82 ), MainHandler )
    try :
        print( 'Server starting...' )
        server.serve_forever()
    except :
        print( 'Server stopped' )


if __name__ == "__main__" :
    main()


'''
Модуль HTTP
 Альтернативне рішення для серверного застосунку - сервер, створений
 засобами мови програмування (платформи), який базується на модулях
 (бібліотеках) мовного пакету.
 У порівнянні з CGI
  + більш мобільний (легше переносити на інший пристрій)
  - як правило, менш швидкодійний
  = може балансувати між швидкістю та повнотою розбору запиту
     (при гарній швидкості майже не проводити аналіз)
 
 Такі технології складаються з двох частин - постійно працюючий
 модуль, який слухає порт (сокет), та обробник, який запускається
 при надходженні запиту.
 
 Відмінності від CGI
 - кодування за замовчанням - utf-8
 - print() виводить у термінал, оскільки запуск іде через
    звичайний Python, а не через CGI. Для виводу у тіло відповіді
    ведеться запис у self.wfile.write(). У параметри передаються
    бінарні дані (не рядок)
 - автоматичний пошук файлів не відбувається, всі запити, навіть ті,
    які стосуються наявних файлів, передаються до do_GET як 
    звичайні запити (у CGI сервер сам повертав файли) з адресою
    у self.path
    запит                self.path
    /public/index.html   /public/index.html
    /public?x=10         /public?x=10
    (nothing)            /
    /                    /
    /123#456             /123
    /123???              /123???
 - параметри запиту передаються через поля і методи класу (Handler),
    а не у параметри методу (req,resp) чи змінні оточення (os.env)
'''
'''
Cookie та сесії
 - заголовки у HTTP-пакетах, які у відповідності до стандартів
    повинні автоматично пересилатись клієнтом у запитах до серверу
    протягом встановленого у заголовках часу.
 - через необхідність підстановки заголовків протягом великого
    часу (за який напевне браузер буде перезапущений), ці дані
    на клієнті зберігаються у постійних сховищах (як правило, у файлах)
 - встановити Cookie може як сервер, надіславши заголовок 
      Set-Cookie: name=value;expires=[DateTime];path=/   
    або клієнт JS командами до document.cookie
    Заміна значення Cookie - повторне її встановлення
    Видалення Cookie - повторне її встановлення з минулим терміном
 - клієнт збирає всі Cookie, передає їх в одному заголовці "Cookie"
    розділені "; ", включаються тількі дані про name1=value1, інші
    параметри опускаються

 Client                                    Server
 GET / 
 Host: localhost ------------------------> HTTP 1/1 200 OK
                                           Set-Cookie:  name1=value1;expires=[DateTime];path=/   
                                           Set-Cookie:  name2=value2;path=/   
 GET /   <-------------------------------  Set-Cookie:  name3=value3
 Host: localhost
 Cookie: name1=value1; name2=value2; name3=value3  -->

 - для чого потрібні Cookie? Для збереженя стану - історії інформаційного
    обміну. Як правило, для помітки того, що даний клієнт раніше вже 
    надсилав дані до цього серверу.
 - за допомогою Cookie організовуються сесії

 Д.З. Забезпечити збереження сесій на час між перезапусками сервера:
 перед зупинкою сервера серіалізувати і зберігати словник MainHandler.sessions 
 перед запуском - десеріалізувати і перекласти в MainHandler
 Перевірити шляхом перезапуску сервера
'''