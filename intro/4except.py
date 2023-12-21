# Виняткові ситуації, Exceptions

def throw() -> None :
    print( "Raising error" )
    raise TypeError


def throw_msg() -> None :
    print( "Raising message error" )
    raise ValueError( "The error message" )


def no_throw() -> None :
    pass               # у Python немає поняття порожнього блоку, типу {}
                       # якщо у блоці немає операцій, то використовується 
                       # "заглушка" pass (NOP)

def main() -> None :
    try :
        throw()
    except :
        print( "Error detected" )

    try :
        throw_msg()
    except TypeError :
        print( "TypeError detected" )
    except ValueError as err :
        print( "ValueError detected: ", err )
    except :
        print( "Unknown error detected" )
    finally :
        print( "Finally action" )

    try :
        no_throw()
    except :
        print( "Unknown error detected" )
    else :                         # продовження у разі відсутності 
        print( "Else action" )     # винятків але не після return
    finally :                      # виконається завжди, навіть якщо у 
        print( "Finally action" )  # блоках буде return



if __name__ == "__main__" :
    main()