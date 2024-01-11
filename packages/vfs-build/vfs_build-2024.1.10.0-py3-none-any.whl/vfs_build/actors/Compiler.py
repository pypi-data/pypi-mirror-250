from .Analyzer import Analyzer, compile_flags
from .Command import Command 
from .Actor import Actor
import os

class Compiler( Actor ):
    def on_start( self, source: str ) -> None:
        self.source = source
        
        self.launch( self.on_analyze, Analyzer(), source )

    def on_analyze( self, deps ):
        # register deps
        self.deps = deps

        # read config from directory of dependancies
        for dep in deps:
            self.add_source_dep( dep )

        # make the output filename
        stem, suffix = os.path.splitext( os.path.basename( self.source ) )
        self.output_filename = self.make_output_filename( sub_dirs = [ 'obj' ], ext = "o", stem = stem )

        # launch cmd
        self.info( f"Compile { self.relative_name( self.source ) }" )

        self.launch( self.on_obj, Command(), compile_flags( 
            self.options.compiler_for( suffix ), 
            self.output_filename,
            self.source,
            self.options
        ) )

    def on_obj( self ):
        self.on_end( self.output_filename, self.deps )

