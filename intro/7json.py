# Робота з даними у форматі JSON
import json  # входить у базовий комплект Python

def create_json_file() -> None :
    try :
        with open( "data.json", mode="w", encoding="utf-8" ) as file :
            file.write( '''{
                       "str": "Hello, World",
                       "digital": 1213,
                       "float": 1.456,
                       "bool1": true,
                       "null": null,
                       "obj": {
                            "bool0": false,
                            "str": "A string"
                       },
                       "arr": [1,2,3,4,5]
            }''' )
    except IOError as err :
        print( err )
    else :
        print( "create_json_file OK" )


def print_json() :
    try :
        with open("data.json") as file :
            j = json.load( file )
        print( type(j), j )
        for k in j :
            print( k, j[k], type(j[k]) )
    except :
        print( "Error" )


def main() -> None :
    # create_json_file()
    print_json()


if __name__ == "__main__" :
    main()