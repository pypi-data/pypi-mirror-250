from File import File

class Dependancies:
    def __init__( self ) -> None:
        self.files = [] # list[File]

    def __iadd__( self, that ):
        if isinstance( that, Dependancies ):
            for dep in that.files:
                self += dep 
            return self
        
        if that not in self.files:
            self.files.append( that )
        return self

    def add_file( self, f: File ):
        for g in self.files:
            if g.resolved_name == f.resolved_name:
                return
        self.files.append( f )


