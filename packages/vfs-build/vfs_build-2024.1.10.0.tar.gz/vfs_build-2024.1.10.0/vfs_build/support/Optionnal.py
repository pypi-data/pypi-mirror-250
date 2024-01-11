class Optionnal:
    """ Optionnal( something ) like in rust... """
    def __init__( self, *args ) -> None:
        if len( args ) == 0:
            self.defined = False
            self.value = None
        else:
            self.defined = True
            self.value = args[ 0 ]

    def __bool__( self ):
        return self.defined
