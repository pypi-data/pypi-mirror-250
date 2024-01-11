from pathlib import Path
import os

class File:
    def __init__( self, input : Path | str ) -> None:
        self.input_path = Path( input )
        self.input_name = str( input )
        self.suffix = self.input_path.suffix
        self.stem = self.input_path.stem

        self.resolved_path = self.input_path.resolve()
        self.resolved_name = str( self.resolved_path )

        self.modification_date = os.path.getmtime(self.input_path )

    def relative_name( self ):
        try:
            return str( Path.relative_to( self.input_path, Path.cwd() ) )
        except ValueError:
            return self.input_name
