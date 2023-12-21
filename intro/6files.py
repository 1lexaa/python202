# Робота з файлами

def create_file1() -> None :
    filename = "file1.txt"
    file = None
    try :
        file = open( filename, mode="w", encoding="utf-8" )
        file.write( "Latin data\n" )
        file.write( "Кирилічні дані" )
    except OSError as err :
        print( err )
    else :
        file.flush()
        print( "Create OK" )
    finally :
        if file != None :
            file.close()


def read_all_text1( filename:str ) -> str :
    file = None
    try :
        file = open( filename, mode="r", encoding="utf-8" )
    except OSError as err :
        print( err )
    else :
        return file.read()
    finally :
        if file != None : file.close()


def create_headers( filename:str ) -> None :
    try :
        with open( filename, mode="w", encoding="utf-8" ) as file :
            file.write( "Host: localhost\r\n" )
            file.write( "Connection: close\r\n" )
            file.write( "Content-Type: text/css\r\n" )
            file.write( "Content-Length: 100500\r\n" )
    except IOError as err :
        print( "Create headers error:", err )
    else :
        print( "Create headers OK" )


def print_headers( filename:str ) -> None :
    try :
        with open( filename, mode="r", encoding="utf-8" ) as file :
            n = 1
            for x in file :      # Ітерування файлу: відбувається по рядках, але
                print( n, x )    # символи \r\n сприймаються як два рядки
                n += 1           # А також кінцевий символ переведення рядка
                                 # включається до самого "х"
    except IOError as err :
        print( err )


def parse_headers_imp( filename:str ) -> dict | None :
    '''Розбирає файл "filename" і повертає dict 
       з розділеними заголовками на ключі та значення'''
    ret = {}   # {} - dict
    try :
        with open( filename, mode="r", encoding="utf-8" ) as file :
            for line in file :
                if ':' in line :
                    k, v = line.split( ':' )
                    ret[ k.strip() ] = v.strip()  # ~ trim()
        return ret
    except IOError as err :
        print( err )
        return None


def parse_headers( filename:str ) -> dict | None :
    '''Розбирає файл "filename" -- функціональний підхід'''
    try :
        with open( filename, mode="r", encoding="utf-8" ) as file :            
            return { k: v                  # Функціональний підхід - у застосуванні
                for k, v in (              # генераторів - "ледачіх" алгоритмів
                    map( str.strip,        # формування даних. Це дозволяє працювати
                        line.split(':') )  # з Big Data
                    for line in file       # 
                        if ':' in line     # умова фільтрації може додаватись до 
                )}                         # генератора
    except IOError as err :
        print( err )
        return None


def main() -> None :
    # create_file1()
    # print( read_all_text1( "file1.txt" ) )
    # create_headers( "headers.txt" )
    # print_headers( "headers.txt" )
    for k, v in parse_headers( "headers.txt" ).items() :
        print( k, v )

if __name__ == "__main__" :
    main()