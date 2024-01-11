from ..support.Options import Options 
from .Command import Command 
from .Actor import Actor 

from pathlib import Path
import tempfile
import shlex
import os

class Analyzer( Actor ):
    def on_start( self, source: str ) -> None:
        self.add_source_dep( source )
        
        self.tmp_file = tempfile.NamedTemporaryFile()
        flags = compile_flags( 
            self.options.compiler_for( Path( source ).suffix ), 
            self.tmp_file.name, 
            source, 
            self.options, 
            for_includes = True
        )
        self.launch( self.on_gcc_analysis, Command(), flags )

    def on_gcc_analysis( self ):
        # read the content
        content = shlex.split( self.tmp_file.read().decode() )
        self.tmp_file.close()

        # parse it
        includes = []
        for path in content:
            if path.endswith( ":" ):
                continue
            includes.append( os.path.abspath( path ) )
            self.check_file( path )

        # we're done
        self.on_end( includes )

def compile_flags( compiler, out: str, src: str, options: Options, for_includes = False ):
    res = [ compiler, src ]
    if for_includes:
        res += [ '-MM', '-MF', out ]
    else:
        res += [ '-o', out, '-c' ]
    for option in options.all_the_options():
        if option[ 0 ] == 'inc-path':
            res.append( f'-I{ option[ 1 ] }' )
            continue
        if option[ 0 ] == 'cpp-flag':
            res.append( str( option[ 1 ] ) )
            continue
        if option[ 0 ] == 'define':
            res.append( f'-D{ option[ 1 ] }' )
            continue
    return res
